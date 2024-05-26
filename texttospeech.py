"""
This file will contain the code to convert text to speech.
This will be done by sending a request to the Google Text-to-Speech API.
"""
from google.cloud import texttospeech
def tts(text: str, output_path: str):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(
        text=text
    )

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        # language_code="en-US", name="en-US-Standard-C", ssml_gender='FEMALE'
        # language_code = "cmn-cn", name = "cmn-cn-Standard-A", ssml_gender = 'FEMALE'
        language_code="en-US", name="en-US-Journey-D", ssml_gender='MALE'
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(f"{output_path}.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

