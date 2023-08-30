import machine
from sdcard import SDCard
import os
import gc

def connectSDCard():
  spisd = machine.SoftSPI(-1,miso=machine.Pin(13),mosi=machine.Pin(12),sck=machine.Pin(14))
  sd = SDCard(spisd,machine.Pin(27))
  vfs = os.VfsFat(sd)
  os.mount(vfs,"/sd")
  print(os.listdir())

def df():
  s = os.statvfs('//')
  return ('{0} MB'.format((s[0]*s[3])/1048576))

def free(full=False):
  F = gc.mem_free()
  A = gc.mem_alloc()
  T = F+A
  P = '{0:.2f}%'.format(F/T*100)
  if not full: return P
  else : return ('Total:{0} \n Free:{1} ({2})'.format(T,F,P))