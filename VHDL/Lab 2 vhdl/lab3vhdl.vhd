library ieee;
use ieee.std_logic_1164.all;

entity fsm is
	port ( 
		Rx, B, S7, S15, clk: in std_logic;
		reset : in std_logic;
		Sen, Ben, Sr, Br, B_shift: out std_logic; 
		control_disp : out std_logic
		);
		
end fsm;

architecture behaviour of fsm is
	type my_states is(idle, start, data, stop);
	signal CS, NS: my_states:= idle;
	begin	
		synchronous_process: process(clk)
		begin	
			if rising_edge(clk) then
				CS <= NS;
			end if;

		end process;
		next_state_logic: process(CS, Rx, B, S7, S15)
		begin
			case CS is 
				when idle =>
					if Rx = '0' then
						NS <= start;
					else
						NS <= idle;
					end if;
				when start =>
					if S7 = '1' then  
						NS <= data;
					else
						NS <= start; 
					end if;
				when data =>
					if ((B = '1') and (S15 = '1')) then
						NS <= stop;
					else
						NS <= data;
					end if;
				when stop =>
					if S15 = '0' then
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
						Sr <= '1';						
					else						
						Sr <= '0';						
					end if;
					control_disp <= '0';
					
				when start =>
					if S7 = '1' then					
						Sr <= '1'; 
						Br <= '1'; 						
					else 					
						Sen <= '1';						
					end if;
					control_disp <= '0';
								
				when data =>					
					if ((B = '1') AND (S15 = '1')) then					
						Sr <= '1';
						B_shift <= '1';						
					elsif ((B = '0') AND (S15 = '1')) then					
						B_shift <= '1';
						Sr <= '1';
						Ben <= '1';						
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
					control_disp <= '1';
			end case;
		end process;
end architecture;
