import requests
import spacy

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

nlp = spacy.load("en_core_web_sm")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! Which country are you from?")

def get_population(country: str) -> str:
    response = requests.get(f"https://restcountries.com/v3.1/name/{country}")
    if response.status_code == 200 and response.json():
        population = response.json()[0].get('population', 'Population data not found')
        return f"The population of {country.title()} is {population:,}."
    return "Sorry, I couldn't find that country."

def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    doc = nlp(user_message)
    country = ' '.join([token.text for token in doc if not token.is_stop and not token.is_punct])

    population_info = get_population(country)
    update.message.reply_text(population_info)

def main() -> None:
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

