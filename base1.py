import time
import wave
import numpy as np


__Author__ = "Amir Mohammad"

def change_voice(in_address='file.wav'):

    # in_address = 'output.wav'
    out_address = 'pitch1.wav'

    # open the file :
    wr = wave.open(in_address, 'r')
    # Set the parameters for the output file.
    par = list(wr.getparams())
    par[3] = 0  # The number of samples will be set by writeframes.
    par = tuple(par)
    ww = wave.open(out_address, 'w')
    ww.setparams(par)

    fr = 5  # 20
    sz = wr.getframerate() // fr  # Read and process 1/fr second at a time.
    # A larger number for fr means less reverb.
    c = int(wr.getnframes() / sz)  # count of the whole file
    shift = 500 // fr  # shifting 500 Hz , default = 100
    for num in range(c):
        # Read the data, split it in left and right channel (assuming a stereo WAV file).
        da = np.fromstring(wr.readframes(sz), dtype=np.int16) * 3

        left, right = da[0::2], da[1::2]  # left and right channel

        # Extract the frequencies using the Fast Fourier Transform built into numpy
        # تبدیل فوریه فرکانس هارا با استفاده از ماژول مربوطه محاسبه میکند
        lf, rf = np.fft.rfft(left), np.fft.rfft(right)

        # Roll the array to increase the pitch.
        lf, rf = np.roll(lf, shift), np.roll(rf, shift)

        # The highest frequencies roll over to the lowest ones. That's not what we want, so zero them.
        lf[0:shift], rf[0:shift] = 0, 0

        # Now use the inverse Fourier transform to convert the signal back into amplitude.
        nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)

        # Combine the two channels.
        ns = np.column_stack((nl, nr)).ravel().astype(np.int16)
        # Write the output data.
        ww.writeframes(ns.tostring())

    wr.close()
    ww.close()

    print("voice has been changed !")
    time.sleep(1)
    print("file created")
