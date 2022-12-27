class SoundProperties:

    def __init__(self, 
        frequencies: list,
        sample_rate: int,       
        block_size: int,
        blocks_per_symbol: int,
    ):
        n = len(frequencies)
        if not (n & (n - 1) == 0) or n < 2:
            raise ValueError('Number of frequencies must be of the form 2 ^ n and greater or equal to 2')

        self.frequencies = frequencies
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.blocks_per_symbol = blocks_per_symbol