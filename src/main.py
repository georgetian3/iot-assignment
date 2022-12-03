from modem.modulator import Modulator
from modem.demodulator import Demodulator
from modem.soundproperties import SoundProperties


#from routes import app



if __name__ == '__main__':
    #app.run(debug=False, port=8000)

    p = SoundProperties(
        f0=10000,
        f1=12000,
        th0=2,
        th1=2,
        sample_rate=48000,
        symbol_duration=1 / 2 ** 6
    )
    m = Modulator(p)
    bits = '01' * 160
    wave = m.modulate(bits)
    m.play(wave)

    d = Demodulator(p)
    d.demodulate(
        bit_buffer=None,
        blocksize=int(p.symbol_duration * p.sample_rate),
        blocking=False
    )

    input('Press enter to continue...')

    d.stop()