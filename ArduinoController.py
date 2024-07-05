import serial

class ArduinoController:
    def __init__(self, port, baud_rate=9600):
        self.port = port
        self.baud_rate = baud_rate
        try:
            self.ser = serial.Serial(self.port, self.baud_rate)
            print("serial connected")
        except:
            raise RuntimeError("Connection Failed")

    def pull(self):
        try:
            data = self.ser.readline()
            self.ser.flushInput()
            return data
        except:
            raise RuntimeError("Pull Failed")
    
    def push(self, msg):
        assert(isinstance(msg, str))
        try:
            self.ser.write(msg.encode())
        except:
            print("Push Failed")

    def __del__(self):
        try:
            self.ser.close()
        except:
            raise RuntimeError("Close Failed")