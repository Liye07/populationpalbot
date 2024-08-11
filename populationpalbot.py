import requests
import spacy

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

nlp = spacy.load("en_core_web_sm")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! I am PopulationPalBot. \n\nI can help you find the population of any country. \n\nWhich country's population would you like to check?")


def get_population(country: str) -> str:
    response = requests.get(f"https://restcountries.com/v3.1/name/{country}")
    if response.ok and response.json():
        population = response.json()[0].get('population', 'Not available')
        return f"The population of {country.title()} is {population:,}."
    return "Sorry, I couldn't find that country."

def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    country = ' '.join(token.text for token in nlp(user_message) if not token.is_stop and not token.is_punct)
    population_info = get_population(country)
    
    update.message.reply_text(population_info)
    update.message.reply_text("Would you like to check another country?")


def handle_response(update: Update, context: CallbackContext) -> None:
    user_response = update.message.text.lower()
    if user_response in ['yes', 'y']:
        update.message.reply_text("Which country would you like to check?")
    elif user_response in ['no', 'n']:
        update.message.reply_text("Thank you for using PopulationPalBot! Goodbye!")
        return 
    else:
        update.message.reply_text("Please respond with 'yes' or 'no'.")
    

def main() -> None:
    updater = Updater("7474298014:AAEHRMBvi1hyg5RAbpplx5In1zAzE8vpb2w", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_response))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
