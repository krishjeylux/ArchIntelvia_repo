
`timescale 1ns/1ps

module tb_memory_controller;

reg clk;
reg rst;
reg read_en;
reg write_en;
reg [9:0] addr;
reg [31:0] write_data;

wire [31:0] read_data;

// DUT
memory_controller dut (
    .clk(clk),
    .rst(rst),
    .read_en(read_en),
    .write_en(write_en),
    .addr(addr),
    .write_data(write_data),
    .read_data(read_data)
);

// Clock generation
initial clk = 0;
always #5 clk = ~clk;

// Stimulus
initial begin
    $dumpfile("wave.vcd");
    $dumpvars(0, tb_memory_controller);

    rst = 1;
    read_en = 0;
    write_en = 0;
    addr = 0;
    write_data = 0;

    #10 rst = 0;

    // Write
    #10;
    write_en = 1;
    addr = 5;
    write_data = 32'hA5A5;

    #10 write_en = 0;

    // Read
    #10;
    read_en = 1;
    addr = 5;

    #10;
    $display("Read Data: %h", read_data);

    #20;
    $finish;
end

endmodule
