
def make_text_blocks(text, **kwargs):
    rest = text
    style = ""
    end_style = ""
    voice_tag = ""
    end_voice_tag = ""
    if "voice" in kwargs:
        voice_tag = f'<voice name="{kwargs["voice"]}">'
        end_voice_tag = "</voice>"

    if "style" in kwargs:
        style = f'<mstts:express-as style="{kwargs["style"]}">'
        end_style = '</mstts:express-as>'

    text_blocks = []
    intro_ssml = f'''
                    <speak xmlns="http://www.w3.org/2001/10/synthesis" 
                        xmlns:mstts="http://www.w3.org/2001/mstts" 
                        xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
                    {voice_tag}
                        <prosody rate="medium">
                            {style}'''
    ending_ssml = f'''
                {end_style}
            </prosody>
        {end_voice_tag}
    </speak>
                '''
    while (len(rest) > 3000):
        begin = 0
        end = rest.rfind("</p>", 0, 3000)  # rfind looks for the last case of the search term.
        if (end == -1):
            end = rest.rfind(". ", 0, 3000)
            text_block = rest[begin:end + 1]
            rest = rest[end + 1:]
            text_blocks.append(intro_ssml + text_block + "</p>" + ending_ssml)
            rest = "<p>" + rest
        else:
            text_block = rest[begin:end + 4]
            rest = rest[ end + 4:]
            text_blocks.append(intro_ssml + text_block + ending_ssml)
    text_blocks.append( intro_ssml + rest + ending_ssml)
    return text_blocks
