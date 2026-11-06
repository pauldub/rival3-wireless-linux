# Pair a SteelSeries Rival 3 Wireless on Linux

This Python 3 script pairs the original Rival 3 Wireless with its 2.4 GHz USB receiver (`1038:1830`). Tested on Linux with that receiver. It uses the Linux `hidraw` interface and requires no Python packages.

1. Plug in the receiver and switch the mouse off.
2. Run `sudo python3 pair-rival3.py --pair` from this directory.
3. When the script says the report was sent, hold the CPI button behind the scroll wheel and flip the mouse switch to **2.4 GHz**.
4. Move the mouse to test it, or run `sudo python3 pair-rival3.py --status`. RF status `4` means connected.

The script selects the receiver's vendor HID interface (usage page `0xffc0`, usage `0x0001`). The pairing report is 65 bytes including the report ID, beginning with `00 71 00` and padded with zeros. The command comes from the original Rival 3 Wireless descriptor bundled with SteelSeries GG. The script targets the original receiver only.
