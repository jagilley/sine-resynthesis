# sine-resynthesis

Resynthesize any audio file lossily as a sum of sine waves, additive synthesizer style.

## Why would you want to do this?

1. Because it's cool
1. Because most generative audio models currently operate on the mel-spectrogram of the source audio. This requires a lot of memory, much of which is probably unnecessary for recreating harmonic sounds (e.g., most musical instruments.) In principle, you can reduce the memory requirements by finding the harmonic peaks in the spectrogram above a given amplitude threshold and modeling the source audio as a sum of sine waves at those frequencies.

## State of the repo

Currently, only static spectral profiles are supported. But it shouldn't be a huge lift to support dynamic spectral profiles as the `audio_to_sine_waves()` function already returns time values.
