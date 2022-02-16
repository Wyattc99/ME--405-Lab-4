import pyb
import utime
import task_share
import time

tim = pyb.Timer(1, freq = 1000)
pinC1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
pinC0 = pyb.ADC(pyb.Pin.board.PC0)

output_ADC_val = task_share.Queue('i', size = 1000, thread_protect = False,
                                  overwrite = False, name = 1)
time_val = task_share.Queue('i', size = 1000, thread_protect = False,
                                  overwrite = False, name = 2)
state = task_share.Share ('i', thread_protect = False, name = "state")
start_time = task_share.Share ('i', thread_protect = False, name = "state")

# tim.irq(handler=tick, trigger=Timer.TIMEOUT)         # create the interrupt

state.put(0)
start_time.put(time.ticks_us())


def tim_irq(IRQ_SRC):
    if not output_ADC_val.full():
        output_ADC_val.put(pinC0.read(), in_ISR = True)
        time_val.put(time.ticks_diff(time.ticks_us(),start_time.get()), in_ISR = True)
    #elif state.get() == 0:
        #state.put(1)

tim.callback(tim_irq)

while state.get() != 4:
    if state.get() == 0:
        output_ADC_val.clear()
        pinC1.high()
        state.put(1)
        print ('ADC Data')
    elif state.get() == 2:
        #output_ADC_val.clear()
        pinC1.low()
        state.put(3)
        print ('Time Data [us]')
    elif state.get() == 1:
        if output_ADC_val.any():
            for i in range (0,1000):
                print(output_ADC_val.get())
            state.put(2)
    elif state.get() == 3:
        if time_val.any():
            for i in range (0,1000):
                print(time_val.get())
            state.put(4)
            print('done')
    elif state.get() == 4:
        pass

#if __name__ == "__main__":
    #main()