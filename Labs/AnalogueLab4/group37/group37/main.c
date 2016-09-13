/*
 * group37.c
 *
 * Created: 10/088/2016 1:50:56 PM
 * Author: mark_
 */ 
#include <avr/io.h>
#include "prototypes37.h"
#define F_CPU 16000000UL
#include <util/delay.h>

int main(void) {
	uart_init();	
	unsigned int dataInt = 6969;
	uint8_t dataArray[4];
	uint8_t index = 0;
		
	for (int i=0;i<4;i++) {
		dataArray[i] = wololo(dataInt%10, i, 0);
	}
	while (1) {
		uint8_t data = dataArray[index];	//Get the integer to send	
		uart_transmit(data);
		_delay_ms(2);	//Small time delay so that no apparent flicker on seven segment displays
		index++;
		//Select next integer to send
		if (index == 4) {
			index = 0;
		}
	}
}