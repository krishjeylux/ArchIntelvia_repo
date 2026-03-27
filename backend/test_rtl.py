from rtl.testbench import generate_testbench

params = {
    "DATA_WIDTH": 32,
    "ADDR_WIDTH": 10
}

tb = generate_testbench(params)

print(tb)