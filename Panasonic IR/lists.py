dev_id = 'ir_panasonic_ac'         
dev_name = 'IR PANASONIC AC'         
dev_long = 'IR PANASONIC AC' 
dev_desc = 'IR PANASONIC Protocol' 

addrcount = 27

header_addresses = [1, 2, 3, 4, 9, 10, 11, 12]
state_address = [14]
temperature_address = [15]
fan_address = [17]
specialmode_addresses = [22]
chsum_address = [8, 27]

## IR-Decoding-Definition Config
dev = 'panasonic'
conf = '9470,2,CE4,720,17C,1DA,17C,54A,17C,1E'
values = ("14," + ','.join(('32 ' * len(chsum_address)).split()) + ";00")       ## Replace ;01 with desired values. 01 is special for Daikin
pre = ','.join(("00").split())
pre += ','

#lc, zero, one, stop, frame frequency(timing)
lc =  0.00515       # 5.15ms
zero = 0.00080      # 0.80ms
one = 0.001763      # 1.763ms
stop = 0.000502     # 0.50ms
frame = 0.01040     # 10.4ms
