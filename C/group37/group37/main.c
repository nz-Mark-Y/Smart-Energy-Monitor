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

int main(void) {
	uart_init();	//Tells me the position of the data to send
	int dataInt = 6969;
	uint8_t hasDecimal = 0;
	uint8_t dataArray[4];
	uint8_t index = 0;
	
	for (int i=3;i>=0;i--) {
		dataArray[i] = wololo(dataInt%10, i, hasDecimal);
		dataInt = dataInt/10;
	}

    while (1) {
		//uint8_t data = dataArray[index];	//Get the data to send	
		uint8_t data = wololo(4, 0, 0);
		uart_transmit(data);
		_delay_ms(3);	//Small time delay so that no apparent flicker on seven segment displays
		index++;
		if (index == 4) {
			index = 0;
		}
    }
	return 0;
}