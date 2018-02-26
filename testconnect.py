import sys
sys.path.append("zklib")
from zklib import zklib
import zkconst

zk = zklib.ZKLib("192.168.1.201", 4370)
ret = zk.connect()
print "connection to device:", ret

