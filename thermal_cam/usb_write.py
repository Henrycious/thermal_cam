#!/usr/bin/env python3
import usb.core
import usb.util

# find our device
dev = usb.core.find(idVendor=0xbda, idProduct=0x5840)

# was it found?
if dev is None:
    raise ValueError('Device not found')

dev.write(1, 'test')