import serial

class ArduinoController:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        try:
            self.ser = serial.Serial(self.port, self.baud_rate)
        except serial.SerialException:
            raise RuntimeError("Connection Failed")

    def __del__(self):
        try:
            self.ser.close()
        except AttributeError:
            raise RuntimeError("Close Failed")
