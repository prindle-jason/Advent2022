from adventutil.DataImport import InputType

DAY_START = 1
DAY_END = 11

def run():
    #This is... probably... not ideal.
    for x in range(DAY_START, DAY_END + 1):
        # not ideal intensifies...
        if (x == 5):
            exec(f"from solutions.Day{x} import Day{x}; Day{x}().run({InputType.LIVE_DATA}, False)")
        else:
            exec(f"from solutions.Day{x} import Day{x}; Day{x}().run({InputType.LIVE_DATA})")

if __name__ == "__main__":
    run()