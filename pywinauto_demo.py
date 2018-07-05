'''
@own: SQA
Function: this script defines "Open HID","Enter DFU", and "Check DUT SW Version"

@author: Bruce.Zhu

2016-10-25
'''
import os
#import re
from pywinauto import application
from time import sleep
import sys
import time


file_path = os.getcwd()
hid=r"%s\HID_CMD.exe"%file_path

def __init__():
    global dlg,app,vendorID,usbID,openHID,sendButton,recButton,closeButton,clearButton,sendBlank,vendor_ID  
    global usb_ID,command,change_ser_no,question
    Usb_ID = [" ","1000","1006","2000","1007","1004","1005"]  
    print "1.CA9    2.CA9MKII    3.CA10    4.CA10MKII    5.CA18    6.CA19"
    model = raw_input("Please select your sample's model:")
    f=0
    while f==0:
        if model.isdigit():
            if int(model) in range(1,7):
                usb_ID = Usb_ID[int(model)]
                print "\n"
                f=1
            else:
                model = raw_input("No model name!Please select again:")
        else:
            model = raw_input("No model name!Please select again:")
            
    print "1.Battery    2.Temperature    3.All information"
    Command = [" ","get_batt_cap","get_batt_temp","All"]
    cmd = raw_input("Please select:")
    f=0
    while f==0:
        if cmd.isdigit():
            if int(cmd) in range(1,4):
                command = Command[int(cmd)]
                print "\n"
                f=1
            else:
                cmd = raw_input("No model name!Please select again:")
        else:
            cmd = raw_input("No model name!Please select again:")

    if command=="All":
        question=raw_input("Do you want to set serial number?(y/n)")
        print "\n"
        if question==("y"or "Y"):
            change_ser_no=raw_input("Please input serial number you want(1-8 number):")
            while not change_ser_no.isdigit():
                change_ser_no=raw_input("Please input correct serial number(1-8 number):")
            print "\n"
            
            
    vendor_ID = "0cd4"
    app=application.Application()
    app.start_(hid)
    sleep(1.5)
    dlg=app.window_(title_re="HID*")
    vendorID=dlg[u'Edit4']     #USB Vendor ID
    usbID=dlg[u'Edit3']        #USB Product ID set different value according to different projects  CA9:1000  CA10:3000 SP1:5000
    openHID=dlg[u'Button1']
    sendButton=dlg[u'Button4']
    recButton=dlg[u'Button5']
    closeButton=dlg[u'Button2'] #close
    clearButton=dlg[u'Button3'] #clear
    sendBlank=dlg[u'Edit2']
    

def isOpenHID():
    vendorID.SetText(vendor_ID)
    usbID.SetText(usb_ID) 
    openHID.Click()
    okMsg="<HID OK"
    consoleMsg=dlg[u'Edit1'].WindowText()
    if okMsg in consoleMsg:
        print "HID open successfully!"
        return True
    else:
        print "HID open fail!Going to exit..."
        #print time.strftime(r'%Y%m%d%H%M%S',time.localtime())
        dlg.Close()
        raw_input("Press any button to exit and replug your usb again!.............")
        sys.exit(1)
       
def isEnterDFU():
    if isOpenHID():
        sendBlank.SetText("dfu_mode")
        sendButton.Click()
        sleep(0.5)
        recButton.Click()
        sleep(0.5)
        readFailMsg="Read fail !!"
        consoleMsg=dlg[u'Edit1'].WindowText()
        if readFailMsg in consoleMsg:#Based on the fact that if "read fail", DUT is in DFU mode
            print "Enter DFU successfully!Going to close HID Demo APP..."
            dlg.Close()
            return True
        else:
            print "Cannot Enter DFU!!Going to exit..."
            #print time.strftime(r'%Y%m%d%H%M%S',time.localtime())
            dlg.Close()
            raw_input("Press any button to exit and replug your usb again!.............")
            sys.exit(1)

def isOn():
    openHID.Click()  
    sendBlank.SetText("get_mode")
    sendButton.Click()
    sleep(0.5)
    recButton.Click()
    sleep(0.5)
    okMsg="ON"
    consoleMsg=dlg[u'Edit1'].WindowText()
    #print consoleMsg
    if okMsg in consoleMsg:
        print "DUT is on!"
        return True
    else:
        print "DUT is off"
        print "Auto on..."
        sendBlank.SetText("power_button_press")
        time.sleep(0.5)
        sendButton.Click()
        sleep(6) #wait power on
        return True
        #isOn() # Recursive judgment.



def check_info(cmd,s):
    clearButton.Click()
    sendBlank.SetText(cmd)
    sendButton.Click()
    sleep(0.5)
    if ("dfu_mode" in cmd) or ("power_button_press" in cmd):    
        sleep(0.1)
    else:
        recButton.Click()
        time.sleep(0.5)  #add this to get enough time
        consoleMsg=dlg[u'Edit1'].WindowText()
    if ("dfu_mode" in cmd) or ("power_button_press" in cmd):
        return False
    if "Read fail" in consoleMsg:
        print "Read fail"
        return False
    a,b = consoleMsg.split("= ")
    b=b.strip()  #wipe off space character
    if s!="no print":
        print "%s(%s):  %s"%(cmd,s,b) #here didn't include the mag == "Read fail" situation
    return b

def check(cmd):
    if isOpenHID():
        openHID.Click()       
        if isOn():
            while True:
                clearButton.Click()
                sendBlank.SetText(cmd)
                sendButton.Click()
                sleep(0.3)
                recButton.Click()
                time.sleep(0.3)  #add this to get enough time
                consoleMsg=dlg[u'Edit1'].WindowText()
                if "Read fail" in consoleMsg:
                    print "Read fail"
                    print "Please check your USB status!"
                    return False
                a,b = consoleMsg.split("= ")
                print "%s:  %s-----------------------------%s"%(cmd,b,time.strftime(r'%Y%m%d %H:%M:%S',time.localtime()))  
    dlg.Close()
    sys.exit(1)

def check_info_all():
    if isOpenHID():
        openHID.Click()       
        if isOn():
            check_info("get_dev_name","Device")
            check_info("get_version","Firmware")
            check_info("get_batt_cap","Battery")
            check_info("get_batt_temp","Temperature")
            check_info("get_bt_mac","MAC address")
            origin_ser_no=check_info("get_ser_no","Serial number default")
            # change serial number
            if question==("y"or "Y"):
                sendBlank.SetText("set_ser_no %s"%change_ser_no)
                time.sleep(0.5)
                sendButton.Click()   
                print "********************************************"
                check_ser=check_info("get_ser_no","no print")
                if check_ser==change_ser_no:
                    print "Your serial number has been changed: %s"%check_ser
                    print "********************************************"
                    
                    #back to default serial number 
                    sendBlank.SetText("set_ser_no %s"%origin_ser_no)
                    time.sleep(0.5)
                    sendButton.Click()
                    check_ser=check_info("get_ser_no","no print")
                    if check_ser==origin_ser_no:
                        print "Serial number has been set to default: %s"%check_ser
                else:
                    print "Serial number set failed"
            check_info("power_button_press","no print")
            print "power_button_press,DUT goes to shutdown......"
            sleep(8)
            print "dfu_mode,DUT goes to DFU mode......"
            check_info("dfu_mode","no print")
            sleep(1)
            print "Check over! Please replug your USB to exit DFU mode!"
            print "------------------------------------------------------%s"%(time.strftime(r'%Y%m%d %H:%M:%S',time.localtime()))  
    dlg.Close()
    raw_input("Press any button to exit!........")
    sys.exit(1)    
 
def main():
    __init__()
    if command=="All":      
        check_info_all()
    else:
        check(command)     
    
if __name__ == '__main__':
    main()

