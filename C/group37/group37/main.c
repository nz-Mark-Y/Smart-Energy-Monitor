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
	//Power Calculations
	float voltage[20] = { 1.65, 2.03, 2.38, 2.65, 2.81, 2.85, 2.76, 2.55, 2.25, 1.89, 1.50, 1.12, 0.81, 0.578, 0.46, 0.47, 0.61, 0.851, 1.15, 1.56 };
	float current[20] = { 1.81, 2.12, 2.38, 2.56, 2.64, 2.62, 2.50, 2.29, 2.01, 1.69, 1.36, 1.07, 0.84, 0.69, 0.65, 0.71, 0.87, 1.11, 1.41 };
	float power = calcPower(&voltage, &current);
	power = roundf(power * 1000) / 1000;
	//-----------------

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