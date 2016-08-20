library ieee;
use ieee.std_logic_1164.all; 
use ieee.numeric_std.all;
use ieee.std_logic_unsigned.all;

entity compare15s is  
	port ( 
		s_count:	in std_logic_vector(3 downto 0);
		cmp15_s:  out std_logic
	);
end compare15s;

architecture behaviour of compare15s is
begin
	cmp15_s <= '1' when s_count= "1111" else '0';
end behaviour;