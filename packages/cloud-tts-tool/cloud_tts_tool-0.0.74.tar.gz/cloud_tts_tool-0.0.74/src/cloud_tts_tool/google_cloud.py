from google.cloud import texttospeech
import keyring

def load_google_client():
    client_dict = {
        "type": "service_account",
        "private_key_id": keyring.get_password("google_tts","google_private_key_id"),
        "private_key": keyring.get_password("google_tts","google_private_key"),
        "client_email": keyring.get_password("google_tts","google_client_email"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/pythontesttexttospeech%40text-to-speech-289419.iam.gserviceaccount.com"
    }
    return texttospeech.TextToSpeechClient.from_service_account_info(client_dict)

def get_google_voices(google_client):
    voices_result = google_client.list_voices()
    voices_list = []
    for n, voice in enumerate(voices_result.voices):
        voices_list.append(dict({
            "id": n,
            "name": voice.name,
            "loc": voice.language_codes[0],
            "gender": voice.ssml_gender.name,
            "rate": voice.natural_sample_rate_hertz,}
        ))
    return(voices_list)


def google_tts(google_client, voice, text_blocks, **kwargs):
    print(f"google_tts loaded with voice {voice} and {len(text_blocks)} text blocks")
    print(text_blocks[0])
    #todo add voice check
    gender = "texttospeech.SsmlVoiceGender." + kwargs['gender']
    voice = texttospeech.VoiceSelectionParams(
        language_code=kwargs['loc'],
        ssml_gender=kwargs['gender'],
        name=voice
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.0,
    )
    return b"".join(
        google_client.synthesize_speech(input=texttospeech.SynthesisInput(ssml=text_block), voice=voice, audio_config=audio_config).audio_content for text_block in text_blocks)


