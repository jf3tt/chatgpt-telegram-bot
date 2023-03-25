import os
from pydub import AudioSegment

async def download_audio(update, context):
    file_id = update.message.voice.file_id
    print (update)
    new_file = await context.bot.get_file(file_id)
    await new_file.download_to_drive(file_id + ".oga")
    return file_id

def convert_audio_to_wav(audio_file):
    with open(audio_file + ".oga", "rb") as f:
        voice = AudioSegment.from_ogg(f)
    voice_wav = voice.export(audio_file + ".wav", format="wav")
    os.remove(audio_file + ".wav")
    os.remove(audio_file + ".oga")
    return voice_wav

