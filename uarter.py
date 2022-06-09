import serial

class UARTER():
    def __init__(self):
        
        # This will have to change, but to what?
        self.port = 'COM10'
        self.baud = 115200
        
    # I want this file to read an xy coordinate one by one from tims computer and give it to me here  
    def Reader(self):
        with serial.Serial(self.port,self.baud) as ser:
            ser.flush()
            line = ser.readline()
            clean = line.decode()
            print(clean)
        return clean