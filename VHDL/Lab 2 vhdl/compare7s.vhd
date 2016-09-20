library ieee;
use ieee.std_logic_1164.all; 
use ieee.numeric_std.all;
use ieee.std_logic_unsigned.all;

entity compare7s is  
	port ( 
		s_count:	in std_logic_vector(3 downto 0);	--input
		cmp7_s:  out std_logic	--output
	);
end compare7s;

architecture behaviour of compare7s is
begin
	cmp7_s <= '1' when s_count= "0111" else '0';--cmp7_s is set to 1 whenever the input is equal to 7
end behaviour;