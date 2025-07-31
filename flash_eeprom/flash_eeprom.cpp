/* 

program for the arduino to read messages over usb and use that to flash the eeprom
this only needs to be run once

*/

#define SHIFT_DATA 2
#define SHIFT_CLK 3
#define SHIFT_LATCH 4
#define EEPROM_D0 5
#define EEPROM_D7 12
#define WRITE_EN 13

/*
 * Output the address bits and outputEnable signal using shift registers.
 */
void setAddress(int address, bool outputEnable) {
  shiftOut(SHIFT_DATA, SHIFT_CLK, MSBFIRST, (address >> 8) | (outputEnable ? 0x00 : 0x80));
  shiftOut(SHIFT_DATA, SHIFT_CLK, MSBFIRST, address);

  digitalWrite(SHIFT_LATCH, LOW);
  digitalWrite(SHIFT_LATCH, HIGH);
  digitalWrite(SHIFT_LATCH, LOW);
}


/*
 * Read a byte from the EEPROM at the specified address.
 */
byte readEEPROM(int address) {
  for (int pin = EEPROM_D0; pin <= EEPROM_D7; pin += 1) {
    pinMode(pin, INPUT);
  }
  setAddress(address, /*outputEnable*/ true);

  byte data = 0;
  for (int pin = EEPROM_D7; pin >= EEPROM_D0; pin -= 1) {
    data = (data << 1) + digitalRead(pin);
  }
  return data;
}


/*
 * Write a byte to the EEPROM at the specified address.
 */
void writeEEPROM(int address, byte data) {
  setAddress(address, /*outputEnable*/ false);
  for (int pin = EEPROM_D0; pin <= EEPROM_D7; pin += 1) {
    pinMode(pin, OUTPUT);
  }

  for (int pin = EEPROM_D0; pin <= EEPROM_D7; pin += 1) {
    digitalWrite(pin, data & 1);
    data = data >> 1;
  }
  digitalWrite(WRITE_EN, LOW);
  delayMicroseconds(1);
  digitalWrite(WRITE_EN, HIGH);
  delay(10);
}


/*
 * Read the contents of the EEPROM and print them to the serial monitor.
 */
void printContents() {
  for (int base = 0; base <= 150; base += 16) {
    byte data[16];
    for (int offset = 0; offset <= 15; offset += 1) {
      data[offset] = readEEPROM(base + offset);
    }

    char buf[80];
    sprintf(buf, "%03x:  %02x %02x %02x %02x %02x %02x %02x %02x   %02x %02x %02x %02x %02x %02x %02x %02x",
            base, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],
            data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15]);

    Serial.println(buf);
  }
}


void setup() {
  // put your setup code here, to run once:
  // int n_bytes_to_write = sizeof(data);

  // Serial.print("Programming EEPROM");
  // for (int address = 0; address < n_bytes_to_write; address += 1) {
  //   writeEEPROM(address, data[address]);

  //   if (address % 64 == 0) {
  //     Serial.print(".");
  //   }
  // }
  // Serial.println(" done");


  pinMode(SHIFT_DATA, OUTPUT);
  pinMode(SHIFT_CLK, OUTPUT);
  pinMode(SHIFT_LATCH, OUTPUT);
  digitalWrite(WRITE_EN, HIGH);
  pinMode(WRITE_EN, OUTPUT);

  Serial.begin(57600);
  // // Read and print out the contents of the EERPROM




}


int address_write = 0;
int address_read = 0;
int reset_interrupt_idx = 0;

int read_idx = 0;

int size_low;
int size_high;

int start_address_low;
int start_address_high;

byte WRITE_CONFIRM = 10;

void loop() {

  
  
  int size = size_low + size_high * 256;
  
  
  


  if (Serial.available() > 0){

    byte input = Serial.read();
    
    if (read_idx == 0){
      Serial.write(input * 2);
    }else if (read_idx == 1){
      size_low = input;
      Serial.write(size_low);
    }else if (read_idx == 2){
      size_high = input;
      Serial.write(size_high);
    }
    else if (read_idx == 3){
      start_address_low = input;
      Serial.write(start_address_low);
    }else if (read_idx == 4){
      start_address_high = input;
      int start_address = start_address_high * 256 + start_address_low;
      address_write = start_address;
      address_read = start_address;
      Serial.write(start_address_high);
    }
    else if (reset_interrupt_idx < 6){
      writeEEPROM(0x7ffa+reset_interrupt_idx, input);
      byte current_value = readEEPROM(0x7ffa+reset_interrupt_idx);
      Serial.write(current_value);
      reset_interrupt_idx++;
    }else if (address_write < size){
      writeEEPROM(address_write, input);
      Serial.write(WRITE_CONFIRM);
      address_write++;
    }else if (address_read < size){
      byte response = readEEPROM(address_read);
      Serial.write(response);
      address_read++;
    }

    read_idx++;



  }
  

}