"""
This code list all the instruments connected and try to
communicate with them
"""
import pyvisa

rm=pyvisa.ResourceManager()
a=rm.list_resources()

for i in a:
    try:
        b=rm.open_resource(i)
        print(b.query("*IDN?"))
    except:
        print("could not be opened:",i)

"""
Output
------

"""