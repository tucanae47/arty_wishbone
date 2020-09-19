# arty_wishbone WIP

Nmigen wishbone with arty a7

# Uart serial bridge

`uartbride.py` was taken from [gram project](https://github.com/jeanthom/gram/blob/master/examples/uartbridge.py)


# usage
after synthesys and programming you should be able to user wishbone-tool

* `pip install -r requirements`
* `python arty_wb.py --baudrate=9600 nmigen_boards.arty_a7.ArtyA7Platfor`
* ` wishbone-tool --serial /dev/ttyUSB1 0x00005000`


# goal
modify memory from fpga memory from wishbone tool
write tests
write tutorial 
