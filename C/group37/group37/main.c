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

volatile uint8_t counter = 0;

int main(void) {
	DDRB |= (1<<5);
	uart_init();	
	timer0_init();
	float floatArray[4] = { 420, 6969, 42, 96.69 };
	unsigned int floatIndex = 0;

	while(1) {
		float dataFloat = floatArray[floatIndex];
		unsigned int dataInt;
		uint8_t hasDecimal = 0;
		uint8_t dataArray[4];
		uint8_t index = 0;
		uint8_t decimalPos = 0;

		decimalPos = find_decimal(dataFloat);
		dataInt = (int)(dataFloat * pow(10, 3-decimalPos) + 0.5);

		for (int i=3;i>=0;i--) {
			if ((decimalPos == i) && ((3-decimalPos) > 0)) {
				hasDecimal = 1;
			} else {
				hasDecimal = 0;
			}
			dataArray[i] = wololo(dataInt%10, i, hasDecimal);
			dataInt = dataInt/10;
		}

		while (1) {
			uint8_t data = dataArray[index];	//Get the data to send	
			uart_transmit(data);
			_delay_ms(3);	//Small time delay so that no apparent flicker on seven segment displays
			index++;
			if (index == 4) {
				index = 0;
			}
			if(TCNT0>=211) {
				TCNT0 = 0;
				if (counter == 50) {
					counter = 0;
					PORTB |= (1<<5);
					break;
				} else {
					counter++;
				}
			}
		}
		if (floatIndex == 3) {
			floatIndex = 0;
		} else {
			floatIndex++;
		}
	}
	return 0;
}