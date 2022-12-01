import base64


with open("cat-min.jpg", "rb") as image2string:
    converted_string = base64.b64encode(image2string.read())


with open('encode.txt', "wb") as file:
    file.write(converted_string)


file = open('encode.txt', 'rb')
byte = file.read()
file.close()

decodeit = open('recreated.jpg', 'wb')
decodeit.write(base64.b64decode((byte)))
decodeit.close()
