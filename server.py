import logging
import grpc
import chat_pb2
from concurrent import futures
from user import User


class Server(User):
    def __init__(self, name, display, host='localhost', port=5000):
        logging.info("init server")

        super().__init__(name)

        class ChatServicerServer(chat_pb2.ChatServicer):
            def Send(self, request, context):
                logging.info("sever received message")
                display(request.message)
                return chat_pb2.Message(text="got it")

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        chat_pb2.add_ChatServicer_to_server(ChatServicerServer(), server)
        server.add_insecure_port("{host}:{port}".format(host=host, port=port))
        server.start()

        logging.info("server started")

    def connect(self, host, port):
        channel = grpc.insecure_channel("{host}:{port}".format(host=host, port=port+1))
        self.stub = chat_pb2.ChatStub(channel)
        logging.info("server connected to client")

    def send_message(self, msg):
        self.stub.Send(chat_pb2.Message(text=msg))
        logging.info("server send message")
