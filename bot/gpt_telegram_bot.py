import openai
import os
import logging

from helpers import download_audio, convert_audio_to_wav
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
    CommandHandler,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

telegram_token = os.environ["TELEGRAM_TOKEN"]
openai.api_key = os.environ["OPENAI_TOKEN"]
openai_version = os.environ["OPENAI_VERSION"]

messages_list = []


def append_history(content, role):
    messages_list.append({"role": role, "content": content})
    return messages_list


def clear_history():
    messages_list.clear()
    return messages_list


async def process_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thinking = await context.bot.send_message(
        chat_id=update.effective_chat.id, text="🤔"
    )
    append_history(update.message.text, "user")

    response = generate_gpt_response()

    append_history(response, "assistant")
    await context.bot.deleteMessage(
        message_id=thinking.message_id, chat_id=update.message.chat_id
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


async def process_audio_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    transcript = await get_audio_transcription(update, context)
    append_history(transcript, "user")

    response = generate_gpt_response()

    append_history(response, "assistant")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


def generate_gpt_response():
    completion = openai.ChatCompletion.create(model=openai_version, messages=messages_list)
    return completion.choices[0].message["content"]


async def get_audio_transcription(update, context):
    new_file = await download_audio(update, context)
    voice = convert_audio_to_wav(new_file)
    transcript = openai.Audio.transcribe("whisper-1", voice)
    return transcript["text"]


async def reset_history(update, context):
    clear_history()
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Messages history cleaned"
    )
    return messages_list


if __name__ == "__main__":
    application = ApplicationBuilder().token(telegram_token).build()
    text_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), process_text_message
    )
    application.add_handler(text_handler)

    application.add_handler(CommandHandler("reset", reset_history))

    audio_handler = MessageHandler(filters.VOICE, process_audio_message)
    application.add_handler(audio_handler)

    application.run_polling()
