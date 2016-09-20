library ieee;
use ieee.std_logic_1164.all; 
use ieee.numeric_std.all;
use ieee.std_logic_unsigned.all;

entity bcounter is
	port (
	clk, en_N, reset_N: in std_logic;	--input
	b_count: out std_logic_vector (3 downto 0) --output  
	);
end bcounter;

architecture behaviour of bcounter is
	signal b_count_temp: std_logic_vector(3 downto 0);
begin
	process (clk, reset_N)
	begin
		if (rising_edge(clk)) then
			if (reset_N='1') then
				b_count_temp <=B"0000"; 	--resets the counter		 
			elsif (en_N ='1') then
				b_count_temp <= b_count_temp + 1; --increments the counter	 
			else
				b_count_temp <= b_count_temp;
			end if;
		end if;
	end process;
	b_count <= b_count_temp;
end behaviour;