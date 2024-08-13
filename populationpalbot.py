import requests
import spacy

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# Load the spaCy model for natural language processing
nlp = spacy.load("en_core_web_sm")

# Define the states for the conversation
ASK_COUNTRY, ASK_ANOTHER = range(2)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello there!\n\nMy name is PopulationPalBot🤖. \n\nI can help you find the population of any country. \n\nWhich country's population would you like to check?"
    )
    return ASK_COUNTRY  # Move to the ASK_COUNTRY state

def get_population(country: str):
    response = requests.get(f"https://restcountries.com/v3.1/name/{country}")
    if response.ok and response.json():
        population = response.json()[0].get('population', 'Not available')
        return f"The population of {country.title()} is {population:,}."
    return None  # Return None for invalid countries

def ask_country(update: Update, context: CallbackContext) -> int:
    user_message = update.message.text
    country = ' '.join(token.text for token in nlp(user_message) if not token.is_stop and not token.is_punct)
    population_info = get_population(country)

    if population_info:
        update.message.reply_text(population_info)
    else:
        update.message.reply_text("Sorry, I couldn't find that country. Please enter a valid country name.")

    update.message.reply_text("Would you like to find another country's population?")
    return ASK_ANOTHER  # Move to the ASK_ANOTHER state

def ask_another(update: Update, context: CallbackContext):
    user_response = update.message.text.strip().lower()

    if user_response in ['y', 'yes']:
        update.message.reply_text("Please enter the name of the country you'd like to check:")
        return ASK_COUNTRY  # Go back to asking for a country name
    elif user_response in ['n', 'no']:
        update.message.reply_text("Thank you for using PopulationPalBot🤖! \n\nDeuces✌🏽!")
        return ConversationHandler.END  # End the conversation
    else:
        update.message.reply_text("Please respond with 'yes' or 'no'.")
        return ASK_ANOTHER  # Stay in the ASK_ANOTHER state

def main():
    updater = Updater("7474298014:AAEHRMBvi1hyg5RAbpplx5In1zAzE8vpb2w", use_context=True)

    dp = updater.dispatcher

    # Set up the ConversationHandler with states ASK_COUNTRY and ASK_ANOTHER
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_COUNTRY: [MessageHandler(Filters.text & ~Filters.command, ask_country)],
            ASK_ANOTHER: [MessageHandler(Filters.text & ~Filters.command, ask_another)],
        },
        fallbacks=[],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
