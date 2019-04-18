import os
import time
from grove.i2c import Bus
from sgp30 import Sgp30 as GroveVOC_eCO2GasSgp30
from grove_oled_display_128x64 import *
from sh1107g import *
from grove_12_key_cap_i2c_touch_mpr121 import *
from grove_thumb_joystick import *
from grove_temperature_humidity_bme680 import *
from grove_uv_sensor import *
from grove_3_axis_accelerometer_adxl372 import *


#oled = GroveOledDisplay128x64()
oled = SH1107G_SSD1327()
mpr121 = Grove12KeyCapTouchMpr121()
joy = GroveThumbJoystick(0)
bme680 = GroveBME680()
veml = veml6070.VEML6070(0)
acc = Grove3AxisAccelerometerADXL372()


disp_bme680 = 0

disp_uv = 1
disp_acc = 2
disp_mpr121 = 3

first_disp = disp_bme680
last_disp = disp_mpr121
curr_disp = first_disp


last_time_disp = disp_bme680



def disp_bme_sensor():
    global curr_disp
    global last_time_disp
    
    oled.setCursor(0,0)
    oled.write("1")

    val = bme680.read()
    '''
    oled.setCursor(0,0)
    oled.puts(str(val.temperature)[0:4])
    oled.setCursor(0,1)
    oled.puts(str(val.pressure)[0:4])
    oled.setCursor(0,2)
    oled.puts(str(val.humidity)[0:4])
    if(val.heat_stable):
        oled.puts(str(val.gas_resistance)[0:5])
    oled.setCursor(0,3)
    '''
    x, y = joy.value
    if(x > 600):
        time.sleep(0.1)
        if(x > 600):
            curr_disp += 1
            last_time_disp = disp_bme680
    if(x < 300):
        time.sleep(0.1)
        if(x < 300):
            curr_disp -= 1
            last_time_disp = disp_bme680
    '''
    val = bme680.read()
    oled.setCursor(0,0)
    oled.puts(str(val.temperature)[0:4])
    oled.setCursor(0,1)
    oled.puts(str(val.pressure)[0:4])
    oled.setCursor(0,2)
    oled.puts(str(val.humidity)[0:4])
    if(val.heat_stable):
        oled.puts(str(val.gas_resistance)[0:5])
    oled.setCursor(0,3)
    '''


def disp_uv_sensor():
    global curr_disp
    global last_time_disp
    
    if(curr_disp != last_time_disp):
        last_time_disp = curr_disp
        oled.clear()
    oled.setCursor(0,0)
    oled.write("UV sensor : ")
    oled.setCursor(2,0)
    oled.write("      ")
    oled.write(str(veml.getUVIntensity()))
    
    x, y = joy.value
    if(x > 600):
        time.sleep(0.1)
        if(x > 600):
            curr_disp += 1
            last_time_disp = disp_uv
    if(x < 300):
        time.sleep(0.1)
        if(x < 300):
            curr_disp -= 1
            last_time_disp = disp_uv

    
    
clear_flag = [0] * 12
def disp_mpr121_sensor():
    global curr_disp
    global last_time_disp
    global clear_flag
    
    if(curr_disp != last_time_disp):
        last_time_disp = curr_disp
        oled.clear()
    for i in range(12):
        if(clear_flag[i]):
            clear_flag[i] = 0
            oled.setCursor(i,0)
            oled.write("                ")
    result = mpr121.listen_sensor_status()
    for i in range(12):
            if(result[i] != 0):
                if(0 == mpr121.touch_flag[i]):
                    mpr121.touch_flag[i] = 1
                    oled.setCursor(i,0)
                    string = "chan: %d pressed"%(i)
                    oled.write(string)
                    #print("Channel %d is pressed,value is %d" %(i,result[i]))
            else:
                if(1 == mpr121.touch_flag[i]):
                    mpr121.touch_flag[i] = 0

                    oled.setCursor(i,0)
                    string = "chan: %d released"%(i)
                    oled.write(string)
                    clear_flag[i] = 1
                    #print("Channel %d is released,value is %d" %(i,result[i]))

    x, y = joy.value
    if(x > 600):
        time.sleep(0.1)
        if(x > 600):
            last_time_disp = disp_mpr121
            curr_disp += 1
    if(x < 300):
        time.sleep(0.1)
        if(x < 300):
            last_time_disp = disp_mpr121
            curr_disp -= 1
    '''
    oled.setCursor(0,0)
    result = mpr121.listen_sensor_status()
    mpr121.parse_and_print_result(result)
    '''

def dsp_adxl372():
    global curr_disp
    global last_time_disp
    
    if(curr_disp != last_time_disp):
        last_time_disp = curr_disp
        oled.clear()

   
    if acc.status | DATA_READY:
        x, y, z = acc.read()
        x = (x-6)/10.0
        y = (y+4)/10.0
        z = (z+43)/10.0

        oled.setCursor(0,0)
        oled.write("X axis: ")
        oled.setCursor(1,6)
        string = "%f   "%(x)
        
        oled.write(string[0:4]+ " g")

        oled.setCursor(4,0)
        oled.write("Y axis: ")
        oled.setCursor(5,6)
        string = "%f   "%(y)
        oled.write(string[0:4]+ " g")

        oled.setCursor(8,0)
        oled.write("Z axis: ")
        oled.setCursor(9,6)
        string = "%f   "%(z)
        
        oled.write(string[0:4]+ " g")
       

    x, y = joy.value
    if(x > 600):
        time.sleep(0.1)
        if(x > 600):
            last_time_disp = disp_acc
            curr_disp += 1
    if(x < 300):
        time.sleep(0.1)
        if(x < 300):
            last_time_disp = disp_acc
            curr_disp -= 1
    
    
    

def demo():

    global curr_disp
    mpr121.sensor_init()
    # mpr121.set_threshold(0x60)
    mpr121.wait_for_ready()
    
    oled.backlight(False)
    time.sleep(.5)
    oled.backlight(True)

    sample_rate = 400  # Hz
    acc.timing_control(sample_rate=sample_rate)
    acc.measurement_control(bandwidth=sample_rate/2, low_noise=1)
    acc.fifo_control(mode=1, format=0, samples=0x81)
    acc.power_control(mode=3, low_pass_filter=1, high_pass_filter=0)

    while 1:
		##
        if(0 == curr_disp):
            disp_bme_sensor()    
        elif(1 == curr_disp):
            disp_uv_sensor()
        elif(2 == curr_disp):
            dsp_adxl372()
        elif(3 == curr_disp):
            disp_mpr121_sensor()
        else:
            if(curr_disp > 0):
                curr_disp = first_disp
            else:
                curr_disp = last_disp
        time.sleep(0.1)
'''
        d = bme680.read()
        if d:
            fmt = '{0:.2f} C, {1:.2f} hPa, {2:.2f} %RH'.format(
                d.temperature, d.pressure, d.humidity)
            if d.heat_stable:
                fmt += ' {1} Ohms'.format(fmt, d.gas_resistance)
            print(fmt)
		##
        print("UV Value: {0}".format(veml.getUVIntensity()))
		##
        x, y = joy.value
        if x > 900:
            print('Joystick Pressed')
        print("X, Y = {0} {1}".format(x, y))
		##
        oled.setCursor(0,0)
        oled.puts('hello')
		##
        result = mpr121.listen_sensor_status()
        mpr121.parse_and_print_result(result)
        time.sleep(1)
		##
        print("")
        print("")
        print("")
'''
        

if __name__ == '__main__':
    demo()






