library ieee;
use ieee.std_logic_1164.all;

entity disp_register is
port(
	D : in std_logic_vector(7 downto 0);
	load, clk : in std_logic;
	Q: out std_logic_vector(7 downto 0)
); end disp_register;

architecture Behaviour of disp_register is 

begin
	process (clk)
	begin
		if clk'event and clk = '1' then
			if load = '1' then
				Q <= D;
			end if;	
		end if;
	end process;
end Behaviour;	
