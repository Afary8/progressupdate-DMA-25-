import time
import board
import neopixel

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

pixel.brightness = 0.05

f = open("files/Storyline - Sheet1 (3).csv", "r")
rgbString = f.read()
f.close()

# The reason for all the mess is that a csv file is being read as a string
# then inside the string are characters "\n" and "\r"
# first I turn the string into an array by splitting by the "\n" character
# But! Theres the "\r" characters as well in each element so I remove those as well in the for loop
# Then finally in the rgb loop I take each element, split by "," then convert it from a string to an int
# and only then can I finally print 

# All the print statements was me debugging, I've decided to keep it in since it shows my train of thought

rgbArray = rgbString.split("\n")

# print(rgbString)

num_lines = rgbString.count("\n")

# print(num_lines)
# print("")
# print(rgbArray)

for i in range(len(rgbArray)):
    clean = rgbArray[i].replace("\r","")
    rgbArray[i] = clean

# print(rgbArray)
# single_line = rgbArray[0].split(",")
# print(single_line)

def story():
    for i in range(len(rgbArray)):
        single_line = rgbArray[i].split(",")
        r = int(single_line[0])
        g = int(single_line[1])
        b = int(single_line[2])
        pixel.fill((r,g,b))
        # print(r)
        time.sleep(0.5)

while True:
    story()
    pixel.fill((0,0,0))
    time.sleep(2)