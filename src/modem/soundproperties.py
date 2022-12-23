class SoundProperties:


    
    def __init__(self, 
        f0: float,              # frequency corresponding to 0 bit
        f1: float,              # frequency corresponding to 1 bit
        sample_rate: int,       
        symbol_duration: float, # duration for which a single bit is transmitted
        block_size: int,
        blocks_per_symbol: int,
    ):

        if f0 < 0 or f1 < 0:
            raise ValueError('Frequency cannot be negative')
        if sample_rate < 0:
            raise ValueError('Sample rate cannot be negative')
        if symbol_duration < 0:
            raise ValueError('Symbol duration cannot be negative')

        self.f0 = f0
        self.f1 = f1
        self.sample_rate = sample_rate
        self.symbol_duration = symbol_duration
        self.block_size = block_size
        self.blocks_per_symbol = blocks_per_symbol



        