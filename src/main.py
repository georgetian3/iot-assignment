from modem.modulator import Modulator
from modem.demodulator import Demodulator
from modem.soundproperties import SoundProperties

import numpy as np

from routes import app




if __name__ == '__main__':
    #app.run(debug=False, port=8000)

    p = SoundProperties(0.8, 440, 880, 0, 44100, 1)
    m = Modulator(p)
    bits = '1' * 100
    wave = m.modulate(bits, False)


    y = np.fft.fft(wave)
    x = np.fft.fftfreq(len(wave), 1 / p.sample_rate)





    input('Press enter to continue...')