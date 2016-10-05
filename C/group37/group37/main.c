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
	adc_init();
	uart_init();	
	timer0_init();
	uint32_t displayCount = 0;

	while(1) {
		uint8_t hasDecimal = 0;
		uint8_t dataArray[4];
		uint8_t index = 0;
		
		//Reading from the ADC, calculating and converting
		float voltageArray[20];
		float currentArray[20];
		for (int i=0;i<39;i++) {
			if (i%2 == 0) {
				unsigned int adcValue = adc_read_voltage();
				float adcVoltage = adc_calculation(adcValue);
				float voltage = voltage_real(adcVoltage, 0);
				voltageArray[i/2] = voltage;
			} else {
				unsigned int adcValue = adc_read_current(0); // Regular Current
				float adcCurrent = adc_calculation(adcValue);
				float current = voltage_real(adcCurrent, 1); // Regular Current
				currentArray[(i-1)/2] = current;
			}
		}
		float power = calcPower(&voltageArray, &currentArray);
		/*
		if ((displayCount%10 < 4) && (displayCount%10 > 0)) { float dataFloat = power; } 
		else if ((displayCount%10 < 7) && (displayCount%10 > 3)) { float dataFloat = power; }
		else if (displayCount%10 > 7) { float dataFloat = power;}
		else { float dataFloat = 0; }
		*/
		float dataFloat;
		dataFloat = roundf(dataFloat * 100) / 100;
		uint8_t decimalPos = find_decimal(dataFloat); //Find the decimal place
		unsigned int dataInt = (int)(dataFloat * pow(10, 2-decimalPos) + 0.5); //Convert to decimal for array conversion
		
		//Splits the integer into an array of 4 integers, each represents the value of a digit, the position of that digit, and if it has a decimal place
		for (int i=2;i>=0;i--) {
			if ((decimalPos == i) && ((2-decimalPos) > 0)) {
				hasDecimal = 1;
			} else {
				hasDecimal = 0;
			}
			dataArray[i] = wololo(dataInt%10, i, hasDecimal);
			dataInt = dataInt/10;
		}
		if ((displayCount%10 < 4) && (displayCount%10 > 0)) { dataArray[3] = 15; }
		else if ((displayCount%10 < 7) && (displayCount%10 > 3)) { dataArray[3] = 15; }
		else if (displayCount%10 > 7) { dataArray[3] = 15; }
		else { dataArray[3] = 12; }

		//Transmits data until we get TCNT0 = 191 fifty times 
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