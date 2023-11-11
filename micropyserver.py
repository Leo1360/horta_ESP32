_I='Not found'
_H='^([A-Z]+)'
_G=None
_F='\r\n'
_E='Content-Type: text/plain\r\n\r\n'
_D='method'
_C='handler'
_B='path'
_A=_G
HTTP_CODES={100:'Continue',101:'Switching protocols',102:'Processing',200:'Ok',201:'Created',202:'Accepted',203:'Non authoritative information',204:'No content',205:'Reset content',206:'Partial content',207:'Multi status',208:'Already reported',226:'Im used',300:'Multiple choices',301:'Moved permanently',302:'Found',303:'See other',304:'Not modified',305:'Use proxy',307:'Temporary redirect',308:'Permanent redirect',400:'Bad request',401:'Unauthorized',402:'Payment required',403:'Forbidden',404:_I,405:'Method not allowed',406:'Not acceptable',407:'Proxy authentication required',408:'Request timeout',409:'Conflict',410:'Gone',411:'Length required',412:'Precondition failed',413:'Request entity too large',414:'Request uri too long',415:'Unsupported media type',416:'Request range not satisfiable',417:'Expectation failed',418:'I am a teapot',422:'Unprocessable entity',423:'Locked',424:'Failed dependency',426:'Upgrade required',428:'Precondition required',429:'Too many requests',431:'Request header fields too large',500:'Internal server error',501:'Not implemented',502:'Bad gateway',503:'Service unavailable',504:'Gateway timeout',505:'Http version not supported',506:'Variant also negotiates',507:'Insufficient storage',508:'Loop detected',510:'Not extended',511:'Network authentication required'}
import re,socket,sys,io
from time import sleep
#from typing import Self
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
			sleep(0.3)
	def stop(A):A._connect.close();A._sock.close();A._sock=_A;print('Server stop')
	def add_route(A,path,handler,method='GET'):A._routes.append({_B:path,_C:handler,_D:method})
	def send(A,data):
		if A._connect is _A:raise Exception("Can't send response, no connection instance")
		A._connect.sendall(data.encode())
	def find_route(E,request):
		C=request.split(_F);D=re.search(_H,C[0]).group(1);B=re.search('^[A-Z]+\\s+(/[-a-zA-Z0-9_.]*)',C[0]).group(1)
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
		else:A.send('HTTP/1.0 404 Not Found\r\n');A.send(_E);A.send(_I)
	def _internal_error(A,error):
		B=error
		if A._on_error_handler:A._on_error_handler(B)
		else:
			if'print_exception'in dir(sys):C=io.StringIO();sys.print_exception(B,C);D=C.getvalue();C.close()
			else:D=str(B)
			A.send('HTTP/1.0 500 Internal Server Error\r\n');A.send(_E);A.send('Error: '+D);print(D)
	def send_response(A,response,http_code=200,content_type='text/html',extend_headers=_G):
		C=extend_headers;B=http_code;A.send('HTTP/1.0 '+str(B)+' '+HTTP_CODES.get(B)+_F);A.send('Content type:'+content_type+_F)
		if C is not _G:
			for D in C:A.send(D+_F)
		A.send(_F);A.send(response)
	def sendFile(A,filename):
		A.send("HTTP/1.0 2000"+_F)
		A.send("Content-Type: aplication/json\r\n\r\n")
		with open(filename,"r") as f:
			for line in f:
				A.send(line)

	@staticmethod
	def get_request_method(request):A=request.split(_F);return re.search(_H,A[0]).group(1)
	@staticmethod
	def get_request_query_string(request):
		B=request.split(_F);A=re.search('\\?(.+)\\s',B[0])
		if A is _G:return''
		else:return A.group(1)
	@staticmethod
	def parse_query_string(query_string):
		B=query_string
		if len(B)==0:return{}
		E=B.split('&');C={}
		for F in E:
			A=F.split('=');G=A[0]
			if len(A)==1:D=''
			else:D=A[1]
			C[G]=D
		return C
	@staticmethod
	def get_request_query_params(request):A=get_request_query_string(request);return parse_query_string(A)
	@staticmethod
	def get_request_post_params(request):
		A=request;C=get_request_method(A)
		if C!='POST':return
		B=re.search('\r\n\r\n(.+)',A)
		if B is _G:return{}
		D=B.group(1);return parse_query_string(D)
	@staticmethod
	def unquote(string):
		E='utf-8';A=string
		if not A:return''
		if isinstance(A,str):A=A.encode(E)
		B=A.split(b'%')
		if len(B)==1:return A.decode(E)
		C=bytearray(B[0]);F=C.append;G=C.extend
		for D in B[1:]:
			try:F(int(D[:2],16));G(D[2:])
			except KeyError:F(b'%');G(D)
		return bytes(C).decode(E)