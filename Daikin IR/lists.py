dev_id = 'ir_daikin_ac'         
dev_name = 'IR Daikin AC'         
dev_long = 'IR Daikin AC' 
dev_desc = 'IR Daikin AC Protocol' 

addrcount = 35

header_addresses = [1, 2, 3, 4, 9, 10, 11, 12, 17, 18, 19, 20]
session_addresses = [13, 14, 15, 16]
state_address = [22]
temperature_address = [23]
fan_address = [25]


## IR-Decoding-Definition Config
chsum_address = [8, 16, 35]
dev = 'daikin'
conf = '9470,2,CE4,720,17C,1DA,17C,54A,17C,1E'
values = ("14," + ','.join(('32 ' * len(chsum_address)).split()) + ";01")       ## Replace ;01 with desired values. 01 is special for Daikin
pre = ','.join(("00").split())
pre += ','



#lc, zero, one, stop, frame frequency(timing)
lc =  0.00515       # 5.15ms
zero = 0.00080      # 0.80ms
one = 0.001763      # 1.763ms
stop = 0.000502     # 0.50ms
frame = 0.036032    # 36.032ms
