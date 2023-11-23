import SW18B_UnitTest_globals
import SerialWombatServo
import SerialWombat
import SerialWombatPulseOnChange
from ArduinoFunctions import delay

IP_IN_PIN  = 18
IP_OUT_PIN  = 19
pocInput1 = SerialWombatServo.SerialWombatServo_18AB (SW18B_UnitTest_globals.SW6B)
pocInput2 = SerialWombatServo.SerialWombatServo_18AB (SW18B_UnitTest_globals.SW6B)
pocPin = SerialWombatPulseOnChange.SerialWombatPulseOnChange(SW18B_UnitTest_globals.SW6B)


POC_IN_PIN2 = 17
POC_IN_PIN1 = 18
POC_OUT_PIN = 19
def pulseOnChangeTest18AB():
    SW18B_UnitTest_globals.resetAll()

    pocPulseOnChange()
    pocPulseOnIncrease()
    pocPulseOnDecrease()
    pocPulseOnLessThanValue()
    pocPulseOnGreaterThanValue()
    pocPulseOnNotEqualValue()
    pocPulseOnPinsEqual()
    pocPulseOnPinsNotEqual()

def pocPulseOnChange():
    SW18B_UnitTest_globals.resetAll();
    pocInput1.attach(POC_IN_PIN1);
    pocInput1.writePublicData(0x8000);
    pocPin.begin(POC_OUT_PIN);
    SW18B_UnitTest_globals.initializePulseReaduS(POC_OUT_PIN);
    delay(1000)
    SW18B_UnitTest_globals.test("POC_POC_01", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 0)  # No Pulses So far
    pocPin.setEntryOnChange(0,POC_IN_PIN1);
    pocInput1.writePublicData(0x8001);
    delay(1000)
    SW18B_UnitTest_globals.test("POC_POC_02a", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 1);  # 1 change
    SW18B_UnitTest_globals.test("POC_POC_02b", SW18B_UnitTest_globals.pulseRead(POC_OUT_PIN), 50000,10000);  # Should be a 50 mS pulse


def pocPulseOnIncrease():
    pocPin.begin(POC_OUT_PIN);
    pocInput1.attach(POC_IN_PIN1);
    pocInput1.writePublicData(0x8000);
    SW18B_UnitTest_globals.initializePulseReaduS(POC_OUT_PIN);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_INC_01", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 0);  # No Pulses So far
    pocPin.setEntryOnIncrease(1,POC_IN_PIN1);
    pocInput1.writePublicData(0x7FFF);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_INC_02", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 0);  # No Pulses So far
    pocInput1.writePublicData(0x8000);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_INC_03", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 1);  # 1 change
    SW18B_UnitTest_globals.test("POC_INC_04", SW18B_UnitTest_globals.pulseRead(POC_OUT_PIN), 50000,10000);  # Should be a 50 mS pulse
    pocInput1.writePublicData(0xC000);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_INC_05", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 2);  # 2 changes
    SW18B_UnitTest_globals.test("POC_INC_06", SW18B_UnitTest_globals.pulseRead(POC_OUT_PIN), 50000,10000);  # Should be a 50 mS pulse

def pocPulseOnDecrease():

    pocPin.begin(POC_OUT_PIN,1,0,20);
    pocInput1.attach(POC_IN_PIN1);
    pocInput1.writePublicData(0x8000);
    SW18B_UnitTest_globals.initializePulseReaduS(POC_OUT_PIN);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_DEC_01", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 0);  # No Pulses So far
    pocPin.setEntryOnDecrease(1,POC_IN_PIN1);
    pocInput1.writePublicData(0xC000);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_DEC_02", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 0);  # No Pulses So far
    pocInput1.writePublicData(0x8000);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_DEC_03", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 1);  # 1 change
    SW18B_UnitTest_globals.test("POC_DEC_04", SW18B_UnitTest_globals.pulseRead(POC_OUT_PIN), 20000,5000);  # Should be a 20 mS pulse
    pocInput1.writePublicData(0x0000);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_DEC_05", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 2);  # 2 changes
    SW18B_UnitTest_globals.test("POC_DEC_06", SW18B_UnitTest_globals.pulseRead(POC_OUT_PIN), 20000,5000);  # Should be a 50 mS pulse

def pocPulseOnEqualValue():
    pocPin.begin(POC_OUT_PIN);
    pocInput1.attach(POC_IN_PIN1);
    pocInput1.writePublicData(0x8000);
    initializePulseReaduS(POC_OUT_PIN);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_EQV_01", pulseCounts(POC_OUT_PIN), 0);  # No Pulses So far
    pocPin.setEntryOnEqualValue(1,POC_IN_PIN1,0x1234);
    pocInput1.writePublicData(0xC000);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_EQV_02", pulseCounts(POC_OUT_PIN), 0);  # No Pulses So far
    pocInput1.writePublicData(0x1234);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_EQV_03", pulseCounts(POC_OUT_PIN), 10,3);  # 1 change
    SW18B_UnitTest_globals.test("POC_EQV_04", pulseRead(POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse
    pocInput1.writePublicData(0x0000);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_EQV_05", pulseCounts(POC_OUT_PIN), 10,3);  # 1 change
    pocInput1.writePublicData(0x1234);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_EQV_06", pulseCounts(POC_OUT_PIN), 20,6);  # 2 changes
    SW18B_UnitTest_globals.test("POC_EQV_07", pulseRead(POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse


def pocPulseOnLessThanValue():
    pocPin.begin(POC_OUT_PIN);
    pocInput1.attach(POC_IN_PIN1);
    pocInput1.writePublicData(0x8000);
    SW18B_UnitTest_globals.initializePulseReaduS(POC_OUT_PIN);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_LTV_01", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 0);  # No Pulses So far
    pocPin.setEntryOnLessThanValue(1,POC_IN_PIN1,0x1234);
    pocInput1.writePublicData(0xC000);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_LTV_02", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 0);  # No Pulses So far
    pocInput1.writePublicData(0x1233);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_LTV_03", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 10,3);  # 1 change
    SW18B_UnitTest_globals.test("POC_LTV_04", SW18B_UnitTest_globals.pulseRead(POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse
    pocInput1.writePublicData(0x6000);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_LTV_05", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 10,3);  # 1 change
    pocInput1.writePublicData(0x1234);
    delay(1000);
    pocInput1.writePublicData(0x6000);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_LTV_06", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 10,3);  # 1 change
    pocInput1.writePublicData(0x1000);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_LTV_07", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 20,6);  # 2 changes
    SW18B_UnitTest_globals.test("POC_LTV_08", SW18B_UnitTest_globals.pulseRead(POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse

def pocPulseOnGreaterThanValue():
    pocPin.begin(POC_OUT_PIN);
    pocInput1.attach(POC_IN_PIN1);
    pocInput1.writePublicData(0x0000);
    SW18B_UnitTest_globals.initializePulseReaduS(POC_OUT_PIN);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_GTV_01", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 0);  # No Pulses So far
    pocPin.setEntryOnGreaterThanValue(1,POC_IN_PIN1,0x1234);
    pocInput1.writePublicData(0x0000);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_GTV_02", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 0);  # No Pulses So far
    pocInput1.writePublicData(0x1235);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_GTV_03", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 10,3);  # 1 change
    SW18B_UnitTest_globals.test("POC_GTV_04", SW18B_UnitTest_globals.pulseRead(POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse
    pocInput1.writePublicData(0x0500);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_GTV_05", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 10,3);  # 1 change
    pocInput1.writePublicData(0x0500);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_GTV_06", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 10,3);  # 1 change
    pocInput1.writePublicData(0x6000);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_GTV_07", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 20,6);  # 2 changes
    SW18B_UnitTest_globals.test("POC_GTV_08", SW18B_UnitTest_globals.pulseRead(POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse


def pocPulseOnNotEqualValue():
    pocPin.begin(POC_OUT_PIN);
    pocInput1.attach(POC_IN_PIN1);
    pocInput1.writePublicData(0x1234);
    SW18B_UnitTest_globals.initializePulseReaduS(POC_OUT_PIN);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_NEV_01", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 0);  # No Pulses So far
    pocPin.setEntryOnNotEqualValue(1,POC_IN_PIN1,0x1234);

    pocInput1.writePublicData(0x1233);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_NEV_03", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 10,3);  # 1 change
    SW18B_UnitTest_globals.test("POC_NEV_04", SW18B_UnitTest_globals.pulseRead(POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse
    pocInput1.writePublicData(0x1234);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_NEV_05", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 10,3);  # 1 change
    pocInput1.writePublicData(0x1235);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_NEV_06", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 20,6);  # 2 changes
    SW18B_UnitTest_globals.test("POC_NEV_07", SW18B_UnitTest_globals.pulseRead(POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse

def pocPulseOnPinsEqual():
    pocPin.begin(POC_OUT_PIN);
    pocInput1.attach(POC_IN_PIN1);
    pocInput2.attach(POC_IN_PIN2);

    pocInput1.writePublicData(0x1234);
    pocInput2.writePublicData(0x1235);
    SW18B_UnitTest_globals.initializePulseReaduS(POC_OUT_PIN);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_EQP_01", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 0);  # No Pulses So far
    pocPin.setEntryOnPinsEqual(1,POC_IN_PIN1,POC_IN_PIN2);

    pocInput1.writePublicData(0x1235);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_EQP_03", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 10,3);  # 1 change
    SW18B_UnitTest_globals.test("POC_EQP_04", SW18B_UnitTest_globals.pulseRead(POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse
    pocInput1.writePublicData(0x1234);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_EQP_05", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 10,3);  # 1 change
    pocInput2.writePublicData(0x1234);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_EQP_06", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 20,6);  # 2 changes
    SW18B_UnitTest_globals.test("POC_EQP_07", SW18B_UnitTest_globals.pulseRead(POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse

def pocPulseOnPinsNotEqual():
    pocPin.begin(POC_OUT_PIN);
    pocInput1.attach(POC_IN_PIN1);
    pocInput2.attach(POC_IN_PIN2);

    pocInput1.writePublicData(0x1234);
    pocInput2.writePublicData(0x1234);
    SW18B_UnitTest_globals.initializePulseReaduS(POC_OUT_PIN);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_EQP_01", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 0);  # No Pulses So far
    pocPin.setEntryOnPinsNotEqual(1,POC_IN_PIN1,POC_IN_PIN2);

    pocInput1.writePublicData(0x1235);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_EQP_03", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 10,3);  # 1 change
    SW18B_UnitTest_globals.test("POC_EQP_04", SW18B_UnitTest_globals.pulseRead(POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse
    pocInput1.writePublicData(0x1234);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_EQP_05", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 10,3);  # 1 change
    pocInput2.writePublicData(0x1200);
    delay(1000);
    SW18B_UnitTest_globals.test("POC_EQP_06", SW18B_UnitTest_globals.pulseCounts(POC_OUT_PIN), 20,6);  # 2 changes
    SW18B_UnitTest_globals.test("POC_EQP_07", SW18B_UnitTest_globals.pulseRead(POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse
