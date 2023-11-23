import SW18B_UnitTest_globals
import SerialWombatAnalogInput
import time
import machine
import SW18B_UnitTest_globals
import SerialWombatResistanceInput
from ArduinoFunctions import delay

class MCP4728:
    def begin(self):
        pass
    def setChannelValue(self,channel, new_value, new_vref = 0, new_gain = 0, new_pd_mode = 0, udac = False):
        cmd = bytearray(3)
        cmd[0] = 0x40 # write reg
        cmd[0] |= channel<<1
        if (udac):
            cmd |= 1
        c16 = new_value
        c16 |= (new_vref << 15)
        c16 |= (new_pd_mode <<13)
        c16 |= (new_gain << 12)
        cmd[1] = (c16 >> 8)
        cmd[2] = (c16 & 0xFF)
        SW18B_UnitTest_globals.i2c.writeto(0x60,cmd)
        
        



global analogSeed
analogSeed = 1

global analog16
analog16 = None

global volt16171819
volt16171819 = None

def setAnalogRatio( pin,  ratio):
  if pin == 16:
      volt16171819.setChannelValue(0, #MCP4728_CHANNEL_A, 
                                   ratio >> 4, 
                                   0, #MCP4728_VREF_VDD, 
                                   0, #MCP4728_GAIN_1X, 
                                   0) #MCP4728_PD_MODE_NORMAL);

  elif pin == 17:
      volt16171819.setChannelValue(1, #MCP4728_CHANNEL_B, 
                                   ratio >> 4, 
                                   0, #MCP4728_VREF_VDD, 
                                   0, #MCP4728_GAIN_1X, MCP4728_GAIN_1X, 
                                   0)# MCP4728_PD_MODE_NORMAL);

  elif pin == 18:
      volt16171819.setChannelValue(2, #MCP4728_CHANNEL_C,
                                   ratio >> 4, 
                                   0, #MCP4728_VREF_VDD, 
                                   0, #MCP4728_GAIN_1X, MCP4728_GAIN_1X, 
                                   0)#MCP4728_PD_MODE_NORMAL);

  elif pin == 19:
      volt16171819.setChannelValue(3, #MCP4728_CHANNEL_D,
                                   ratio >> 4, 
                                   0, #MCP4728_VREF_VDD,
                                   0, #MCP4728_GAIN_1X,  MCP4728_GAIN_1X, 
                                   0)#MCP4728_PD_MODE_NORMAL);


def analogShutdown():
  volt16171819.begin();
  volt16171819.setChannelValue(0, #MCP4728_CHANNEL_A, 
                               0, 
                               0, #MCP4728_VREF_VDD, 
                               0, #MCP4728_GAIN_1X, 
                               3 ) # MCP4728_PD_MODE_GND_500K);
  volt16171819.setChannelValue(1, #MCP4728_CHANNEL_B, 
                               0, 
                               0, #MCP4728_VREF_VDD, 
                               0, #MCP4728_GAIN_1X, MCP4728_GAIN_1X, 
                                3) # MCP4728_PD_MODE_GND_500K);
  volt16171819.setChannelValue(2, #MCP4728_CHANNEL_C, 
                               0, 
                               0, #MCP4728_VREF_VDD, 
                               0, #MCP4728_GAIN_1X, MCP4728_GAIN_1X,  
                               3) # MCP4728_PD_MODE_GND_500K);
  volt16171819.setChannelValue(3, #MCP4728_CHANNEL_D, 
                               0, 
                               0, #MCP4728_VREF_VDD, 
                               0, #MCP4728_GAIN_1X, MCP4728_GAIN_1X,  
                               3) # MCP4728_PD_MODE_GND_500K);

def analog1k( pin):
    if pin == 16:
      volt16171819.setChannelValue(0, #MCP4728_CHANNEL_A, 
                                   0, 
                                   0, #MCP4728_VREF_VDD, 
                                   0, #MCP4728_GAIN_1X,
                                    1) #  MCP4728_PD_MODE_GND_1K);


    elif pin == 17:
      volt16171819.setChannelValue(1, #MCP4728_CHANNEL_B, 
                                   0, 
                                   0, #MCP4728_VREF_VDD, 
                                   0, #MCP4728_GAIN_1X, 
                                   1 )# MCP4728_PD_MODE_GND_1K);


    elif pin == 18:
      volt16171819.setChannelValue(2, #MCP4728_CHANNEL_C, 
                                   0, 
                                   0, #MCP4728_VREF_VDD, 
                                   0, #MCP4728_GAIN_1X, 
                                   1 )# MCP4728_PD_MODE_GND_1K);

    elif 19:
      volt16171819.setChannelValue(3, #MCP4728_CHANNEL_D, 
                                   0, 
                                   0, #MCP4728_VREF_VDD, 
                                   0, #MCP4728_GAIN_1X,
                                    1 )# MCP4728_PD_MODE_GND_1K);




def analogInputTest():
  SW18B_UnitTest_globals.resetAll()
  SW6B = SW18B_UnitTest_globals.SW6B
  SW6E = SW18B_UnitTest_globals.SW6E
  SW6F = SW18B_UnitTest_globals.SW6F
  global volt16171819
  volt16171819 = MCP4728()

  global analog16
  analog16 = SerialWombatAnalogInput.SerialWombatAnalogInput(SW6B)
  analog17 = SerialWombatAnalogInput.SerialWombatAnalogInput(SW6B)
  analog18= SerialWombatAnalogInput.SerialWombatAnalogInput(SW6B)
  analog19= SerialWombatAnalogInput.SerialWombatAnalogInput(SW6B)
  analog16SW4B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW6F)
  analog17SW4B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW6E)
  analog18SW4B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW6E)
  analog19SW4B= SerialWombatAnalogInput.SerialWombatAnalogInput(SW6E);

  analog16.begin(16);
  analog17.begin(17);
  analog18.begin(18);
  analog19.begin(19);
  analog16SW4B.begin(1);
  analog17SW4B.begin(3);
  analog18SW4B.begin(2);
  analog19SW4B.begin(1);

  for i in range(0,65535,1024):
    ratio = i;
    setAnalogRatio(16, ratio);
    setAnalogRatio(17, (ratio + 15000) & 0xFFFF);
    setAnalogRatio(18, (ratio + 30000) & 0xFFFF);
    setAnalogRatio(19, (ratio + 45000) & 0xFFFF);

    delay(100);



    for x in range(100):
      SW6B.readTemperature_100thsDegC();
      readResult = analog16.readCounts();
      SW18B_UnitTest_globals.test("ANALOGIN_COUNTS_16", readResult, ratio,256,3);
      
      readResult = analog16.readAveragedCounts();
      SW18B_UnitTest_globals.test("ANALOGIN_AVERAGE_16", readResult, ratio,256,3);
        
      readResult = analog16SW4B.readCounts();
      SW18B_UnitTest_globals.test("ANALOGIN_COUNTS_16_4B", readResult, ratio,512,7);
      
      readResult = analog16SW4B.readAveragedCounts();
      SW18B_UnitTest_globals.test("ANALOGIN_AVERAGE_16_4B", readResult, ratio,512,7);
      delay(0);  

    
    ratio += 15000
    ratio &= 0xFFFF

    for x in range(100):
      SW6B.readTemperature_100thsDegC();
      readResult = analog17.readCounts();
      SW18B_UnitTest_globals.test("ANALOGIN_COUNTS_17", readResult, ratio,256,3);
      

      readResult = analog17SW4B.readCounts();
      SW18B_UnitTest_globals.test("ANALOGIN_COUNTS_17_4B", readResult, ratio,256,3);
      delay(0);
 
    ratio += 15000;
    ratio &= 0xFFFF

    for x in range(100):

      SW6B.readTemperature_100thsDegC();
      readResult = analog18.readCounts();
      SW18B_UnitTest_globals.test("ANALOGIN_COUNTS_18", readResult, ratio,256,3);

      readResult = analog18SW4B.readCounts();
      SW18B_UnitTest_globals.test("ANALOGIN_COUNTS_18_4B", readResult, ratio,256,3);
      delay(0);

    ratio += 15000;
    ratio &= 0xFFFF
    
    for x in range(100):
      SW6B.readTemperature_100thsDegC();
      readResult = analog19.readCounts();
      SW18B_UnitTest_globals.test("ANALOGIN_COUNTS_19", readResult, ratio,256,3);
   
    readResult = analog19SW4B.readCounts();
    SW18B_UnitTest_globals.test("ANALOGIN_COUNTS_10_4B", readResult, ratio,256,3);
    delay(100);



  analogMaxMinTest();
  analogAverageTest();
  analogFilterTest();
  analogShutdown();



def analogMaxMinTest():
  setAnalogRatio(16, 0x8000);
  analog16.readMaximumCounts(True);

  setAnalogRatio(16,0x4000);
  delay(100);
  setAnalogRatio(16,0xC000);
  delay(100);
  minimum = analog16.readMinimumCounts();
  SW18B_UnitTest_globals.test("ANALOGIN_MIN_16", minimum, 0x4000,256,3);

  maximum = analog16.readMaximumCounts();
  SW18B_UnitTest_globals.test("ANALOGIN_MAX_16", maximum, 0xC000,256,3);

def analogAverageTest():

  setAnalogRatio(16, 0x0000);
  analog16.begin(16,10000);
  for i in range(60):
      setAnalogRatio(16,0x4000);
      delay(100);
      setAnalogRatio(16,0xC000);
      delay(100);
  
  average = analog16.readAveragedCounts();
  SW18B_UnitTest_globals.test("ANALOGIN_AVG_16", average, 0x4000,256,3);



def analogFilterTest():
  setAnalogRatio(16, 0xFFFF);
  delay(100);
  analog16.begin(16,10000,65445);
  setAnalogRatio(16, 0);
  delay(500);
  
  result = analog16.readFilteredCounts();
  SW18B_UnitTest_globals.test("ANALOGIN_Filter_16", result, 0x8000,256,3);
  delay(500);
  result = analog16.readFilteredCounts();
  SW18B_UnitTest_globals.test("ANALOGIN_Filter_16_2", result, 0x4000,256,3);
  


def resistanceInputTest():
    resist16 = SerialWombatResistanceInput.SerialWombatResistanceInput(SW18B_UnitTest_globals.SW6B);
    analog1k(16);
    resist16.begin(16);
    delay(2000);

    result = resist16.readAveragedOhms();

    SW18B_UnitTest_globals.test("Resistance_16", result, 1000,100);
    analogShutdown();
  

        
    
