import sys
import time
import os
import atexit
import threading
import subprocess
from typing import Any
from vertx import EventBus
from queue import Queue
import traceback
from redflagbpm.Services import Service, DocumentService, Context, ResourceService, ExecutionService, RuntimeService


class ServiceError(Exception):
    def __init__(self, body: dict):
        super().__init__(body.get("error"))
        self.trace = body.get("trace")


class BPMService:
    service: Service
    context: Context
    execution: ExecutionService
    documentService: DocumentService
    resourceService: ResourceService
    runtimeService: RuntimeService

    __eb_calls: EventBus
    __eb_handlers: EventBus
    delay = 10
    call_timeout = 30.0
    __handlers = []
    __address_dict: dict

    def __init__(self, host=None, port=None, options=None, err_handler=None, ssl_context=None):
        if host != None:
            pass
        elif 'BPM_HOST' in os.environ:
            host = os.environ['BPM_HOST']
        else:
            host = 'localhost'
        if port != None:
            pass
        elif 'BPM_HOST' in os.environ:
            port = int(os.environ['BPM_PORT'])
        else:
            port = 7000
        if options is None:
            options = {}
        self.__eb_calls = EventBus(host=host, port=port, options=options, err_handler=err_handler,
                                   ssl_context=ssl_context)
        self.__eb_handlers = EventBus(host=host, port=port, options=options, err_handler=err_handler,
                                      ssl_context=ssl_context)
        self.__address_dict = {}
        self.service = Service(self)
        self.context = Context(self)
        self.execution = ExecutionService(self)
        self.documentService = DocumentService(self)
        self.resourceService = ResourceService(self)
        self.runtimeService = RuntimeService(self)

        self.connect()
        atexit.register(self.close)

    def __setAddress(self, address: Any = None):
        """
        Este método se utiliza durante la conexión con el backend de la BPM.
        Establece la dirección vertx habilitada en el backend para comunicarse con el contexto.
        En el uso diario no es necesario invocarlo porque se autoconfigura.
        :param address:
        """
        if isinstance(address, dict):
            addr = address['replyAddress']
        elif isinstance(address, str):
            addr = address
        elif 'BPM_EVENT_BUS_REPLY' in os.environ:
            addr = os.environ['BPM_EVENT_BUS_REPLY']
        else:
            raise ValueError('No address supplied')
        tid = threading.get_ident()
        self.__address_dict[tid] = addr

    def __getAddress(self, address: Any = None) -> str:
        if isinstance(address, dict):
            return address['replyAddress']
        elif isinstance(address, str):
            return address
        elif threading.get_ident() in self.__address_dict:
            return self.__address_dict[threading.get_ident()]
        elif 'BPM_EVENT_BUS_REPLY' in os.environ:
            return os.environ['BPM_EVENT_BUS_REPLY']
        else:
            raise ValueError('No address supplied')

    def send(self, address, headers=None, body=None):
        ret = Queue()
        self.__eb_calls.send(address=address, headers=headers, body=body, reply_handler=lambda msg: ret.put(msg))
        return ret.get(True, self.call_timeout)

    def reply(self, body=None, address=None, headers=None):
        try:
            addr = self.__getAddress(address)
            if not isinstance(body, dict):
                body = {"reply": body}
            self.__eb_calls.send(address=addr, headers=headers, body=body)
        except ValueError as x:
            if str(x) == 'No address supplied':
                print({"reply": body})
                exit(0)
            else:
                raise x

    def fail(self, message: str = None, do_quit=True, address=None, headers=None):
        if message is None:
            message = traceback.format_exc()
        try:
            addr = self.__getAddress(address)
            body = {"error": message, "succeeded": False}
            self.__eb_calls.send(address=addr, headers=headers, body=body)
        except ValueError as x:
            if str(x) == 'No address supplied':
                print({"error": message, "succeeded": False})
            else:
                raise x
        if do_quit:
            quit()

    def call(self, address, body=None, headers=None):
        ret = self.send(address, headers, body)
        if 'body' in ret:
            if 'succeeded' in ret['body']:
                if not ret['body']['succeeded']:
                    raise ServiceError(ret['body'])
            if 'reply' in ret['body']:
                return ret['body']['reply']
        return None

    def connect(self):
        if not self.__eb_calls.is_connected():
            self.__eb_calls.connect()
        if not self.__eb_handlers.is_connected():
            self.__eb_handlers.connect()

    def close(self):
        for address in self.__handlers:
            self.unregister_handler(address)
        if self.__eb_calls.is_connected():
            self.__eb_calls.close()
        if self.__eb_handlers.is_connected():
            self.__eb_handlers.close()

    def __run_external(self, address, handler):
        my_env = os.environ.copy()
        my_env["BPM_EVENT_BUS_REPLY"] = address["replyAddress"]
        subprocess.Popen(sys.executable + " " + handler, env=my_env, shell=True)

    def register_handler(self, address, handler):
        if isinstance(handler, str):
            self.__eb_handlers.register_handler(address, lambda msg: self.__run_external(msg, handler))
        else:
            self.__eb_handlers.register_handler(address, handler)
        self.__handlers.append(address)

    def unregister_handler(self, address, handler=None):
        self.__eb_handlers.unregister_handler(address, handler)
        self.__handlers.remove(address)

    def run(self, address, handler):
        self.register_handler(address, handler)
        self.start()

    def exec(self, script: str, lang: str = 'javascript', context: dict = None, address: object = None) -> object:
        addr = self.__getAddress(address)
        ret = Queue()
        self.__eb_calls.send(address=addr, body={
            "lang": lang,
            "script": script,
            "context": context
        }, reply_handler=lambda x: ret.put(x))
        result = ret.get(True, self.call_timeout)
        if result['body']['succeeded']:
            return result['body']['body']
        else:
            raise ValueError(result['body']['trace'])

    def request(self, request: str, address=None):
        addr = self.__getAddress(address)
        ret = Queue()
        self.__eb_calls.send(address=addr, body={"request": request}, reply_handler=lambda x: ret.put(x))
        return ret.get(True, self.call_timeout)

    def start(self):
        # self.connect()
        try:
            while True:
                time.sleep(self.delay)
        except KeyboardInterrupt:
            self.stop()

    def isConnected(self):
        return self.__eb_calls.is_connected()

    def stop(self):
        print("Stopping...")
        self.close()
        print("Stopped...")
        sys.exit(0)
