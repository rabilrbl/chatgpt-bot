<div align="center">

  # CHATGPT-BOT
  
  **A Python Telegram bot powered by ChatGPT**

  *This is a Python Telegram bot that uses ChatGPT to generate creative text formats based on user input. It is designed to be a fun and interactive way to explore the possibilities of large language models.*

  [ChatGPT Bot Preview](https://github.com/rabilrbl/chatgpt-bot/assets/63334479/d2cdf7db-58c7-4500-bea0-827baca8beb7)

</div>

### Features

* Generate creative text formats like poems, code, scripts, musical pieces, etc.
* Stream the generation process, so you can see the text unfold in real-time.
* Reply to your messages with Bard's creative output.
* Easy to use with simple commands:
    * `/start`: Greet the bot and get started.
    * `/help`: Get information about the bot's capabilities.
* Send any text message to trigger the generation process.
* Restrict the bot to specific users or groups.

### Requirements

* Python 3.10+
* Telegram Bot API token
* A `__Secure-next-auth.session-token` cookie value from ChatGPT Website.
* dotenv (for environment variables)


### Docker

#### GitHub Container Registry
Simply run the following command to run the pre-built image from GitHub Container Registry:

```shell
docker run --env-file .env ghcr.io/rabilrbl/chatgpt-bot:latest
```

Update the image with:
```shell
docker pull ghcr.io/rabilrbl/chatgpt-bot:latest
```

#### Build
Build the image with:
```shell
docker build -t chatgpt-bot .
```
Once the image is built, you can run it with:
```shell
docker run --env-file .env chatgpt-bot
```

### Installation

1. Clone this repository.
2. Install the required dependencies:
    * `pipenv install` (if using pipenv)
    * `pip install -r requirements.txt` (if not using pipenv)
3. Create a `.env` file and add the following environment variables:
    * `BOT_TOKEN`: Your Telegram Bot API token. You can get one by talking to [@BotFather](https://t.me/BotFather).
    * `SESSION_KEY`: `__Secure-next-auth.session-token` cookie value. You can get one from [ChatGPT](https://chat.openai.com/). After logging in, head to inspect tab > Applications > Cookie > select chat.openai.com.
    * `AUTHORIZED_USERS`: A comma-separated list of Telegram usernames or user IDs that are authorized to use the bot. You can get your user ID by talking to [@userinfobot](https://t.me/userinfobot).
4. Run the bot:
    * `python main.py` (if not using pipenv)
    * `pipenv run python main.py` (if using pipenv)

### Usage

1. Start the bot by running the script.
   ```shell
   python main.py
   ```
2. Open the bot in your Telegram chat.
3. Send any text message to the bot.
4. The bot will generate creative text formats based on your input and stream the results back to you.

### Bot Commands

| Command | Description |
| ------- | ----------- |
| `/start` | Greet the bot and get started. |
| `/help` | Get information about the bot's capabilities. |
| `/new` | Start a new chat session. |


### Contributing

We welcome contributions to this project. Please feel free to fork the repository and submit pull requests.


### Acknowledgements

- [Zai-Kun/reverse-engineered-chatgpt](https://github.com/Zai-Kun/reverse-engineered-chatgpt)
- [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot)

### Disclaimer

This bot is still under development and may sometimes provide nonsensical or inappropriate responses. Use it responsibly and have fun!

### License

This is a free and open-source project released under the GNU Affero General Public License v3.0 license. See the LICENSE file for details.
