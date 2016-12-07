import tkinter
from time import localtime, strftime


class Interface:
    def __init__(self, handle_server, handle_client):
        self.root = tkinter.Tk()
        self.root.title("P2P Chat")
        self.root.geometry("400x240+300+200")

        self.handle_server = handle_server
        self.handle_client = handle_client

        self.init_user()
        self.init_server(handle_server)
        self.init_client(handle_client)
        self.init_chatfield()
        self.init_writingfield()

        self.root.mainloop()

    def init_chatfield(self):
        self.chatfield = tkinter.Text(width=30, height=10, state='disabled')
        self.chatfield.grid(row=0, column=1, rowspan=7, padx=20, pady=5)

    def display_message(self, msg):
        self.chatfield.configure(state='normal')
        self.chatfield.insert(tkinter.END, msg)
        self.chatfield.configure(state='disabled')

    def init_writingfield(self):
        self.message_text = tkinter.StringVar()
        tkinter.Entry(width=30, textvariable=self.message_text).grid(row=7, column=1, rowspan=2, padx=20, pady=5)
        self.root.bind("<Return>", lambda x: self.send_message())

    def send_message(self):
        msg = self.message_text.get()
        self.message_text.set("")
        msg = "({tm}) {user}: {msg}\n".format(tm=strftime("%H:%M:%S", localtime()), user=self.user.name, msg=msg)
        self.display_message(msg)
        self.user.send_message(msg)

    def init_user(self):
        self.user_name = tkinter.StringVar()
        self.user_name.set("username")
        tkinter.Entry(width=15, textvariable=self.user_name).grid(padx=5)

    def init_server(self, handle_server):
        tkinter.Label(text="Set server: ").grid()

        self.server_host = tkinter.StringVar()
        self.server_host.set("localhost")
        tkinter.Entry(width=15, textvariable=self.server_host).grid(padx=5)

        self.server_port = tkinter.StringVar()
        self.server_port.set("5000")
        tkinter.Entry(width=15, textvariable=self.server_port).grid(padx=5)

        tkinter.Button(text="Set server", width=15, command=lambda: self.create_user(self.handle_server)).grid(padx=5)

    def init_client(self, handle_client):
        tkinter.Label(text="Connect to server: ").grid(padx=5)

        self.client_host = tkinter.StringVar()
        self.client_host.set("localhost")
        tkinter.Entry(width=15, textvariable=self.server_host).grid(padx=5)

        self.client_port = tkinter.StringVar()
        self.client_port.set("5000")
        tkinter.Entry(width=15, textvariable=self.client_port).grid(padx=5)

        tkinter.Button(text="Connect", width=15, command=lambda: self.create_user(self.handle_client)).grid(padx=5)
        tkinter.Button(text="Connect server", width=15, command=lambda: self.connect_server()).grid(padx=5)

    def create_user(self, user_create):
        self.user = user_create(
            name=self.user_name.get(), display=self.display_message,
            host=self.client_host.get(), port=int(self.client_port.get())
        )

    def connect_server(self):
        self.user.connect(host=self.client_host.get(), port=int(self.client_port.get()))