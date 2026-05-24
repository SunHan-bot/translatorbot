import discord
import requests

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_message(message):

    # aby bot nereagoval sám na sebe
    if message.author == client.user:
        return

    # pokud zpráva začíná /translate
    if message.content.startswith("/translate"):

        # rozdělí zprávu na části
        casti = message.content.split(" ", 2)

        # kontrola správného použití
        if len(casti) < 3:
            await message.channel.send(
                "Použití:\n"
                "/translate en text\n"
                "/translate es text\n"
                "/translate cs text"
            )
            return

        # cílový jazyk
        cilovy_jazyk = casti[1]

        # text k překladu
        text = casti[2]

        # povolené jazyky
        if cilovy_jazyk not in ["en", "es", "cs"]:
            await message.channel.send("Umím jen: en, es, cs")
            return

        try:

            # požadavek na Google překladač
            odpoved = requests.post(
                "https://translate.googleapis.com/translate_a/single",
                params={
                    "client": "gtx",
                    "sl": "auto",
                    "tl": cilovy_jazyk,
                    "dt": "t",
                    "q": text
                }
            )

            # odpověď
            data = odpoved.json()

            # překlad
            vysledek = data[0][0][0]

            # pošle překlad
            await message.channel.send(vysledek)

        except Exception as chyba:
            await message.channel.send("Chyba: " + str(chyba))

# sem vlož svůj token
import os

client.run(os.getenv("DISCORD_TOKEN"))
