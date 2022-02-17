"""!
@file main.py
    This file uses interupt requests to quickly collect data from an RC circuit.
    It uses two queues to collect time and ADC reading data. After collecting data
    This main file operates as a finite state machine: State 0 - sets Pin C1 high
    State 1 - prints ADC data, State 2 - sets Pin C1 low, State 3 - collects time
    data, State 4 - idle state.

@author Wyatt Conner
@author Jameson Spitz
@author Jacob Wong
@date   2022-Feb-16 
"""
import pyb
import utime
import task_share
import time

## Timer object 1 object operating at frequency 1000 Hz
tim = pyb.Timer(1, freq = 1000)

## Pin PC1 configured as a push/pull output
pinC1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)

## Pin PC0 configured as an ADC
pinC0 = pyb.ADC(pyb.Pin.board.PC0)

## task_share.Queue object collecting ADC data
output_ADC_val = task_share.Queue('i', size = 1500, thread_protect = False,
                                  overwrite = False, name = 1)

## task_share.Queue object collecting time data
time_val = task_share.Queue('i', size = 1500, thread_protect = False,
                                  overwrite = False, name = 2)

## task_share.Share object containing state for finite state machine
state = task_share.Share ('i', thread_protect = False, name = "state")

## task_share.Share object containing the start time for the time_val queue
start_time = task_share.Share ('i', thread_protect = False, name = "state")

# Sets initial values for state and start_time
state.put(0)
start_time.put(time.ticks_us())


def tim_irq(IRQ_SRC):
    """!
    Callback function that adds ADC output data to the 'output_ADC_val' queue and
    the current time to the 'time_val' queue.
    """
    # Checks if queue is not full
    if not output_ADC_val.full():
        # puts data into ADC queue
        output_ADC_val.put(pinC0.read(), in_ISR = True)
        
        # puts time data into time queue
        time_val.put(time.ticks_diff(time.ticks_us(),start_time.get()), in_ISR = True)

# Creates a callback object with the callback function
tim.callback(tim_irq)

# Exits the while loop when finite state machine enters the idle state
while state.get() != 4:
    
    # State 0: sets pin C1 high
    if state.get() == 0:
        output_ADC_val.clear()
        pinC1.high()
        state.put(1)
        print ('ADC Data')
        
    # State 2: Sets pin C1 low    
    elif state.get() == 2:
        pinC1.low()
        state.put(3)
        print ('Time Data [us]')
        
    # State 1: Prints ADC queue one value at a time
    elif state.get() == 1:
        if output_ADC_val.any():
            for i in range (0,1500):
                print(output_ADC_val.get())
            state.put(2)
        
    # State 3: Prints Time queue one value at a time
    elif state.get() == 3:
        if time_val.any():
            for i in range (0,1500):
                print(time_val.get())
            state.put(4)
            print('done')
    
    # State 4: Idle state
    elif state.get() == 4:
        pass
