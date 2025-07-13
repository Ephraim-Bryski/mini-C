#-------- these are avr specific: -------#

# for 6502 the sp is its own register
SP_ADDRESS_LOW = 900
SP_ADDRESS_HIGH = SP_ADDRESS_LOW+1

X_LOW = "r26"
X_HIGH = "r27"



#--------- BP is for both avr and 6502 -----------#

# arbitrary address
BP_ADDRESS_LOW = 1
BP_ADDRESS_HIGH = BP_ADDRESS_LOW + 1

# for 6502 i just set it to 1ff, but easier to keep things consistent
GLOBAL_P_ADDRESS_LOW = 6
GLOBAL_P_ADDRESS_HIGH = GLOBAL_P_ADDRESS_LOW + 1

#---------- these are 6502 specific --------------#

# in avr you use the x,y,or z register
LOW_INDIRECT_6502 = 3
HIGH_INDIRECT_6502 = 4

# i'm using r30 for the right side
RIGHT_SIDE_6502 = 5



