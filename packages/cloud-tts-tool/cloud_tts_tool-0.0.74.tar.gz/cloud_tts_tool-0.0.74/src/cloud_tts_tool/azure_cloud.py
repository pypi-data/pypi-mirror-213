import azure.cognitiveservices.speech as speechsdk
import keyring
import time

def load_azure_client():
    subscription_key = keyring.get_password("azure_tts","azure_subscription_key")
    service_region= keyring.get_password("azure_tts","azure_service_region")
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=service_region)
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio48Khz96KBitRateMonoMp3)
    print('speech client loaded ' + service_region)
    return(speechsdk.SpeechSynthesizer(speech_config=speech_config))

def get_azure_voices(azure_client):
    voices_result = azure_client.get_voices_async().get()
    voices_list = []
    for n, voice in enumerate(voices_result.voices):
        voices_list.append(dict({
            "id": n,
            "name": voice.short_name,
            "loc": voice.locale,
            "gender": voice.gender.name,
            "styles": voice.style_list
             }
        ))
    return(voices_list)

def azure_tts(azure_client, text_blocks):
    audio_data_list = []
    for n, text_block in enumerate(text_blocks):
        print(f'Text block {n} of {len(text_blocks)}')
        result = azure_client.speak_ssml_async(text_block).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            # print(text_block)
            # print("Speech synthesized for text")
            audio_data_list.append(result.audio_data)
            time.sleep(2)
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                 if cancellation_details.error_details:
                       print("Error details: {}".format(cancellation_details.error_details))
                       print("Did you set the speech resource key and region values?")
            break
    return b"".join(audio_data_list)