from modem.modulator import Modulator
from modem.demodulator import Demodulator
from modem.soundproperties import SoundProperties


from routes import app



if __name__ == '__main__':
    #app.run(debug=False, port=8000)

    p = SoundProperties(
        f0=12000,
        f1=14000,
        th0=5,
        th1=5,
        sample_rate=48000,
        symbol_duration=1 / 2 ** 6
    )
    m = Modulator(p)
    bits = '01' * 4
    wave = m.modulate(bits, 1)

    d = Demodulator(p)
    d.demodulate(
        bit_buffer=None,
        blocksize=128,
        blocking=False
    )

    input('Press enter to continue...')

    d.stop()