# Cloud TTS

This package is in development but will allow you to easily connect to a variety of text to speach apis.

Please set keyring items:

Google Cloud:
https://cloud.google.com/iam/docs/service-accounts-create
```python
#python console
import keyring
keyring.set_password("cloud_tts", "google_private_key_id", "<GOOGLE_PRIVATE_KEY_ID_FROM_JSON>")
keyring.set_password("cloud_tts", "google_private_key", "<GOOGLE_PRIVATE_KEY_FROM_JSON>")
keyring.set_password("cloud_tts", "google_client_email", "<GOOGLE_CLIENT_EMAIL>")
```
The other items don't appear to matter.

#AWS Polly:
in console, IAM, Users, Add user,
choose a username 
Attatch Policies Directly
select only "AmazonPollyReadOnlyAccess"
Create User, copy Access key ID and Secret access key and add them to your keychain

```python
#python console
import keyring

keyring.set_password("aws_tts", "aws_access_key_id", "<AWS_ACCESS_KEY_ID>")
keyring.set_password("aws_tts", "aws_secret_access_key", "<AWS_SECRET_ACCESS_KEY>")`
```
#Microsoft Azure:
https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-text-to-speech?tabs=script%2Cwindowsinstall&pivots=programming-language-python
Create Speech Services resource
Pay-as-you-go/DefaultResourceGroup-CUS
Choose region
Name resource (don't use spaces or underscores)
Chose pricing tier (free allows for about an hour of neural voice per month)
Network type: Selected Network
create new virtual network and subnet
put your ip address in the firewall  (https://www.google.com/search?q=what+is+my+ip)
Review and Create
Create

From home you should see the name of your resource, click on it
Click Manage Keys
Copy Key 1 and add it to your keychain
Copy Location/Region and add it to your keychain (not really a secret, but since 
your key is tied to a region, it's nice to have it in the same place)

```python
#python console
import keyring
keyring.set_password("azure_tts", "azure_key", "<AZURE_KEY_1>")
keyring.set_password("azure_tts", "azure_region", "<AZURE_REGION>")
```

# Usage

```python
import keyring
from cloud_tts import get_voices

platform = "google" # or "aws" or "azure"
voice_list = get_voices(platform)

# print out the voices
for voice in voice_list:
    print(f'{voice["id"]} {voice["name"]} {voice["language"]}')
```

Send text to cloud

```python
from cloud_tts import make_tts, example_text

audio_content = make_tts(text =example_text(), voice="en-US-Wavenet-A", platform="google", loc="en_US", gender="FEMALE")

#save audio
filename = "example.mp3"
with open("example.mp3", "wb") as f:
    f.write(audio_content)
```


