_C=False
_B='utf-8'
_A=True
import machine,network,socket,re,time
class WifiManager:
	def __init__(A,ssid='WifiManager',password='wifimanager',reboot=_A,debug=_C):
		B=password;A.wlan_sta=network.WLAN(network.STA_IF);A.wlan_sta.active(_A);A.wlan_ap=network.WLAN(network.AP_IF)
		if len(ssid)>32:raise Exception('The SSID cannot be longer than 32 characters.')
		else:A.ap_ssid=ssid
		if len(B)<8:raise Exception('The password cannot be less than 8 characters long.')
		else:A.ap_password=B
		A.ap_authmode=3;A.wifi_credentials='/sd/wifi.dat';A.wlan_sta.disconnect();A.reboot=reboot;A.debug=debug
	def connect(A):
		if A.wlan_sta.isconnected():return
		C=A.read_credentials()
		for(B,*E)in A.wlan_sta.scan():
			B=B.decode(_B)
			if B in C:
				D=C[B]
				if A.wifi_connect(B,D):return
		print('Could not connect to any WiFi network. Starting the configuration portal...');A.web_server()
	def disconnect(A):
		if A.wlan_sta.isconnected():A.wlan_sta.disconnect()
	def is_connected(A):return A.wlan_sta.isconnected()
	def get_address(A):return A.wlan_sta.ifconfig()
	def write_credentials(B,profiles):
		A=[]
		for(C,D)in profiles.items():A.append('{0};{1}\n'.format(C,D))
		with open(B.wifi_credentials,'w')as E:E.write(''.join(A))
	def read_credentials(A):
		B=[]
		try:
			with open(A.wifi_credentials)as D:B=D.readlines()
		except Exception as E:
			if A.debug:print(E)
			pass
		C={}
		for F in B:G,H=F.strip().split(';');C[G]=H
		return C
	def wifi_connect(A,ssid,password):
		print('Trying to connect to:',ssid);A.wlan_sta.connect(ssid,password)
		for B in range(100):
			if A.wlan_sta.isconnected():print('\nConnected! Network information:',A.wlan_sta.ifconfig());return _A
			else:print('.',end='');time.sleep_ms(100)
		print('\nConnection failed!');A.wlan_sta.disconnect();return _C
	def web_server(A):
		A.wlan_ap.active(_A);A.wlan_ap.config(essid=A.ap_ssid,password=A.ap_password,authmode=A.ap_authmode);B=socket.socket();B.close();B=socket.socket(socket.AF_INET,socket.SOCK_STREAM);B.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);B.bind(('',80));B.listen(1);print('Connect to',A.ap_ssid,'with the password',A.ap_password,'and access the captive portal at',A.wlan_ap.ifconfig()[0])
		while _A:
			if A.wlan_sta.isconnected():
				A.wlan_ap.active(_C)
				if A.reboot:print('The device will reboot in 5 seconds.');time.sleep(5);machine.reset()
			A.client,E=B.accept()
			try:
				A.client.settimeout(5.);A.request=b''
				try:
					while _A:
						if'\r\n\r\n'in A.request:A.request+=A.client.recv(512);break
						A.request+=A.client.recv(128)
				except Exception as C:
					if A.debug:print(C)
					pass
				if A.request:
					if A.debug:print(A.url_decode(A.request))
					D=re.search('(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP',A.request).group(1).decode(_B).rstrip('/')
					if D=='':A.handle_root()
					elif D=='configure':A.handle_configure()
					else:A.handle_not_found()
			except Exception as C:
				if A.debug:print(C)
				return
			finally:A.client.close()
	def send_header(A,status_code=200):A.client.send('HTTP/1.1 {0} OK\r\n'.format(status_code));A.client.send('Content-Type: text/html\r\n');A.client.send('Connection: close\r\n')
	def send_response(A,payload,status_code=200):A.send_header(status_code);A.client.sendall('\n            <!DOCTYPE html>\n            <html lang="en">\n                <head>\n                    <title>WiFi Manager</title>\n                    <meta charset="UTF-8">\n                    <meta name="viewport" content="width=device-width, initial-scale=1">\n                    <link rel="icon" href="data:,">\n                </head>\n                <body>\n                    {0}\n                </body>\n            </html>\n        '.format(payload));A.client.close()
	def handle_root(A):
		A.send_header();A.client.sendall('\n            <!DOCTYPE html>\n            <html lang="en">\n                <head>\n                    <title>WiFi Manager</title>\n                    <meta charset="UTF-8">\n                    <meta name="viewport" content="width=device-width, initial-scale=1">\n                    <link rel="icon" href="data:,">\n                </head>\n                <body>\n                    <h1>WiFi Manager</h1>\n                    <form action="/configure" method="post" accept-charset="utf-8">\n        '.format(A.ap_ssid))
		for(B,*C)in A.wlan_sta.scan():B=B.decode(_B);A.client.sendall('\n                        <p><input type="radio" name="ssid" value="{0}" id="{0}"><label for="{0}">&nbsp;{0}</label></p>\n            '.format(B))
		A.client.sendall('\n                        <p><label for="password">Password:&nbsp;</label><input type="password" id="password" name="password"></p>\n                        <p><input type="submit" value="Connect"></p>\n                    </form>\n                </body>\n            </html>\n        ');A.client.close()
	def handle_configure(A):
		C=re.search('ssid=([^&]*)&password=(.*)',A.url_decode(A.request))
		if C:
			B=C.group(1).decode(_B);D=C.group(2).decode(_B)
			if len(B)==0:A.send_response('\n                    <p>SSID must be providaded!</p>\n                    <p>Go back and try again!</p>\n                ',400)
			elif A.wifi_connect(B,D):A.send_response('\n                    <p>Successfully connected to</p>\n                    <h1>{0}</h1>\n                    <p>IP address: {1}</p>\n                '.format(B,A.wlan_sta.ifconfig()[0]));E=A.read_credentials();E[B]=D;A.write_credentials(E);time.sleep(5)
			else:A.send_response('\n                    <p>Could not connect to</p>\n                    <h1>{0}</h1>\n                    <p>Go back and try again!</p>\n                '.format(B));time.sleep(5)
		else:A.send_response('\n                <p>Parameters not found!</p>\n            ',400);time.sleep(5)
	def handle_not_found(A):A.send_response('\n            <p>Page not found!</p>\n        ',404)
	def url_decode(I,url_string):
		A=url_string
		if not A:return b''
		if isinstance(A,str):A=A.encode(_B)
		C=A.split(b'%')
		if len(C)==1:return A
		G=[C[0]];B=G.append;H={}
		for D in C[1:]:
			try:
				E=D[:2];F=H.get(E)
				if F is None:F=H[E]=bytes([int(E,16)])
				B(F);B(D[2:])
			except Exception as J:
				if I.debug:print(J)
				B(b'%');B(D)
		return b''.join(G)