library ieee;
use ieee.std_logic_1164.all; 
use ieee.numeric_std.all;
use ieee.std_logic_unsigned.all;

entity compare15s is  
	port ( 
		s_count:	in std_logic_vector(3 downto 0);	--input
		cmp15_s:  out std_logic	--output
	);
end compare15s;

architecture behaviour of compare15s is
begin
	cmp15_s <= '1' when s_count= "1111" else '0';	--cmp15_s is set to 1 whenever the input is equal to 15
end behaviour;