import asyncore, socket
import json

class HTTPClient(asyncore.dispatcher):

    def __init__(self, host):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( (host, 22893) )
        self.buffer = raw_input('>')

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(8192)
        # data = eval(data)
        f = open("file.txt","r")
        list_ = f.readlines()
        i=0
        for eachLine in list_:
            dictionary = eval(eachLine)
            i=i+1
            print i
            print dictionary
        f.close()
        self.get_input()       

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

    def get_input(self):
        self.buffer = raw_input('>')
        if self.buffer.lower() == 'quit':
            self.handle_close()
        else:    
            self.handle_write()

client = HTTPClient('localhost')
asyncore.loop()
