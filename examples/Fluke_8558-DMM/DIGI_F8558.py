"""
Simple acquisition Fluke 8558A in current Digitize mode.
query_ascii_values method

Connection
----------
External trigger [HP-3245A]: 5 Vpk-pk; 2.5 Voffset; 10 kHz
Current Input [Fluke 5500]: 0.7 Arms 10 Hz
"""
import pyvisa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

rm=pyvisa.ResourceManager()
F8558_address="USB0::0x0F7E::0x8009::624282630::INSTR"
F8558=rm.open_resource(F8558_address)

print("ID: ",F8558.query("*IDN?"))

#Fluke 8558 configuratrion
F8558.write("*RST")
F8558.write("INIT:CONT OFF") #stop trigger
F8558.write("DISPlay ON")

#channel 
F8558.write("ROUT:TERM FRON") #FROM or REAR
F8558.write("ROUT:INP:GUAR OFF") # ON or OFF

#Current
F8558.write("SENS:FUNC \"DIG:CURR\"") 
F8558.write("SENS:DIG:CURR:COUP DC")
F8558.write("SENS:DIG:CURR:RANG 1")
F8558.write("SENS:DIG:FILT 3MHZ")

#Aperture time
F8558.write("SENS:DIG:APER 7E-7")

#Arm setup
F8558.write("ARM:LAY2:SOUR IMM")
F8558.write("ARM:LAY2:COUN 1") #count trigger 2
F8558.write("ARM:LAY2:DEL:AUTO OFF")
F8558.write("ARM:LAY2:DEL 0")
F8558.write("ARM:LAY1:SOUR EXT")
F8558.write("ARM:LAY1:COUN 1") #count trigger 1
F8558.write("ARM:LAY1:DEL:AUTO OFF")
F8558.write("ARM:LAY1:DEL 0")

# #samples=count_tri1*Count_trig2
# Max samples: 5e6 with timestamp
# Max samples: 10e6 without timestamp

#trigger
F8558.write("TRIG:SOUR TIM")
F8558.write("TRIG:TIM 1E-6") #frec sample in 
F8558.write("TRIG:COUN 1E6")
F8558.write("TRIG:DEL:AUTO OFF")
F8558.write("TRIG:DEL 0")
F8558.write("TRIG:HOLD OFF")

# Current source manually setup
print("Configure the current source and press enter: ")
input()

time.sleep(1) #Current channel settling time (to avoid undesired transients) 

#Launch trigger
F8558.write("INIT:CONT ON")
start = time.time()
#Read 
data=F8558.query_ascii_values("READ?", container=np.array) #numpy.ndarray
finish = time.time()

l_data=len(data)
print("Time READ command: ",finish-start)
print("Data length: ",l_data)
print("Data type: ", type(data))
print("Data raw: ",data[:5])

#save in csv
df=pd.DataFrame(data)
df.to_csv(r"F8558\files\data.csv", header=False, index=False)

ts=1E-6
t=np.linspace(0.0, l_data*ts, l_data, endpoint=False)

#Plot data
fig, ax = plt.subplots()
ax.plot(t,data)
ax.set(xlabel='Time [s]', ylabel='Current [A]',
       title='Current Digitize with Fluke 8558A')
ax.grid()
fig.savefig(r"F8558\files\data.png")
plt.show()

"""
Output
------
ID:  FLUKE,8558A,624282630,1.31

Configure the current source and press enter:

Time READ command:  43.23023462295532
Data length:  1000000
Data type:  <class 'numpy.ndarray'>
Data raw:  [-0.431717 -0.431229 -0.431823 -0.431752 -0.431744]

"""