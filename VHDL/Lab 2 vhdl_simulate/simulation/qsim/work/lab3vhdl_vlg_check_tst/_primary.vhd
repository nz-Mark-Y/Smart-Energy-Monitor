library verilog;
use verilog.vl_types.all;
entity lab3vhdl_vlg_check_tst is
    port(
        decimal_point   : in     vl_logic;
        segment7        : in     vl_logic_vector(6 downto 0);
        single_digit    : in     vl_logic_vector(3 downto 0);
        sampler_rx      : in     vl_logic
    );
end lab3vhdl_vlg_check_tst;
