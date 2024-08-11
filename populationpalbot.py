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
    return None 

def thank_you(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Thank you for using PopulationPalBot! \n\nGoodbye!")

def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    country = ' '.join(token.text for token in nlp(user_message) if not token.is_stop and not token.is_punct)
    population_info = get_population(country)
    
    if population_info:
        update.message.reply_text(population_info)
    else:
        update.message.reply_text("Sorry, I couldn't find that country.")
    
    thank_you(update, context)
    context.bot_data['updater'].stop()  # Stop the bot after sending the thank you message

def main() -> None:
    updater = Updater("7474298014:AAEHRMBvi1hyg5RAbpplx5In1zAzE8vpb2w", use_context=True)
    updater.dispatcher.bot_data['updater'] = updater 
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
