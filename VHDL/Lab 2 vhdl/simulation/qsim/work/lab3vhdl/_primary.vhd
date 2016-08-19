library verilog;
use verilog.vl_types.all;
entity lab3vhdl is
    port(
        decimal_point   : out    vl_logic;
        clk             : in     vl_logic;
        rx              : in     vl_logic;
        segment7        : out    vl_logic_vector(6 downto 0);
        single_digit    : out    vl_logic_vector(3 downto 0)
    );
end lab3vhdl;
