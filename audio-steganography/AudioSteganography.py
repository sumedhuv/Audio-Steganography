import struct
import sys

class InputFile:
    def __init__(self, filename):
        """
        :param filename:
        """
        self.totalBits = 0
        self.totalBytes = 0
        self.charlist = []
        self.intlist = []
        self.filestr = ""
        self.filename = filename
        self.openfile()

    def openfile(self):

        try:
            # opens file in read mode to variable file
            file = open(self.filename, "r")
            # for characters in the file
            for item in file.read():
                # appends each character to the char list
                self.charlist.append(item)
            # appends NULL at the end to be our sentinel byte
            self.charlist.append(None)
            # calls function to add how many bits & bytes in the file
            self.totalBits, self.totalBytes = self.calculateBitsAndBytes()
            # closes the file
            file.close()
            # opens the file again in read mode, I could have also just made a string by iterating through
            # the char list[], but I wrote this portion at 1 am and I am commenting this now at 8 am.
            file = open(self.filename, "r")
            self.filestr = file.read()
            file.close()
            self.createIntList()

        except:
            # Broad exception that just catches any errors from file and quits the program
            print("Could not create file, check file name or that file is in current directory.")
            print("Exiting program.")
            sys.exit()

    def calculateBitsAndBytes(self):
        """
        :return bit byte:
        """
        bit = 0
        byte = 0
        # for characters in the list of characters
        for i in range(len(self.charlist)):
            # adds 8 bits per character
            bit += 8
            # adds 1 byte per character
            byte += 1
        # returns them for fun too
        return bit, byte

    def createIntList(self):
        """
        :return none:
        """
        # creates a new list for the integer ASCII values of the characters
        intlist = []
        # for characters in the char list - 1 (can't convert NULL to int in Python)
        for i in range(len(self.charlist)-1):
            # append the converted char -> int to new list
            intlist.append(ord(self.charlist[i]))
        # appends 0x00 as our new sentinel that is an int
        intlist.append(0)
        # adds this list to the class
        self.intlist = intlist


def encode(list, textfile):
    file = InputFile(textfile)
    encodedAudio = []
    audioNum = 0
    print(len(list),"\n")
    print(file.totalBits)
    # If we have equal or greater than amount of audio bytes to encode textfile bits into
    if len(list) >= file.totalBits:
        # for every character in the textfile
        for val in file.intlist:
            # for every bit in the character
            for i in range(7, -1, -1):
                # encode bit from left to right into the audio bytes
                bitToEncode = readBit(val, i)
                if list[audioNum] != abs(list[audioNum]):
                    negative = True
                else:
                    negative = False
                newVal = writeBit(abs(list[audioNum]), bitToEncode)
                if negative == True:
                    encodedAudio.append(-1*newVal)
                else:
                    encodedAudio.append(newVal)
                audioNum += 1

        #print(list)
        #print(encodedAudio)
        #print(encodedAudio + list[audioNum:])
        totalEncode = encodedAudio + list[audioNum:]

        return encodedAudio + list[audioNum:]

    else:
        print("Not enough samples to encode message in.")
        sys.exit(-1)

def decode(list, newfilename):
    """
    :param list:
    :param newfilename:
    :return strMessage or garbage:
    """
    # makes empty list to hold bits extracted
    bitlist = []
    # for all the bits in each audio sample
    for bits in list:
        # We want to treat this data as unsigned, so we abs() each audio sample value
        # then read the LSB of that audio same and append it to the bit list
        bitlist.append(readBit(abs(bits), 0))
    # Based on number of bits in our bit list, we can determine the amount of bytes by dividing the length by 8
    potentialBytes = determineTotalBytes(bitlist)
    # string variable to hold a bit string of our new data byte
    newByte = ""
    # boolean for determining if we have discovered a 0x00 sentinel byte that indicates we can stop looking for data
    endByte = False
    # counter makes sure we only append 8 bits to each new byte
    counter = 0
    # message holds our new characters we discover!
    message = []
    # for the length of potential bits
    for i in range(potentialBytes):
        # if we haven't appended 8 bits or we haven't discovered the sentinel
        if counter < 8 and endByte == False:
            # We add the newByte + a string of next bit in the bit list
            newByte += str(bitlist[i])
            # We increment the counter to indicate we added a bit
            counter += 1
        # else if we have already gotten 8 bits for our new data byte
        elif counter >= 8:
            # We get the ascii int value of the character by sequestering the base-2 string into its int form
            character = int(newByte, 2)
            # if our new character is equal zero then we have found our sentinel byte
            if(character == 0):
                # so this is true, we can exit the program!
                endByte = True
            # we append our new message as a character to the message list
            message.append(chr(character))
            # we reset newByte
            newByte = ""
            # and add a bit
            newByte += str(bitlist[i])
            # we reset the counter
            counter = 0
            # and add one to indicate we added a bit (you can also remove this line and make the above line counter = 1)
            counter += 1
        # if our end byte is true, we are done!
        elif endByte == True:
            # make a string to hold a string of our message
            strMessage = ""
            # for characters in the message list
            for characters in message:
                # we just add the characters to the string
                strMessage += characters
            # We write this message to a file, with our given file name from the input
            writeMessageToFile(strMessage, newfilename)
            # and we return the string of the message
            return strMessage

    # This section catches if there is no sentinel or the message was too long and was somehow encoded into the
    # audio sample
    print("No message found in signal (No sentinel encountered).")
    print("Returning string and file of random bytes found in message.")
    garbage = ""
    for things in message:
        garbage += things
    return garbage

def writeMessageToFile(message, filename):

    try:
        # opens new file based on file name provided
        newtext = open(filename, "w")
        # writes the message to the text file
        newtext.write(message)
        # closes the file
        newtext.close()
    except:
        print("Unable to open and write to file. Check file name and extension.")
        sys.exit()
    return

def determineTotalBytes(list):
    """
    :param list:
    :return total:
    """
    # Returns the length of the list divided by 8 as an integer (no remainder)
    return int(len(list) / 8)

def writeBit(integer, boolean):
    # If we want to set a 1 in the LSB
    if boolean == True:
        # ORs the integer with 0x01
        value = integer | 0x01
    # We want to set a 0 in the LSB
    else:
        # ANDs the integer with the inverse of 0x01
        value = integer & ~0x01
    # Returns new value
    return value

def readBit(integer, position):

    return ((0x01 << position) & abs(integer)) >> position
