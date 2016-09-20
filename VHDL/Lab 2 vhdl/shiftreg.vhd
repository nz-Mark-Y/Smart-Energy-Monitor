library ieee;
use ieee.std_logic_1164.all; 
use ieee.numeric_std.all;
use ieee.std_logic_unsigned.all;

entity shiftreg is
	port (
	clk, Rx, en_SHIFT: in std_logic;	--inputs
	output_8bit: out std_logic_vector (7 downto 0) --output  
	);
end shiftreg;

architecture behaviour of shiftreg is
	signal output_8bit_temp: std_logic_vector(7 downto 0);
begin
	process (clk)
	begin
		if clk'event and clk='1' then              
			if en_SHIFT='1' then --if en_SHIFT is equal to 1, shift the input bit Rx into the register               
				output_8bit_temp <= Rx & output_8bit_temp(7 downto 1);     
			end if;
		end if;
	end process;
	output_8bit <= output_8bit_temp;
end behaviour;