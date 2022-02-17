"""!
@file plottingtask.py
The PC program to communicate to Nucleo through the serial port. This
program also plots the data received through the serial port for the ADC values
and time obtained from our RC circuit. This data is then plotted. 
@author Jacob Wong
@author Wyatt Conner
@author Jameson Spitz
@date   16-Feb-22
@copyright by Jacob Wong all rights reserved
"""

import serial
import time
from matplotlib import pyplot

## Empty Lists and string for manipulating data from serial port time data
time_data = [] 
## Empty Lists and string for manipulating data from serial port ADC data
ADC_data= []


## Empty Lists and string for manipulating data from serial port overall data
string = ''
## Empty Lists and string for manipulating data from serial port int values of the ADC data
ticks = []

## This is an empty array used to store position data from ADC
ADC_count = []
## This is an empty array used to store position data from Timer
time_count = []


# Begins communication with Serial Port COM27
with serial.Serial('COM27', 115200) as s_port:
    
        # CRTL-B
        s_port.write(b'\x02')
        
        # CTRL-C
        s_port.write(b'\x03')

        # CTRL-D
        s_port.write(b'\x04')

        print('No errors')
        ## This varuable represents the data read up until next set of data
        data = s_port.read_until(b'ADC')      
        print('past ADC')
        time.sleep(.1)
        # Flushes buffer until prompt
        time.sleep(.1)
        ## Writes time data as a string to 'ADC_data'
        ADC_data = s_port.read_until(b'Time')
        time.sleep(.1)
        ## Writes ticks data as a string to 'time_data'
        time_data = s_port.read_until(b'done')
        
        ## Time A data in a string format
        ADC_string = ADC_data.decode('Ascii')
        ## Ticks A data in a string format
        time_string = time_data.decode('Ascii')
        
        # Converts ADC data to intergers
        for i in ADC_string:
            if(i.isnumeric()):
                string += i
            elif(i == '\n'):
                try:
                    ADC_count.append(int(string))
                    string = ''
                except:
                    pass
                
        # Converts Time data to intergers        
        for i in time_string:
            if(i.isnumeric()):
                string += i
            elif(i == '\n'):
                try:
                    time_count.append(int(string)/1_000_000)
                    string = ''
                except:
                    pass
        
        print(ADC_count)
        print(time_count)

## Creates and formats 'ADC vs Time' plot
font = {'fontname':'Times New Roman'}
pyplot.plot(time_count, ADC_count, '-k')
pyplot.title('ADC Reading vs. Time', font)
pyplot.xlabel('Time, t [s]', font)
pyplot.ylabel('ADC Value', font)
pyplot.grid()

if __name__ == "__main__":
    print('')