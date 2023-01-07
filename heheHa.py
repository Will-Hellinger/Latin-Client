import random, playsound, threading

from info import *

def heheHA():
    playsound.playsound(f'.{subDirectory}data{subDirectory}sounds{subDirectory}test.mp3')

try:
    if int(random.randint(1,50)) == 1 and funnySound == True:
        threading.Thread(target=heheHA).start()
except:
    pass