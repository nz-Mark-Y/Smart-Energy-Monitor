/*
 * functions37.c
 *
 * Created: 10/08/2016 9:26:53 PM
 * Author: mark_
 */ 
 #include <avr/io.h>
 #include "prototypes37.h"
 #define F_CPU 16000000UL
 #include <util/delay.h>

 //Initializes the UART
 void uart_init() {
	UBRR0H = 0;
	UBRR0L = 103;
	UCSR0B|= (1<<TXEN0);	//Sets the Transmit Enable to 1
	UCSR0C|= (1<<UCSZ00)|(1<<UCSZ01);	//Sets an 8-bit character
 }

 //Transmits the data
 void uart_transmit(uint8_t data) {
	while(!((1<<UDRE0) && UCSR0A));	//When UDRE0 is empty, put data value into buffer to be sent
		UDR0 = data;
 }

 void timer0_init() {
	TCCR0B |= (1<<CS00)|(1<<CS02);
	TCNT0 = 0;
 }

 unsigned int find_decimal(float data) {
	if (data < 10) { return 0; }
	if (data < 100) { return 1; }
	if (data < 1000) { return 2; }
	return 3;
 }

 //Converts our parameters into the value to send
 unsigned int wololo(uint8_t input, uint8_t position, uint8_t decimal) {
	unsigned int output = input;
	if (decimal == 1) { output += 16; }
	if (position == 0) { output += 96; }
	if (position == 1) { output += 64; }
	if (position == 2) { output += 32; }
	return output;
 }