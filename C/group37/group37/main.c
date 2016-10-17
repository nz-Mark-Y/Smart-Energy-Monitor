/*
 * group37.c
 *
 * Created: 10/088/2016 1:50:56 PM
 * Author: mark
 *
 * Apologies for the terrible variable and function names
 */ 
#include <avr/io.h>
#include <avr/interrupt.h>
#include <math.h>
#define F_CPU 16000000UL
#define maxPower 6.97
#include <util/delay.h>
#include "prototypes37.h"

volatile uint8_t counter = 0; //Counter for the number of times the TCNT0 compares correctly
volatile uint8_t flag = 0; // Flag for zero crossing detector
volatile float oldVoltage = 0;

int main(void) {
	sei();
	adc_init();
	uart_init();	
	timer0_init();
	timer1_init();
	int_init();
	DDRB |= (1<<5);
	uint32_t displayCount = 0;
	uint8_t currentFlag = 1;

	while(1) {
		uint8_t hasDecimal = 0;
		uint8_t dataArray[4];
		uint8_t index = 0;
		float dataFloat = 0;
		
		flag = 0;
		while (flag == 0); // Wait for the zero crossing detector to signal a rising zero crossing
		
		// Reading from the ADC, calculating and converting
		float voltageArray[10];
		float currentArray[10];
		for (int i=0;i<19;i++) { // Alternate reading voltage and current
			if (i%2 == 0) {
				unsigned int adcValue = adc_read_voltage();
				float adcVoltage = adc_calculation(adcValue);
				float voltage = voltage_real(adcVoltage, 0);
				voltageArray[i/2] = voltage;
			} else {
				unsigned int adcValue = adc_read_current(currentFlag); 
				float adcCurrent = adc_calculation(adcValue);
				float current = voltage_real(adcCurrent, currentFlag+1); 
				currentArray[(i-1)/2] = current;
			}
		}
		float test = calcCurrentRMS(&currentArray);
		if (test > 0.22) {
			if (currentFlag != 0) {
				currentFlag = 0; // Set the flag to regular amplifier
				continue;
			}
		} else if (test < 0.2) { // Hysteresis
			if (currentFlag != 1) {
				currentFlag = 1; // Set the flag to high gain amplifier
				continue;
			}
		}
		
		if ((displayCount%10 < 4) && (displayCount%10 >= 0)) { 
			dataFloat = calcPower(&voltageArray, &currentArray) * 1.29; // Display average power
			if (dataFloat >= maxPower*0.75) {
				OCR1A = 0x001; // Flash constantly
			} else if ((dataFloat < maxPower*0.75 ) && (dataFloat >= maxPower*0.5)) { 
				OCR1A = 0xA2C; // Flash 3 times per second
			} else if ((dataFloat < maxPower*0.5 ) && (dataFloat >= maxPower*0.25)) { 
				OCR1A = 0xF42; // Flash 2 times per second
			} else { 
				OCR1A = 0x1E84; // Flash once per second
			} 
		} 
		else if ((displayCount%10 < 7) && (displayCount%10 > 3)) { 
			dataFloat = calcCurrentRMS(&currentArray) * sqrt(2); // Display peak current
			if (currentFlag == 0) {
				dataFloat = dataFloat * 1.09;
			}
		} else if (displayCount%10 > 6) { 
			float dataFloatOne = calcVoltageRMS(&voltageArray) * 1.11; // Display rms voltage
			dataFloat = (dataFloatOne + oldVoltage) / 2; 
			oldVoltage = dataFloatOne;
		} 

		dataFloat = roundf(dataFloat * 100) / 100;
		uint8_t decimalPos = find_decimal(dataFloat); //Find the decimal place
		unsigned int dataInt = (int)(dataFloat * pow(10, 2-decimalPos) + 0.5); //Convert to decimal for array conversion
		
		// Splits the integer into an array of 4 integers, each represents the value of a digit, the position of that digit, and if it has a decimal place
		for (int i=2;i>=0;i--) {
			if ((decimalPos == i) && ((2-decimalPos) > 0)) {
				hasDecimal = 1;
			} else {
				hasDecimal = 0;
			}
			dataArray[i] = wololo(dataInt%10, i, hasDecimal);
			dataInt = dataInt/10;
		}
		
		if ((displayCount%10 < 4) && (displayCount%10 >= 0)) { 
			dataArray[3] = 15; // Unit P
		} else if ((displayCount%10 < 7) && (displayCount%10 > 3)) { 
			dataArray[3] = 13; // Unit I
		} else if (displayCount%10 > 6) { 
			dataArray[3] = 14; // Unit V
		} 

		// Transmits data until we get TCNT0 = 191 fifty times (i.e 500ms for each transmission)
		while (1) {
			uint8_t data = dataArray[index]; // Get the integer to send	
			uart_transmit(data);
			_delay_ms(3); // Small time delay so that no apparent flicker on seven segment displays
			index++;
			// Select next integer to send
			if (index == 4) {
				index = 0;
			}
			// Polling mechanism
			if(TCNT0>=156) {
				TCNT0 = 0;
				if (counter == 50) {
					counter = 0;
					break;
				} else {
					counter++;
				}
			}
		}
		displayCount++;
	}
	return 0;
}

ISR (INT0_vect) {
	flag = 1; 
}

ISR (TIMER1_COMPA_vect) {
	PORTB ^= (1<<5); // Toggle the LED
}