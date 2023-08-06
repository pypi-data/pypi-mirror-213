
from .text_blocks import make_text_blocks
from .google_cloud import google_tts, get_google_voices, load_google_client
from .azure_cloud import azure_tts, get_azure_voices, load_azure_client
from .aws_cloud import aws_tts, get_aws_voices, load_aws_client

def get_voices(platform):
    if platform == "google":
        google_client = load_google_client()
        voice_list = get_google_voices(google_client)
        return voice_list
    elif platform == "azure":
        azure_client = load_azure_client()
        voice_list = get_azure_voices(azure_client)
        return voice_list
    elif platform == "aws":
        aws_client = load_aws_client()
        voice_list = get_aws_voices(aws_client)
        return voice_list

def example_text():
    return """This is an example of how to use the cloud_tts module. 
    The module automatically uses the text_blocks module which breaks a long string
    of text into blocks of text that are short enough to be processed by the cloud tts services. 
    The cloud_tts module then sends each block of text to the cloud tts service 
    and returns the audio data. 
    The audio data is then saved to a file by the save_audio module. 
    The save_audio module can save the audio data to a file or play the audio data.
    """

def make_tts(text =example_text(), platform="google", voice="en-US-Wavenet-A", **kwargs):
    if platform == "google":
        text_blocks = make_text_blocks(text, voice=voice)
        google_client = load_google_client()
        return google_tts(google_client, voice, text_blocks, **kwargs)
    elif platform == "aws":
        text_blocks = make_text_blocks(text)
        aws_client = load_aws_client()
        engine = "neural"
        if kwargs["engine"]:
            engine = kwargs["engine"]
        return aws_tts(text_blocks, aws_client, voice, engine=engine)
    elif platform == "azure":
        text_blocks = make_text_blocks(text, voice=voice, **kwargs)
        azure_client = load_azure_client()
        return azure_tts(azure_client, text_blocks)
