try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct

dst = 1

host = "pool.ntp.org"

def time(NTP_DELTA):
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    res = s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA

# There's currently no timezone support in MicroPython, so
# utime.localtime() will return UTC time (as if it was .gmtime())
# Small change to enable DST (essentially BST until TZ support)
# by manipulating NTP_DELTA value which is derived from following:
# (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
# To use DST, call function again as settime(dst)
def settime( dst = 0 ):
    if dst == 1:
        NTP_DELTA = 3155670000
    else:
        NTP_DELTA = 3155673600
    t = time(NTP_DELTA)
    import machine
    import utime
    tm = utime.localtime(t)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    machine.RTC().datetime(tm)
    print(utime.localtime())
