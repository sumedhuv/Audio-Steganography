# Importing wave, struct, and sys from Python Standard Libraries
import wave
import struct
import sys



def getAudioInfo(audio):
    print("Samples in the file: ", audio.getnframes())
    print("Sampling rate of the file: ", audio.getframerate())
    print("Sampling width of file (bits per file: output*8):", audio.getsamplewidth())
    length = round(int(audio.getnframes()) / int(audio.getframerate()), 3)
    print("Length in seconds of the file:", length, "seconds")



def parseFrames(audio):
    # Uses wave object function getnframes to get number of samples
    length = audio.getnframes()
    # List for final audio files
    audioFrames = []
    # For the number for audio samples
    for i in range(0, length):
        # Read first audio file sample
        frame = audio.readframes(1)
        # Unpack 2 bytes, since these WAV files are 16-bit
        data = struct.unpack("<h", frame)
        # Appends the data point to audio frame file
        audioFrames.append(data[0])
    # Clears variable memory
    del length
    # returns list of audio points
    return audioFrames

def writeNewWave(list, sr, name):

    try:
        # Opens new wav file based on name
        newWave = wave.open(name, "w")
        # Sets channels to 1 (Mono)
        newWave.setnchannels(1)
        # Sets sample width to 2 (16-bit)
        newWave.setsampwidth(2)
        # Sets frame rate to that specified before
        newWave.setframerate(sr)
        # Sets number of frames to the length of the list you feed in
        newWave.setnframes(len(list))
        # For items in your list
        for items in list:
            # Makes item in list a 16-bit Byte
            byteType = struct.pack('<h', items)
            # Writes new byte as a frame in your new file
            newWave.writeframes(byteType)
        # Closes your wav file
        newWave.close()
        # Clears list and variable memory
        del list, sr, name
        # Returns new wav-object
        return newWave
    except:
        print("Error opening or naming file, check name and directory.")
        sys.exit(-1)

