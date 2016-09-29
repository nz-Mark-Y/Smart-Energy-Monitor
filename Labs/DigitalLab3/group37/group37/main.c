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
#include <avr/interrupt.h>

volatile uint16_t countCheck = 1; 

int main(void) {
	sei();	
	timer0_init();
	DDRB |= (1<<5);
	DDRB &= ~(1<<7);
	
	PORTB &= ~(1<<5);

	while (1) {	
		if (PINB & (1<<PORTB7)) {
			
		} else {
			if (countCheck == 1) {
				countCheck = 2;
				OCR1A = 0x7C6A;
			} else {
				countCheck = 1;
				OCR1A = 0x3D08;
			}
			_delay_ms(100);
		}

		/* 
		if (TCNT0 >= 156) {
			TCNT0 = 0;
			if (counter == 100) {
				PORTB ^= (1<<5);
				counter = 0;	
			} else {
				counter++;
			}
		}
		*/
	}
	return 0;
}

ISR (TIMER1_COMPA_vect) {
	PORTB ^= (1<<5);
}