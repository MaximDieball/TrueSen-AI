#!/bin/bash

modprobe libcomposite
cd /sys/kernel/config/usb_gadget/
mkdir -p g1
cd g1

echo 0x103c > idVendor # hp
echo 0x0102 > idProduct # Multifunction Composite Gadget
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2

mkdir -p strings/0x409
echo "7254262830" > strings/0x409/serialnumber
echo "HP" > strings/0x409/manufacturer
echo "HP Gaming Mouse Prototype" > strings/0x409/product

mkdir -p configs/c.1/strings/0x409
echo "Config 1: ECM network" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower

mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 2 > functions/hid.usb0/subclass
echo 4 > functions/hid.usb0/report_length
echo -ne \\x05\\x01\\x09\\x02\\xa1\\x01\\x09\\x01\\xa1\\x00\\x05\\x09\\x19\\x01\\x29\\x03\\x15\\x00\\x25\\x01\\x95\\x03\\x75\\x01\\x81\\x02\\x95\\x01\\x75\\x05\\x81\\x01\\x05\\x01\\x09\\x30\\x09\\x31\\x15\\x81\\x25\\x7f\\x75\\x08\\x95\\x02\\x81\\x06\\xc0\\xc0 > functions/hid.usb0/report_desc

ln -s functions/hid.usb0 configs/c.1/
ls /sys/class/udc > UDC