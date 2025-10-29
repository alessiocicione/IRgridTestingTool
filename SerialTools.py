import serial
import time
from XmlTools import write #ctrlaltlPD

def readSerial(port, baud, type, val, destination):
    print("connecting to serial port ", port, "with baud rate ", baud, "...")
    data = []

    try:
        arduinoData = serial.Serial(port, baud)
        print(arduinoData)
    except:
        print("connection failed")
        return

    time.sleep(1)
    if val == " " or val == "":
        val = 0
    val = int(val)

    if type == "ForNumber":
        count = 0
        while count < val:
            while arduinoData.in_waiting == 0 and count < val:
                pass
            dataPacket = str(arduinoData.readline(), 'utf-8').strip('\r\n')
            print(dataPacket)
            data.append(dataPacket)
            count = count + 1
            #time.sleep(.5)
        write(data, destination)
        print('done')
    else:
        start = time.time()
        count = 0
        if type == "ForTime":
            while time.time() - start < val:
                while arduinoData.in_waiting == 0 and time.time() - start < val:
                    pass
                dataPacket = str(arduinoData.readline(), 'utf-8').strip('\r\n')
                print(dataPacket)
                data.append(dataPacket)
                count = count + 1
            write(data, destination)
            print('done')


def readSerialNew(limiterType, port, baud, destination, tag, testLimiter):
    print(f"connecting to serial port {port} at baud rate {baud} \n "
          f"limiter type: {limiterType} \n "
          f"destination folder: {destination} \n "
          f"sample tag: {tag} \n "
          f"test limiter: {testLimiter}")

    data = []
    try:
        arduinoData = serial.Serial(port, baud)
    except:
        print("connection failed")
        return
    time.sleep(1)
    limiter = int(testLimiter)

    if limiterType == "number":
        count = 0
        while count < limiter:
            while arduinoData.in_waiting == 0 and count < limiter:
                pass
            dataPacket = str(arduinoData.readline(), 'utf-8').strip('\r\n')
            print(dataPacket)
            data.append(dataPacket)
            count = count + 1
        write(data, destination, tag.replace(" ",""))
        print('done')
    elif limiterType == "time":
        start = time.time()
        count = 0
        while time.time() - start < limiter:
            while arduinoData.in_waiting == 0 and time.time() - start < limiter:
                pass
            dataPacket = str(arduinoData.readline(), 'utf-8').strip('\r\n')
            print(dataPacket)
            data.append(dataPacket)
            count = count + 1
        write(data, destination, tag.replace(" ",""))
        print('done')
    else:
        pass

