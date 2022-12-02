class SoundProperties:
    def __init__(self, 
        amplitude: float,
        freq_0: float,
        freq_1: float,
        phase: float,
        sample_rate: int,
        duration: float
    ):

        if freq_0 < 0 or freq_1 < 0:
            raise ValueError('Frequency cannot be negative')
        if sample_rate < 0:
            raise ValueError('Frequency cannot be negative')
        if duration < 0:
            raise ValueError('Frequency cannot be negative')

        self.amplitude = amplitude
        self.freq_0 = freq_0
        self.freq_1 = freq_1
        self.phase = phase
        self.sample_rate = sample_rate
        self.duration = duration