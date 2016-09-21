/*
 * prototypes37.h
 *
 * Created: 10/08/2016 9:26:42 PM
 * Author: mark_
 */
#include <avr/io.h> 
#ifndef PROTOTYPES37_H_
#define PROTOTYPES37_H_

void uart_init();
void uart_transmit(uint8_t data);
void timer0_init();
unsigned int find_decimal(float data); 
unsigned int wololo(uint8_t input, uint8_t position, uint8_t decimal);
float calcPower(float (*voltage)[20], float (*current)[20]);
float linearApproximate(float higher, float lower);
void adc_init();
unsigned int adc_read_polling();
unsigned int adc_read_interrupt();
float adc_calculation(unsigned int adcValue);

#endif /* PROTOTYPES37_H_ */