# https://adventofcode.com/2022/day/15
from dataclasses import dataclass
from itertools import product
from adventutil.IntHelper import string_to_ints
from adventutil.DataImport import InputType
from adventutil.Day import Day

YEAR, DAY = 2022, 15

EXPECTED_A = 6425133
EXPECTED_B = 10996191429555
INPUT_TYPE = InputType.LIVE_DATA

manhattan_distance = lambda s, b: int(abs(s.real - b.real) + abs(s.imag - b.imag))

class Day15(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)

    def partA(self):
        scan_row = 2000000 if INPUT_TYPE == InputType.LIVE_DATA else 10

        blocked_positions, beacons_in_row = set(), set()

        for packet in self.build_packets():
            row_dist = int(abs(packet.s.imag - scan_row))

            x_offsets = packet.mhd - row_dist
            if x_offsets < 0:
                continue

            for block in range(-1*x_offsets, x_offsets + 1):
                blocked_positions.add(int(block + packet.s.real))

            if packet.b.imag == scan_row:
                beacons_in_row.add(packet.b)

        return len(blocked_positions) - len(beacons_in_row)

    def partB(self):
        print("Building packets")
        packets = self.build_packets()
        print("Building search set")
        search_locations = self.search_set(packets)
        print("Finding distress beacon")        
        return self.find_distress_beacon(packets, search_locations)

    @dataclass
    class Packet:
        s : complex
        b : complex
        mhd : int

    def build_packets(self):
        packets = []
        for line in self.lines:
            v = string_to_ints(line)
            s = complex(v[0],v[1])
            b = complex(v[2],v[3])
            p = Day15.Packet(s, b, manhattan_distance(s,b))
            packets.append(p)

        return packets

    def search_set(self, packets):
        max_dist = 4000000 if INPUT_TYPE == InputType.LIVE_DATA else 20

        search_locations = set()
        for index, packet in enumerate(packets):
            print(f"Searching Packet #{index+1}/{len(packets)}")
            search_dist = packet.mhd + 1

            for dy in range(-1*search_dist,search_dist+1):
                x_offset = search_dist - abs(dy)
                for dx in (-1*x_offset, x_offset): 
                    location = packet.s + complex(dx,dy)
                    if 0 <= location.real <= max_dist and 0 <= location.imag <= max_dist and abs(dy) + abs(dx) == search_dist:
                        search_locations.add(location)
        return search_locations

    def find_distress_beacon(self, packets, search_locations):
        for location in search_locations:
            valid = True
            for packet in packets:
                potential_mhd = manhattan_distance(packet.s, location)
                if potential_mhd <= packet.mhd:
                    valid = False
                    break
            if valid:
                return int(location.real * 4000000 + location.imag)

if __name__ == '__main__':
    Day15().run(INPUT_TYPE)