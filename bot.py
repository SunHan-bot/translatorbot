import discord
import requests
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_message(message):

    # aby bot nereagoval sám na sebe
    if message.author == client.user:
        return

    # reaguje na /translate i /traductor
    if message.content.startswith("/translate") or message.content.startswith("/traductor"):

        # rozdělí zprávu
        casti = message.content.split(" ", 2)

        # kontrola správného použití
        if len(casti) < 3:
            await message.channel.send(
                "Použití:\n"
                "/translate en text\n"
                "/translate es text\n"
                "/translate cs text\n\n"
                "nebo\n\n"
                "/traductor en text\n"
                "/traductor es text\n"
                "/traductor cs text"
            )
            return

        # příkaz (/translate nebo /traductor)
        prikaz = casti[0]

        # cílový jazyk
        cilovy_jazyk = casti[1]

        # text k překladu
        text = message.content.replace(prikaz, "", 1).strip()
        text = text.split(" ", 1)[1]

        # povolené jazyky
        if cilovy_jazyk not in ["en", "es", "cs"]:
            await message.channel.send("Umím jen: en, es, cs")
            return

        try:

            # Google překladač
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

            # data z odpovědi
            data = odpoved.json()

            # překlad
            vysledek = data[0][0][0]

            # odešle překlad
            await message.channel.send(vysledek)

        except Exception as chyba:
            await message.channel.send("Chyba: " + str(chyba))

# token z HeavenCloud / Railway / systému
client.run(os.getenv("DISCORD_TOKEN"))
