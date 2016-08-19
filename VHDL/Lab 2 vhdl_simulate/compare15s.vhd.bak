library ieee;
use ieee.std_logic_1164.all; 
use ieee.numeric_std.all;
use ieee.std_logic_unsigned.all;

entity compare7n is  
	port ( 
		b_count:	in std_logic_vector(3 downto 0);
		cmp7_n:  out std_logic
	);
end compare7n;

architecture behaviour of compare7n is
begin
	cmp7_n <= '1' when b_count= "0111" else '0';
end behaviour;