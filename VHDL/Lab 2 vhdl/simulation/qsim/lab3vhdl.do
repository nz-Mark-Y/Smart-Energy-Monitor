onerror {quit -f}
vlib work
vlog -work work lab3vhdl.vo
vlog -work work lab3vhdl.vt
vsim -novopt -c -t 1ps -L max7000ae_ver -L altera_ver -L altera_mf_ver -L 220model_ver -L sgate work.lab3vhdl_vlg_vec_tst
vcd file -direction lab3vhdl.msim.vcd
vcd add -internal lab3vhdl_vlg_vec_tst/*
vcd add -internal lab3vhdl_vlg_vec_tst/i1/*
add wave /*
run -all
