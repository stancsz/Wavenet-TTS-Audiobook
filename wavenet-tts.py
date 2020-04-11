"""Synthesizes speech from the input string of text or ssml.
Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
import os
from google.cloud import texttospeech

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Loop through <files-source> directory
path_in = "files-source"
path_out = "files-audio-out"

for filename in os.listdir(path_in):
    if filename.endswith(".txt") or filename.endswith(".ssml"):
        print(os.path.join(path_in, filename))
        source = os.path.join(path_in, filename)
        read_file = open(source, mode='r')

        # read all lines at once
        text_to_transcribe = read_file.read()
        # close the file
        read_file.close()
        print(text_to_transcribe)

        # Set the text input to be synthesized
        synthesis_input = texttospeech.types.SynthesisInput(text=text_to_transcribe)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        # Voices names can be found under: https://cloud.google.com/text-to-speech/docs/voices
        voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-US',
            name='en-US-Wavenet-F',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

        # Select the type of audio file you want returned
        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(synthesis_input, voice, audio_config)

        # The response's audio_content is binary.
        target = os.path.join(path_out, filename + '.mp3')
        with open(target, 'wb') as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to file "'+target+'"')

        continue
    else:
        print("This file is not in txt format")
        continue

