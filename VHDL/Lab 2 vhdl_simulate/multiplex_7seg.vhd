library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.std_logic_arith.all;

entity multiplex_7seg is
	port (
		clk  : in std_logic;
		bcd : in std_logic_vector(7 downto 0);
		decimal_point : out std_logic;
		single_digit : out std_logic_vector (3 downto 0)
	);
end multiplex_7seg;

architecture behaviour of multiplex_7seg is
	signal seg_num : std_logic_vector(1 downto 0);
	begin
			process(bcd,clk)
				begin
					seg_num(1 downto 0) <= bcd(6 downto 5);
					if ((clk'event) and (clk = '1')) then	
							decimal_point <= bcd(4);
							case seg_num is
								when "00"=> single_digit <="0001";
								when "01"=> single_digit <="0010";
								when "10"=> single_digit <="0100";
								when "11"=> single_digit <="1000";
								
								when others=> single_digit <="0000";
							end case;
					end if;
			end process;
end behaviour;		
			
	