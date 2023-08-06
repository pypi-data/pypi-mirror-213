class ExponentialMovingAverage:
    def __init__(self, data, window):
        self.data = data
        self.window = window

    def calculate_ema(self):
        ema = []
        alpha = 2 / (self.window + 1)  # Smoothing factor
        ema.append(self.data[0])
        for i in range(1, len(self.data)):
            ema_value = self.data[i] * alpha + ema[i - 1] * (1 - alpha)
            ema.append(ema_value)
        return ema


# data = [10, 12, 15, 13, 14, 11, 9]
# window = 3

# ema_calculator = ExponentialMovingAverage(data, window)
# ema = ema_calculator.calculate_ema()
# print(ema)
