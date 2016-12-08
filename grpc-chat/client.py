import logging
import grpc
import chat_pb2

from concurrent import futures
from user import User


class Client(User):
    def __init__(self, name, display, host='localhost', port=5000):
        logging.info("init client")

        super().__init__(name)

        class ChatServicerClient(chat_pb2.ChatServicer):
            def Send(self, request, context):
                logging.info("client received message")
                display(request.text)
                return chat_pb2.Message(text="got it")

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        chat_pb2.add_ChatServicer_to_server(ChatServicerClient(), self.server)
        self.server.add_insecure_port("{host}:{port}".format(host=host, port=port))
        self.server.start()

        self.channel = grpc.insecure_channel("{host}:{port}".format(host=host, port=port+1))
        self.stub = chat_pb2.ChatStub(self.channel)

        logging.info("client connected")

    def send_message(self, msg):
        self.stub.Send(chat_pb2.Message(text=msg))
        logging.info("client send message")
