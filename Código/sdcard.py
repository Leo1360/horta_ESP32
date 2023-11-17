_B=False
_A=b'\xff'
from micropython import const
import time
_CMD_TIMEOUT=const(100)
_R1_IDLE_STATE=const(1<<0)
_R1_ILLEGAL_COMMAND=const(1<<2)
_TOKEN_CMD25=const(252)
_TOKEN_STOP_TRAN=const(253)
_TOKEN_DATA=const(254)
class SDCard:
	def __init__(A,spi,cs,baudrate=1320000):
		A.spi=spi;A.cs=cs;A.cmdbuf=bytearray(6);A.dummybuf=bytearray(512);A.tokenbuf=bytearray(1)
		for B in range(512):A.dummybuf[B]=255
		A.dummybuf_memoryview=memoryview(A.dummybuf);A.init_card(baudrate)
	def init_spi(A,baudrate):
		B=baudrate
		try:C=A.spi.MASTER
		except AttributeError:A.spi.init(baudrate=B,phase=0,polarity=0)
		else:A.spi.init(C,baudrate=B,phase=0,polarity=0)
	def init_card(A,baudrate):
		A.cs.init(A.cs.OUT,value=1);A.init_spi(100000)
		for H in range(16):A.spi.write(_A)
		for I in range(5):
			if A.cmd(0,0,149)==_R1_IDLE_STATE:break
		else:raise OSError('no SD card')
		C=A.cmd(8,426,135,4)
		if C==_R1_IDLE_STATE:A.init_card_v2()
		elif C==_R1_IDLE_STATE|_R1_ILLEGAL_COMMAND:A.init_card_v1()
		else:raise OSError("couldn't determine SD card version")
		if A.cmd(9,0,0,0,_B)!=0:raise OSError('no response from SD card')
		B=bytearray(16);A.readinto(B)
		if B[0]&192==64:A.sectors=((B[8]<<8|B[9])+1)*1024
		elif B[0]&192==0:D=(B[6]&3)<<10|B[7]<<2|B[8]>>6;E=(B[9]&3)<<1|B[10]>>7;F=B[5]&15;G=(D+1)*2**(E+2)*2**F;A.sectors=G//512
		else:raise OSError('SD card CSD format not supported')
		if A.cmd(16,512,0)!=0:raise OSError("can't set 512 block size")
		A.init_spi(baudrate)
	def init_card_v1(A):
		for B in range(_CMD_TIMEOUT):
			time.sleep_ms(50);A.cmd(55,0,0)
			if A.cmd(41,0,0)==0:A.cdv=512;return
		raise OSError('timeout waiting for v1 card')
	def init_card_v2(A):
		for C in range(_CMD_TIMEOUT):
			time.sleep_ms(50);A.cmd(58,0,0,4);A.cmd(55,0,0)
			if A.cmd(41,1073741824,0)==0:
				A.cmd(58,0,0,-4);B=A.tokenbuf[0]
				if not B&64:A.cdv=512
				else:A.cdv=1
				return
		raise OSError('timeout waiting for v2 card')
	def cmd(A,cmd,arg,crc,final=0,release=True,skip1=_B):
		D=final;C=arg;A.cs(0);B=A.cmdbuf;B[0]=64|cmd;B[1]=C>>24;B[2]=C>>16;B[3]=C>>8;B[4]=C;B[5]=crc;A.spi.write(B)
		if skip1:A.spi.readinto(A.tokenbuf,255)
		for F in range(_CMD_TIMEOUT):
			A.spi.readinto(A.tokenbuf,255);E=A.tokenbuf[0]
			if not E&128:
				if D<0:A.spi.readinto(A.tokenbuf,255);D=-1-D
				for G in range(D):A.spi.write(_A)
				if release:A.cs(1);A.spi.write(_A)
				return E
		A.cs(1);A.spi.write(_A);return-1
	def readinto(A,buf):
		C=buf;A.cs(0)
		for D in range(_CMD_TIMEOUT):
			A.spi.readinto(A.tokenbuf,255)
			if A.tokenbuf[0]==_TOKEN_DATA:break
			time.sleep_ms(1)
		else:A.cs(1);raise OSError('timeout waiting for response')
		B=A.dummybuf_memoryview
		if len(C)!=len(B):B=B[:len(C)]
		A.spi.write_readinto(B,C);A.spi.write(_A);A.spi.write(_A);A.cs(1);A.spi.write(_A)
	def write(A,token,buf):
		A.cs(0);A.spi.read(1,token);A.spi.write(buf);A.spi.write(_A);A.spi.write(_A)
		if A.spi.read(1,255)[0]&31!=5:A.cs(1);A.spi.write(_A);return
		while A.spi.read(1,255)[0]==0:0
		A.cs(1);A.spi.write(_A)
	def write_token(A,token):
		A.cs(0);A.spi.read(1,token);A.spi.write(_A)
		while A.spi.read(1,255)[0]==0:0
		A.cs(1);A.spi.write(_A)
	def readblocks(A,block_num,buf):
		E=block_num;B=buf;A.spi.write(_A);C=len(B)//512
		if C==1:
			if A.cmd(17,E*A.cdv,0,release=_B)!=0:A.cs(1);raise OSError(5)
			A.readinto(B)
		else:
			if A.cmd(18,E*A.cdv,0,release=_B)!=0:A.cs(1);raise OSError(5)
			D=0;F=memoryview(B)
			while C:A.readinto(F[D:D+512]);D+=512;C-=1
			if A.cmd(12,0,255,skip1=True):raise OSError(5)
	def writeblocks(A,block_num,buf):
		E=block_num;B=buf;A.spi.write(_A);C,G=divmod(len(B),512)
		if C==1:
			if A.cmd(24,E*A.cdv,0)!=0:raise OSError(5)
			A.write(_TOKEN_DATA,B)
		else:
			if A.cmd(25,E*A.cdv,0)!=0:raise OSError(5)
			D=0;F=memoryview(B)
			while C:A.write(_TOKEN_CMD25,F[D:D+512]);D+=512;C-=1
			A.write_token(_TOKEN_STOP_TRAN)
	def ioctl(A,op,arg):
		if op==4:return A.sectors
		if op==5:return 512