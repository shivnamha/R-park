#!/usr/bin/python
# "ath\r\n"    used to disconnect call 
#AT+CNUM   Returns the subscriber name/number from the SIM, or internal memory for CDMA phones.
#Returns: +CNUM: Owner Name,15555555555,129
#ss7 signaling packets used to send while calling 

# need to switch to SMS mode 
# "AT+CMGF=1"
# "AT+CMGS=\"443\"" for message 

# "AT+CLIP=1\r" turn on caller ID notification
#http://linksprite.com/wiki/index.php5?title=SIM900_GPRS/GSM_Shield
#useful link
#https://github.com/Makeroni/Arduino-SIM900
#at+clip=1
#OK
#at+cgatt=1 
#RING
#+CLIP: "919811412714",145,"",0,"",0
#ath
#OK
# ser = serial.Serial('/dev/ttyUSB2', 115200, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout=1)
#AT+CENG   to find locations

from time import sleep, time
import datetime  
import re, serial, os 
#from log import Log

no_db={}
# status NONE request, IN, OUT, NONE
# { "919538183628" : {  "status" : "NONE",
#                       "intime" :  0,
#                       "outtime" : 0,
#                    }  
# }

LOG = open("log-txt", "a")

def LOG_write(text):
    ts = time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    LOG.write(timestamp + ":: " + text + "\n")
 
def powerON (ser):
    # Turn on caller ID notification
    ser.write("ATE0\r\n")      # stop echo response
    ser.write("AT+CLIP=1\r")
    ser.write("AT+CRC=1\r")  #Enable extended format of incoming indication (optional)
    ser.write("AT+CVHU=0\r") #Enable call hang-up with ATH command
    ser.write("AT+CMEE=1\r")   # detailed error details
    
    LOG_write("Turn on caller ID notification")
    
def user_req (number, req):
    #a = time.time()
    time = datetime.datetime.now()
#    print( "REQUEST from number->" + number )

    number = str (number)
    if (not no_db.has_key(number) or  ( req == "NONE" )):
        no_db[number]= {  "status" : "REQUEST",
                          "intime" : 0,
                          "outtime" : 0
                       } 
        LOG_write( "REQUEST from number->" + number )

   
    if (no_db[number] and  no_db[number]["status"] == "OUT" ):
        no_db[number]["outtime"] = time
        no_db[number]["status"] = "NONE" 

    if ( no_db[number] and no_db[number]["status"] == "IN" ):
        no_db[number]["intime"] = time
        no_db[number]["status"] = "OUT"

    if (no_db[number] and no_db[number]["status"] == "REQUEST" ):
        no_db[number]["status"] = "IN"
    
    if no_db[number]:
        LOG_write("In user_req: number->" +number+ " In-Time->" + str(no_db[number]["intime"])+ " Out-Time->" +str(no_db[number]["outtime"]))
    
def sendsms(ser, number):
    number = str (number)

    #print no_db
    if not no_db.has_key(number) or not no_db[number]["outtime"]:
        return 

    total = no_db[number]["outtime"] - no_db[number]["intime"]
    if not total:
       return 

    # calculate time difference
    hr  = int (total.total_seconds()/3600)
    mn  = int ((total.total_seconds() % 60)/60)
    sec = int (total.total_seconds() % 3600) 
    tt  = str(hr) + ":" + str(mn) + ":" + str(sec)
    it  = str(no_db[number]["intime"].hour) + ":" + str(no_db[number]["intime"].minute) + ":" + str(no_db[number]["intime"].second)
    ot  = str(no_db[number]["outtime"].hour) + ":" + str(no_db[number]["outtime"].minute) + ":" + str(no_db[number]["outtime"].second)

    # create sms text and send to user 
    sms_text =    "chetan sharma In-Time = " + it + " , Out-Time = " + ot + " , Total-Time = "+ tt
    sms_text = sms_text + '\r'
    ser.flush()
    ser.write('AT+CMGF=1\r')
    sleep(1)
    num="+" + number
    
    ser.write('''AT+CMGS="''' + num + '''"\r''')
    sleep(1)
    ser.write(sms_text + "\r")
    sleep(1)
    ser.write(chr(26))
    sleep(1)
    del no_db[number]

    print( "sent sms to number-> " + num + "text" + sms_text)
    LOG_write( "sent sms to number-> " + num + "text" + sms_text)

def callhalt(ser):
    ser.write("ATH\r")
    LOG_write("call halt")
    
def process_data(ser):
    LOG_write( "In process_data:")
    print( "In process_data:")
    
    while True:
        # Read a line and convert it from b'xxx\r\n' to xxx
        # line = ser.readline().decode('utf-8')[:-2]
        data = ""
        while ser.inWaiting() > 0:
            data += ser.read(60)
            break 

        if data.__len__() > 10:
           callhalt(ser) 
           #LOG_write("after halt" + data)
           print data.split("\r\n")
           #data = ['', 'RING', '', '+CLIP: "917042329978",145,"",0']

           for res in data.split("\r\n"):
#           for res in data:
               print res 
               f_no = re.match(r'.*\"\+?(\d+)\",.*', res , re.M | re.I) 
               
               if f_no:
                   num = int(f_no.group(1))
                   #print num
                   user_req(num, "REQUEST")
                   sendsms(ser, num) 
        ser.flush()
#        sleep(.50)


# __main__
ser = ""
#process_data(ser)
device = '/dev/ttyUSB0'
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=5, xonxoff = False, rtscts = False, bytesize = serial.EIGHTBITS, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE)
#ser = serial.Serial(port="COM6",baudrate=460800,timeout=0,rtscts=0,xonxoff=0)
ser.open()
if ser.isOpen():
    LOG_write("connected to: " + ser.portstr)
    powerON(ser)
    ser.flush()
    while True:
        process_data(ser)
else:
    LOG_write("device not connected to " + device )
ser.close()
