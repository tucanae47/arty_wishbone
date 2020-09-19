import argparse
import importlib
from nmigen_boards.arty_a7 import *
from nmigen import *
from nmigen_soc import wishbone
from uartbridge import UARTBridge
from lambdasoc.periph.sram import SRAMPeripheral


__all__ = ["ArtyWB"]


class ArtyWB(Elaboratable):
    def __init__(self, *,
                 ram_addr, ram_size,
                 uart_addr, uart_divisor, uart_pins):
        self._arbiter = wishbone.Arbiter(addr_width=30, data_width=32, granularity=8)
        self._decoder = wishbone.Decoder(addr_width=30, data_width=32, granularity=8, features={"cti", "bte"})
        
        self.ram = SRAMPeripheral(size=ram_size)
        self._decoder.add(self.ram.bus, addr=ram_addr)
        self.bridge = UARTBridge(divisor=uart_divisor, pins=uart_pins)
        

    def elaborate(self, platform):
        m = Module()
        m.submodules.arbiter = self._arbiter
        m.submodules.decoder = self._decoder
        m.submodules.ram     = self.ram
        m.submodules.bridge = self.bridge

        m.d.comb += [
            self.bridge.bus.connect(self._decoder.bus),
            self._arbiter.bus.connect(self._decoder.bus)
        ]

        return m


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("platform", type=str,
            help="target platform (e.g. '')")
    parser.add_argument("--baudrate", type=int,
            default=9600,
            help="UART baudrate (default: 9600)")

    args = parser.parse_args()

    platform = ArtyA7Platform()
    uart_divisor = int(platform.default_clk_frequency // args.baudrate)
    uart_pins = platform.request("uart", 0)

    soc = ArtyWB(ram_addr=0x00004000, ram_size=0x1000,
          uart_addr=0x00005000, uart_divisor=uart_divisor, uart_pins=uart_pins,
    )

    platform.build(soc, do_program=True)
    
