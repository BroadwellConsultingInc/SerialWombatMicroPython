import time

millisStart = time.time()
def millis():
    return(int((time.time() - millisStart) * 1000))

def delay(delayMs):
    startTime = millis()
    while (millis() < startTime + delayMs):
        continue

def delayMicroseconds(delayUs):
    startTime = time.time()
    while (time.time() < startTime + delayUs):
        continue
