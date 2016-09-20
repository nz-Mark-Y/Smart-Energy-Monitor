library ieee;
use ieee.std_logic_1164.all; 
use ieee.numeric_std.all;
use ieee.std_logic_unsigned.all;

entity scounter is
	port (
	clk, en_S, reset_S: in std_logic;	--inputs
	s_count: out std_logic_vector (3 downto 0)	--output   
	);
end scounter;

architecture behaviour of scounter is
	signal s_count_temp: std_logic_vector(3 downto 0);
begin
	process (clk, reset_S)
	begin
		if (rising_edge(clk)) then
			if (reset_S='1') then --resets the value of the counter
				s_count_temp <=B"0000"; 			 
			elsif (en_S ='1') then
				s_count_temp <= s_count_temp + 1; 	--increments the counter 
			else
				s_count_temp <= s_count_temp;
			end if;
		end if;
	end process;
	s_count <= s_count_temp;
end behaviour;