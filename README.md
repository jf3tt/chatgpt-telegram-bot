# GPT-4 Telegram Bot

GPT-4 Telegram Bot is a simple and easy-to-use conversational AI-assistant running on GPT-4 language models. It provides the capability to interact with the bot through voice inputs by performing audio recognition on Telegram.

## Features
* Responds to user inputs in text format using [OpenAI GPT-4 Language Models](https://beta.openai.com/docs/models/gpt-4).
* Voice recognition with OpenAI Whisper ASR to handle voice inputs.
* Reset mechanism for clearing the conversation history.

## Requirements
* Python 3.x installed
* Install necessary Python packages using the requirements.txt file.
  ```
  pip install -r requirements.txt
  ```

## Environment Variables
* `TELEGRAM_TOKEN`: Your Telegram Bot Token which can be obtained from [BotFather](https://core.telegram.org/bots#6-botfather).
* `OPENAI_TOKEN`: Your OpenAI API Key, which can be found on the [OpenAI Dashboard](https://beta.openai.com/signup).

## Usage
1. Set your environment variables:
   ```
   export TELEGRAM_TOKEN=your_telegram_token
   export OPENAI_TOKEN=your_openai_token
   ```

2. Run the script:
   ```
   python3 gpt_telegram_bot.py
   ```

3. Open the Telegram app and interact with the bot using text messages or voice inputs.

## Commands
* `/reset`: Clear the conversation history.

## Functions
* `append_history(question, messages_list, role)`: Appends a message to the conversation history.
* `audio_response(text)`: Converts text to audio.
* `gpt_response(update: Update, context: ContextTypes.DEFAULT_TYPE)`: Handles GPT model requests and sends text responses.
* `audio_recognition(update: Update, context: ContextTypes.DEFAULT_TYPE)`: Handles audio inputs, performs voice recognition, and sends text responses.
* `reset(update, context)`: Clears the conversation history.

**Note:** GPT-4 model in this code is a placeholder, as future models like GPT-4 are expected to be built upon GPT-3's architecture, making the script ready for an upgrade once GPT-4 is released.