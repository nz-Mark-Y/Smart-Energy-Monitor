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
	uint8_t dataInt = 102;

	while (1) {	
		uart_transmit(dataInt);
		_delay_ms(2);	
	}
}