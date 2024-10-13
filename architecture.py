# this address stores the LOW component of the stack pointer
# you would add one to the address to get the HIGH component of the stack pointer
SP_ADDRESS_LOW = 900
SP_ADDRESS_HIGH = SP_ADDRESS_LOW+1


# arbitrary address
BP_ADDRESS_LOW = 800
BP_ADDRESS_HIGH = BP_ADDRESS_LOW + 1

GLOBAL_P_ADDRESS_LOW = 700
GLOBAL_P_ADDRESS_HIGH = GLOBAL_P_ADDRESS_LOW + 1



X_LOW = "r26"
X_HIGH = "r27"