library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.std_logic_arith.all;

entity multiplex_7seg is
	port (
		clk  : in std_logic;	--inputs
		bcd : in std_logic_vector(7 downto 0);
		decimal_point : out std_logic;	--outputs
		single_digit : out std_logic_vector (3 downto 0)
	);
end multiplex_7seg;

architecture behaviour of multiplex_7seg is
	signal seg_num : std_logic_vector(1 downto 0);
	begin
			process(bcd,clk)
				begin
					seg_num(1 downto 0) <= bcd(6 downto 5);--extracts the part of the UART data frame that dictates which of the 7-segment displays is to be turned on
					if ((clk'event) and (clk = '1')) then	
							decimal_point <= bcd(4); --determines if decimal point led will be on or off
							case seg_num is	--depending on the value of seg_num, one of the 4 7-segment displays will be turned on
								when "00"=> single_digit <="0001";
								when "01"=> single_digit <="0010";
								when "10"=> single_digit <="0100";
								when "11"=> single_digit <="1000";
								
								when others=> single_digit <="0000";
							end case;
					end if;
			end process;
end behaviour;		
			
	