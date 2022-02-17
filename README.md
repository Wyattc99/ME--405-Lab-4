# Lab 4: Using Interrupts with RC Circuit
## Authors: Wyatt Conner, Jameson Spitz, Jacob Wong

## Background
In this lab, we create an interrupt method to callback in order to record the time response of an RC circuit. 
We measure the current step response of the RC circuit when given an input voltage. This is accomplished by 
suddenly setting the Nucleo pin (A4) wired to the circuit to high. We read the current value of the RC circuit
by reading the ADC value seen at the outpit Nucleo pin (A5). Additionally, the circuit is grounded to to the
Nucleo ground pin. An image of our circuit setup wired to the Nucleo can be seen in the image below.

### RC Circuit Wiring
![200ms Period Plot](/Plts/MotorResponse_200ms.png)

## Main File
The main task configures the Nucleo pins and initializes the Queue variables to store up to 1500 data points
for time and ADC readings. Additionally, the main file creates an interrupt that reads and stores ADC and time
data when called. This interrupt method is continually triggered with the callback method shown below.

'''python
tim.callback(tim_irq)
'''

Finally, we have a state machine that handles the printing of ADC readings and time data, printing all 1500 data
points of each queue. Once printing is complete, the input voltage pin is set back to low and the program is 
terminated.

## Printing Task
The purpose of the printing tas


