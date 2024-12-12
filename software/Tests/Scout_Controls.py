# Test the pots and switches on the Project Athena keyboard
import time
import board
from digitalio import DigitalInOut, Direction, Pull
import rotaryio


switch1 = DigitalInOut(board.GP2)
switch2 = DigitalInOut(board.GP3)
switch3 = DigitalInOut(board.GP6)
switch4 = DigitalInOut(board.GP7)
switch5 = DigitalInOut(board.GP21)
switch6 = DigitalInOut(board.GP22)
switch_enc = DigitalInOut(board.GP9)
torch = DigitalInOut(board.GP16)

switch1.direction = Direction.INPUT
switch1.pull = Pull.UP
switch2.direction = Direction.INPUT
switch2.pull = Pull.UP
switch3.direction = Direction.INPUT
switch3.pull = Pull.UP
switch4.direction = Direction.INPUT
switch4.pull = Pull.UP
switch5.direction = Direction.INPUT
switch5.pull = Pull.UP
switch6.direction = Direction.INPUT
switch6.pull = Pull.UP
switch_enc.direction = Direction.INPUT
switch_enc.pull = Pull.UP
torch.direction = Direction.OUTPUT
encoder = rotaryio.IncrementalEncoder(board.GP14, board.GP15)
last_position = None

while True:
    if switch1.value is False:
        print("Button 1")
        torch.value = True
        
    if switch2.value is False:
        print("Button 2")
        torch.value = False
        
    if switch3.value is False:
        print("Button 3")
        
    if switch4.value is False:
        print("Button 4")
        
    if switch5.value is False:
        print("Button 5")
        
    if switch6.value is False:
        print("Button 6")
        
    if switch_enc.value is False:
        print("Button Encoder")     
        
    position = encoder.position
    if last_position is None or position != last_position:
        print(position)
    last_position = position
