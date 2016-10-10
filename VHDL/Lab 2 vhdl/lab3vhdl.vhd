library ieee;
use ieee.std_logic_1164.all;

entity fsm is
	port ( 
		Rx, B, S7, S15, clk: in std_logic; --inputs
		reset : in std_logic;
		Sen, Ben, Sr, Br, B_shift: out std_logic; --outputs
		control_disp : out std_logic --controls when output from the shift register is loaded into the seven seg decoder and the (decimal point & position) decoder via the parallel load disp_register
		);
		
end fsm;

architecture behaviour of fsm is
	type my_states is(idle, start, data, stop);
	signal CS, NS: my_states:= idle;
	begin	
		synchronous_process: process(clk)
		begin	
			if rising_edge(clk) then	--on the rising clock edge transition to the next state
				CS <= NS;
			end if;

		end process;
		next_state_logic: process(CS, Rx, B, S7, S15)
		begin
			case CS is 
				when idle =>	--idle state
					if Rx = '0' then	--if the value of the input Rx signal changes to 0, transition to the start state, otherwise remain in the idle state
						NS <= start;
					else
						NS <= idle;
					end if;
				when start =>	--start state
					if S7 = '1' then --Once the s counter reaches 7, transition to the data state 
						NS <= data;
					else
						NS <= start; 
					end if;
				when data =>	--data state
					if ((B = '1') and (S15 = '1')) then	--once the s count reaches 15 and the bit counter reaches 7, transition to the stop state, otherwise keep sampling data.
						NS <= stop;
					else
						NS <= data;
					end if;
				when stop =>	--stop state
					if S15 = '0' then --if the s counter reaches 15, transition to the idle state
						NS <= stop;
					else
						NS <= idle;
					end if;
			end case;
		end process;
		output_logic: process(CS, Rx, B, S7, S15)
		begin
		
		Sen <= '0';
		Sr <= '0';
		Ben <= '0';
		B_shift <= '0';
		Br <= '0';
		control_disp <= '0';
			case CS is
				when idle =>
					if Rx = '0' then	
						Sr <= '1'; --reset the s counter						
					else						
						Sr <= '0';						
					end if;
					control_disp <= '0';
					
				when start =>
					if S7 = '1' then					
						Sr <= '1';	--once the s counter reaches 7 (the s counter is reset) it indicates that the middle of the transmission bit has been reached 
						Br <= '1'; 	--reset the b counter					
					else 					
						Sen <= '1'; --increment the s counter						
					end if;
					control_disp <= '0';
								
				when data =>					
					if ((B = '1') AND (S15 = '1')) then	--When the sampling counter reaches  15 and the bit counter reaches 7, we know that 					
						Sr <= '1';
						B_shift <= '1';						
					elsif ((B = '0') AND (S15 = '1')) then	--When the sampling counter reaches  15 we know we are at the middle of the data bit				
						B_shift <= '1'; --enable shift register so that we capture the Rx input
						Sr <= '1';
						Ben <= '1';	--Increment the bit counter						
					else					
						Sen <= '1';						
					end if;
					control_disp <= '0';
					
				when stop =>
					if S15 = '0' then						
						Sen <= '1';						
					else						
						Sen <= '0';						
					end if;
					control_disp <= '1';	--Data loaded into seven seg only at stop state so as to prevent ghosting in the output
			end case;
		end process;
end architecture;
