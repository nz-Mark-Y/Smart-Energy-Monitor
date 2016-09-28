/*
 * group37.c
 *
 * Created: 10/088/2016 1:50:56 PM
 * Author: mark_
 */ 
#include <avr/io.h>
#include "prototypes37.h"
#define F_CPU 16000000UL

volatile uint8_t counter = 0; //Counter for the number of times the TCNT0 compares correctly

int main(void) {	
	timer0_init();
	DDRB |= (1<<PORTB5);

	while (1) {	
		
		if(TCNT0>=156) {
			TCNT0 = 0;
			if (counter == 100) {
				counter = 0;
				PORTB ^= (1<<5);
				break;
			} else {
				counter++;
			}	
		}
	}
	return 0;
}