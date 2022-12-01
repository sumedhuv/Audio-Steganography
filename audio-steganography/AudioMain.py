import wave
import AudioParse
import AudioSteganography
import base64
def solve(x):
    if(x==1):
        
        with open("cat-min.jpg", "rb") as image2string:
            converted_string = base64.b64encode(image2string.read())
        with open('secret.txt', "wb") as file:
            file.write(converted_string)
        

        audio = wave.open("FirstAddress.wav", "r")
        list = AudioParse.parseFrames(audio)

        samplerate = audio.getframerate()
        encodedAudio = AudioSteganography.encode(list, "secret.txt")
        AudioParse.writeNewWave(encodedAudio, samplerate, "altered_FA.wav")
        audio.close()
        print("----IMAGE ENCODED IN THE AUDIO SUCCESSFULLY------\n")
    elif x==2:
        encodedAudio = wave.open("altered_FA.wav", "r")
        newlist = AudioParse.parseFrames(encodedAudio)
        secretMessage = AudioSteganography.decode(newlist, "ANS.txt")
        #print(secretMessage)
        encodedAudio.close()

        file = open('secret.txt', 'rb')
        byte = file.read()
        file.close()

        decodeit = open('recreated.jpg', 'wb')
        decodeit.write(base64.b64decode((byte)))
        decodeit.close()
        print("Image has been extracted")
        
    elif x==3:
        quit()
    else:
        print("Invalid choice")



def main():

    while(1):
        print("\nSelect an option: \n1)Hide the message\n2)Decode the message\n3)exit")
        val = int(input("\nChoice:"))
        solve(val)


main()