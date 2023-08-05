# self_messages

self_messages is a Python library for reading messages using discord selfbots. This is handy because discord recently removed the access of message content to self bots.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install self_messages
```

## Usage

```python
import discord
from self_messages import self_messages

token = ""

sm = self_messages(token)
bot = discord.Client()

@bot.event
async def on_message(message):
    # message id and channel id
    message_content = sm.get(channel_id=message.channel.id, message_id=message.id)

    print(message_content)

bot.run(token, bot=False)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)