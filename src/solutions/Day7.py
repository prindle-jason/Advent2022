# https://adventofcode.com/2022/day/7
from adventutil.DataImport import InputType
from adventutil.Day import Day

YEAR, DAY = 2022, 7

EXPECTED_A = 1583951
EXPECTED_B = 214171
INPUT_TYPE = InputType.SAMPLE_DATA

class Day7(Day):
    def __init__(self):
        super().__init__(YEAR, DAY, EXPECTED_A, EXPECTED_B)
        self.file_system = None
        self.directory_sizes = None

    def partA(self):
        #lines = readLines(YEAR, DAY)

        self.file_system, self.directory_sizes = dict(), dict()

        self.build_file_system(self.lines)
        self.build_directory_sizes('')

        return sum([v for v in self.directory_sizes.values() if v <= 100000])


    def partB(self):
        #lines = readLines(YEAR, DAY)

        self.file_system, self.directory_sizes = dict(), dict()

        self.build_file_system(self.lines)
        self.build_directory_sizes('')

        size_list = list(self.directory_sizes.values())
        size_list.sort()
        for x in range(len(size_list)):
            if size_list[x] >= self.directory_sizes[''] - 40000000:
                return size_list[x]

    def build_file_system(self, lines):
        directory_chain = []
        for line in lines:
            match line.split():
                case '$','cd','..':     directory_chain.pop()
                case '$','cd','/':      directory_chain = ['/']
                case '$', 'cd', dir:    directory_chain.append(dir)
                case '$', 'ls':
                    current = '/'.join(directory_chain)[1:]
                    if current not in self.file_system:
                        self.file_system[current] = []
                case _:
                    self.file_system[current].append(line)

    def build_directory_sizes(self, directory):
        self.directory_sizes[directory] = 0
        for item in [d.split() for d in self.file_system[directory]]:
            if item[0] == 'dir':
                child = directory + '/' + item[1]
                if child not in self.directory_sizes:
                    self.build_directory_sizes(child)
                self.directory_sizes[directory] += self.directory_sizes[child]
            else:
                self.directory_sizes[directory] += int(item[0])

if __name__ == '__main__':
    Day7().run(INPUT_TYPE)
