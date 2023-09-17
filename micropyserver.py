_E='Content-Type: text/plain\r\n\r\n'
_D='method'
_C='handler'
_B='path'
_A=None
import re,socket,sys,io
class MicroPyServer:
	def __init__(A,host='0.0.0.0',port=80):A._host=host;A._port=port;A._routes=[];A._connect=_A;A._on_request_handler=_A;A._on_not_found_handler=_A;A._on_error_handler=_A;A._sock=_A
	def start(A):
		A._sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);A._sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);A._sock.bind((A._host,A._port));A._sock.listen(1);print('Server start')
		while True:
			if A._sock is _A:break
			try:
				A._connect,D=A._sock.accept();B=A.get_request()
				if len(B)==0:A._connect.close();continue
				if A._on_request_handler:
					if not A._on_request_handler(B,D):continue
				C=A.find_route(B)
				if C:C[_C](B)
				else:A._route_not_found(B)
			except Exception as E:A._internal_error(E)
			finally:A._connect.close()
	def stop(A):A._connect.close();A._sock.close();A._sock=_A;print('Server stop')
	def add_route(A,path,handler,method='GET'):A._routes.append({_B:path,_C:handler,_D:method})
	def send(A,data):
		if A._connect is _A:raise Exception("Can't send response, no connection instance")
		A._connect.sendall(data.encode())
	def find_route(E,request):
		C=request.split('\r\n');D=re.search('^([A-Z]+)',C[0]).group(1);B=re.search('^[A-Z]+\\s+(/[-a-zA-Z0-9_.]*)',C[0]).group(1)
		for A in E._routes:
			if D!=A[_D]:continue
			if B==A[_B]:return A
			else:
				F=re.search('^'+A[_B]+'$',B)
				if F:print(D,B,A[_B]);return A
	def get_request(A,buffer_length=4096):return str(A._connect.recv(buffer_length),'utf8')
	def on_request(A,handler):A._on_request_handler=handler
	def on_not_found(A,handler):A._on_not_found_handler=handler
	def on_error(A,handler):A._on_error_handler=handler
	def _route_not_found(A,request):
		if A._on_not_found_handler:A._on_not_found_handler(request)
		else:A.send('HTTP/1.0 404 Not Found\r\n');A.send(_E);A.send('Not found')
	def _internal_error(A,error):
		B=error
		if A._on_error_handler:A._on_error_handler(B)
		else:
			if'print_exception'in dir(sys):C=io.StringIO();sys.print_exception(B,C);D=C.getvalue();C.close()
			else:D=str(B)
			A.send('HTTP/1.0 500 Internal Server Error\r\n');A.send(_E);A.send('Error: '+D);print(D)