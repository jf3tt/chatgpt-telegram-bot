import openai
import os
import logging

from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, MessageHandler

from pydub import AudioSegment

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
telegram_token = os.environ["TELEGRAM_TOKEN"]
openai.api_key = os.environ["OPENAI_TOKEN"]

messages_list = []
messages_json = {}


def append_history(question, messages_list, role):
    if role == "user":
        messages_list.append({"role": "user", "content": question})
    elif role == "assistant":
        messages_list.append({"role": "assistant", "content": question})
    return messages_list

async def gpt_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    append_history(update.message.text, messages_list, "user")

    completion = openai.ChatCompletion.create(model="gpt-4", messages=messages_list)
    response = completion.choices[0].message["content"]

    append_history(response, messages_list, "assistant")

    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

async def audio_recognition(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file_id = update.message.voice.file_id
    new_file = await context.bot.get_file(file_id)
    await new_file.download_to_drive("voice.oga")
    audio_file = open("voice.oga", "rb")
    voice = AudioSegment.from_ogg(audio_file)
    voice_wav = voice.export("voice.wav", format="wav")
    os.remove("voice.wav")
    os.remove("voice.oga")

    transcript = openai.Audio.transcribe("whisper-1", voice_wav)

    append_history(transcript["text"], messages_list, "user")

    completion = openai.ChatCompletion.create(model="gpt-4", messages=messages_list)
    response = completion.choices[0].message["content"]

    append_history(response, messages_list, "assistant")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


async def reset(update, context):
    print(messages_list)
    append_history("none", messages_list, "none")
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Messages history cleaned"
    )

    print(messages_list)


if __name__ == "__main__":
    application = ApplicationBuilder().token(telegram_token).build()
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), gpt_response)
    application.add_handler(text_handler)

    audio_handler = MessageHandler(filters.VOICE, audio_recognition)
    application.add_handler(audio_handler)

    application.run_polling()
