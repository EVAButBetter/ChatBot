import struct

# Open the audio file in binary mode
with open("../../data/audio/1679000906.mp3", "rb") as audio_file:
    # Read the contents of the file as bytes
    audio_data = audio_file.read()

# Pack the audio data into a binary string using the 's' format string (string)
packed_data = struct.pack('{}s'.format(len(audio_data)), audio_data)

# Convert the binary string to an ArrayBuffer in JavaScript
array_buffer = bytearray(packed_data)