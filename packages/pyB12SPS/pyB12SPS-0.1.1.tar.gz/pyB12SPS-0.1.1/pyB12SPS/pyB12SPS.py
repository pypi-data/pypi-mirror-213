import numpy as np
import serial
import time
import os
import sys
import serial.tools.list_ports


class Shim:
    def __init__(self, port=None):
        if port == None:
            self.port = self.detectSerialPort()
        else:
            self.port = port

        self.verbose = True
        self.init()

    def init(self):
        if self.verbose:
            print("Connecting to Shim Power Supply using port %s" % self.port)
        self.ser = serial.Serial(self.port, 9600, timeout=1.0)
        time.sleep(0.1)
        self.ser.reset_input_buffer()

    def detectSerialPort(self):
        """Automatically detect serial port

        Returns:
        str: If detected, returns the serial port, None otherwise
        """
        ports = list(serial.tools.list_ports.comports())

        port = None
        for p in ports:
            if p.vid == 10374:
                port = p.device

        return port

    def sch(self, channel, value):
        """Set register to channel"""

        self.send_command("sch %i %i" % (channel, value))

    def rstall(self):
        """Reset all registers"""
        self.send_command("rstall")

    def rst(self, channel):
        """Reset the register of a channel"""
        self.send_command("rst %i" % (channel))

    def status(self):
        """Query Shim Power Supply status"""

        out = self.send_command("status?", recv=True)
        return out

    def save(self):
        """Save all registers to the memory"""

        self.send_command("save")

    def memory(self):
        """Query the registers stored in memory"""

        out = self.send_command("memory?", recv=True)

        return out

    def restore(self):
        """Query all registers from the memory and set to channels"""

        self.send_command("restore")

    def firmware(self):
        """Query firmware version"""
        out = self.send_command("firmware?", recv=True)

        return out

    def serial(self):
        """Query serial number"""
        out = self.send_command("serial?", recv=True)

        return out

    def send_command(self, command, recv=False):
        """Send string command to Shim Power Supply

        Args:
            command (str): string command to be sent
            recv (bool): True if serial port should be read after writing. False by default.

        Returns:
            recv_string (str): if recv = True, returns string received

        Example::

            send_command('rch 1') # Manually send command for reading shim channel 1

        """

        self.ser.reset_input_buffer()  # reset and flush buffer

        send_string = "%s\n" % command

        # specify string as utf-8
        send_bytes = send_string.encode("utf-8")

        # send bytes to MPS
        self.ser.write(send_bytes)

        # Read Bytes from Shim
        if recv == True:
            # NOTE: Remove delay later
            time.sleep(0.01)  # short delay for response
            while self.ser.inWaiting() > 0:
                time.sleep(0.01)  # short delay for response
                from_shim_bytes = self.ser.readline()
                from_shim_string = from_shim_bytes.decode("utf-8").rstrip()

            return from_shim_string


if __name__ == "__main__":
    shim = Shim()
    out = shim.send_command("help", recv=True)
    print(out)
    out = shim.send_command("status?", recv=True)
    print(out)
    print(out)
    out = shim.status()
    print(out)
    del shim

    out_split = out.strip().split(",")

    print(out_split)
