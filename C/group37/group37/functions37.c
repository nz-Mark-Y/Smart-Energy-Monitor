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

 //Initializes the timer
 void timer0_init() {
	TCCR0B |= (1<<CS00)|(1<<CS02); //Prescaler of 1024
	TCNT0 = 0; //Initialize timer0
 }
 
 //Finds the decimal place in the float
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

 //Calculates power from a voltage array and a current array
 float calcPower(float (*voltage)[20], float (*current)[20]) {
	float power = 0;
	float newVoltage[39];
	float newCurrent[39];
	for (int i=0;i<39;i++) {
		if (i%2 == 0) {
			newVoltage[i] = (*voltage)[i/2];
			if ((i == 0) || (i == 38)) {
				newCurrent[i] = (*current)[i/2];
			} else {
				newCurrent[i] = linearApproximate((*current)[((i+1)/2)-1], (*current)[((i+1)/2)-2]);
			}
		} else {
			newVoltage[i] = linearApproximate((*voltage)[(i+1)/2], (*voltage)[((i+1)/2)-1]);
			newCurrent[i] = (*current)[(i-1)/2];
		}
	}
	for (int i=0;i<39;i++) {
		power = power + newVoltage[i]*newCurrent[i];
	}
	power = power / 39;
	return power;
 }

 //Approximates a data value based on the two nearest data points
 float linearApproximate(float higher, float lower) {
	float approximation = (higher + lower) / 2;
	return approximation;
 }

 //Initialises the ADC
 void adc_init() {
	DDRC = 0x00; //Set port c as input
	ADCSRA |= (1<<ADPS0)|(1<<ADPS1)|(1<<ADPS2)|(1<<ADEN); //Set Prescaler to 128 and enable the ADC 
 }

 unsigned int adc_read_1() {
	ADCSRA |= (1<<ADSC);
	while ((ADCSRA & (1<<ADIF)) == 0);
	unsigned int adcRead = ADC;
	return adcRead;
 }

 unsigned int adc_read_2() {
	return 0;
 }

 float adc_calculation(unsigned int adcValue) {
	float calculatedValue;
	calculatedValue = (adcValue / 1000) * 3.3;
	return calculatedValue; 
 }