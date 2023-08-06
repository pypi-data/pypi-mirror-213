class SimpleMovingAverage:
    def __init__(self, data, window):
        self.data = data
        self.window = window

    def calculate_sma(self):
        sma = []
        for i in range(len(self.data)):
            if i < self.window - 1:
                sma.append(None)
            else:
                sma.append(sum(self.data[i - self.window + 1 : i + 1]) / self.window)
        return sma


# data = [x for x in range(1,11)]
# window = 3

# sma_calculator = SimpleMovingAverage(data, window)
# sma = sma_calculator.calculate_sma()
