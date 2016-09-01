/*
 * group37.c
 *
 * Created: 10/088/2016 1:50:56 PM
 * Author: mark_
 */ 
#include <avr/io.h>
#include <math.h>
#include "prototypes37.h"
#define F_CPU 16000000UL
#include <util/delay.h>

volatile uint8_t counter = 0; //Counter for the number of times the TCNT0 compares correctly

int main(void) {
	uart_init();	
	timer0_init();
	float floatArray[4] = { 1234, 1235, 1236, 1237 }; //Array of values to send
	unsigned int floatIndex = 0;

	while(1) {
		float dataFloat = floatArray[floatIndex]; //Select the value to send
		unsigned int dataInt;
		uint8_t hasDecimal = 0;
		uint8_t dataArray[4];
		uint8_t index = 0;
		uint8_t decimalPos = 0;

		decimalPos = find_decimal(dataFloat); //Find the decimal place
		dataInt = (int)(dataFloat * pow(10, 3-decimalPos) + 0.5); //Convert to decimal for array conversion
		
		//Splits the integer into an array of 4 integers, each represents the value of a digit, the position of that digit, and if it has a decimal place
		for (int i=3;i>=0;i--) {
			if ((decimalPos == i) && ((3-decimalPos) > 0)) {
				hasDecimal = 1;
			} else {
				hasDecimal = 0;
			}
			dataArray[i] = wololo(dataInt%10, i, hasDecimal);
			dataInt = dataInt/10;
		}

		//Transmits data until we get TCNT0 = 191 twenty times 
		while (1) {
			uint8_t data = dataArray[index];	//Get the integer to send	
			uart_transmit(data);
			_delay_ms(3);	//Small time delay so that no apparent flicker on seven segment displays
			index++;
			//Select next integer to send
			if (index == 4) {
				index = 0;
			}
			//Polling mechanism
			if(TCNT0>=211) {
				TCNT0 = 0;
				if (counter == 50) {
					counter = 0;
					break;
				} else {
					counter++;
				}
			}
		}
		//Select next float to send
		if (floatIndex == 3) { 
			floatIndex = 0;
		} else {
			floatIndex++;
		}
	}
	return 0;
}