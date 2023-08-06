from sndlib import* 
import soundfile as sndf
import copy, os

stim_folder = "../sound_source_id/prm_files/pink_noises/"
pulsed = False
n_pulses = 1
interpulse_isi = 50 #ms
n_noises = 30
noise1SpectrumLevel = 40
duration = 180
ramp = 10
sf = 48000
maxLevel = 100
noise1RefHz = 1000
noise1LowFreq = 50
noise1HighFreq = 16000
lowStop = 0.8
highStop = 1.2

if os.path.exists(stim_folder) == False:
    os.makedirs(stim_folder)
    
thisTone = pureTone(frequency=1000, phase=0, level=60, duration=duration, ramp=ramp, channel="Both", fs=sf, maxLevel=maxLevel)

for i in range(n_noises):
    noise1Source = broadbandNoise(noise1SpectrumLevel, duration + ramp*2+20, 0,
                                  "Both", sf,
                                  maxLevel)
    noise1 = makePinkRef(copy.copy(noise1Source), sf, noise1RefHz)

    noise1 = fir2Filt(noise1LowFreq*lowStop, noise1LowFreq, noise1HighFreq,
                      noise1HighFreq*highStop, noise1, sf)
    noise1 = noise1[int(round(0.01*sf)):int(round(0.01*sf))+thisTone.shape[0],]

    if pulsed == True:
        for pulse_n in range(n_pulses-1):
                noiseXSource = broadbandNoise(noise1SpectrumLevel, duration + ramp*2+20, 0,
                                  "Both", sf,
                                  maxLevel)
                noiseX = makePinkRef(copy.copy(noiseXSource), sf, noise1RefHz)
                
                noiseX = fir2Filt(noise1LowFreq*lowStop, noise1LowFreq, noise1HighFreq,
                                  noise1HighFreq*highStop, noise1, sf)
                noiseX = noiseX[int(round(0.01*sf)):int(round(0.01*sf))+thisTone.shape[0],]
                ips = makeSilence(interpulse_isi, sf)
                noise1 = concatenate((noise1, ips, noiseX), axis=0)

    sndf.write(stim_folder+'noise'+str(i+1)+'.wav', noise1[:,0], sf, subtype="PCM_24")



# duration = 10000 / 1000 #convert from ms to sec
# nSamples = int(round(duration * sf))
# sil = zeros((nSamples, 15))
# sndf.write('silence_15_chan.wav', sil, sf, subtype="PCM_24")

# sil = zeros((nSamples, 16))
# sndf.write('silence_16_chan.wav', sil, sf, subtype="PCM_24")
