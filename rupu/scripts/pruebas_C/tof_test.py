import smbus

bus = smbus.SMBus(1)
address = 0x29

try:
    bus.write_quick(address)
    print("I2C device found at address 0x29!")
except Exception as e:
    print(f"Failed to access device: {e}")
