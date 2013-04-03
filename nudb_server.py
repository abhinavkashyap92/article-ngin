import asyncore
import socket
import nu_database


class QueryHandler(asyncore.dispatcher_with_send):

	def handle_read(self):
		query = self.recv(16384)
		f = open('file.txt','wb')
		if query:
			# make a call to evaluate in nudb.py
			json_list = db.evaluate(query)
			i = 0;
			for eachObject in json_list:
				# print i
				# print eachObject
				# self.send(json.dumps(eachObject))
				f.writelines(str(eachObject) + '\n')
				# i = i+1

			f.close()
			self.send("receive data")

			
		else:
			# there is no query,send error
			 self.send(json.dumps({"error_code":"420"}))

class QueryServer(asyncore.dispatcher):

	def __init__(self , host , port):

		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET , socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind((host,port))
		self.listen(5)


	def handle_accept(self):
		pair = self.accept()

		if pair is not None:
			sock , addr = pair
			print "Connection coming from the address",repr(addr)
			handler = QueryHandler(sock)


if __name__ == '__main__':
	
	db = nu_database.nudb()
	server = QueryServer("localhost",22893)
	asyncore.loop()