#!/usr/bin/env python
#
# !!! Needs psutil installing:
#
#    $ sudo pip install psutil
#

import os
import sys
from time import sleep
if os.name != 'posix':
    sys.exit('platform not supported')

from datetime import datetime
import psutil
import lcd as lcd

def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return "%sB" % n
    
def cpu_usage():
    # load average, uptime
    av1 = psutil.cpu_percent(interval=None)
    #av1, av2, av3 = os.getloadavg()
    return "Load:    %.1f%% " \
            % (av1 )

def uptime():
    # uptime
    uptime = datetime.now() - datetime.fromtimestamp(psutil.BOOT_TIME)
    return "Up:   %sh" \
            % (str(uptime).split('.')[0])
    
def mem_usage():
    usage = psutil.phymem_usage()
    return "Mem Used: %s " \
            % (bytes2human(usage.used))  

    
def disk_usage(dir):
    usage = psutil.disk_usage(dir)
    return "SDCard: %s %.0f%%" \
            % (bytes2human(usage.used), usage.percent)  

def network(iface):
    stat = psutil.network_io_counters(pernic=True)[iface]
    return "%s:Tx%s,Rx%s" % \
           (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))
    
def stats():

    lcd.str(0,"Olimexino:")
    lcd.str(1,cpu_usage())
    lcd.str(2,uptime())
    lcd.str(3,mem_usage())
    lcd.str(4,disk_usage('/'))
    #lcd.str(3,network('wlan7'))
    lcd.update()    
    
def main():
	lcd.init()
	lcd.clear()
	while(1):
	    	stats()
    		sleep(1)
if __name__ == "__main__":
    main()
