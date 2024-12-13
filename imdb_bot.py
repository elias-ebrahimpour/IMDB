from Config import Settings
from Database import MongoDB
from strings import HELP_COMMAND_RESPONSE, PROCESS_DONE_MESSAGE
from textblob import TextBlob
import re
import requests
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from telegram import Update
from Utils import preprocessing
from crawler import get_imdb_reviews

import logging

settings = Settings()

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# MongoDB setup
db = MongoDB()
db.set_collection("university_assignment")


# Telegram bot handlers and functions
def clean_movie_name(text):
    cleaned_text = re.sub(r"@\S+", "", text)
    cleaned_text = cleaned_text.strip()
    cleaned_text = re.sub(r"\s+\d{4}.*$", "", cleaned_text)
    return cleaned_text


def get_movie_details(movie_name):
    url = f"https://www.omdbapi.com/?t={movie_name}&apikey={settings.imdb_api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            return data
        else:
            return "Movie not found."
    return "Error fetching details."


def analyze_sentiments(reviews):
    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
    processed_reviews = []
    for review in reviews:
        sentiment = TextBlob(review).sentiment.polarity
        if sentiment > 0:
            sentiment_category = "positive"
        elif sentiment < 0:
            sentiment_category = "negative"
        else:
            sentiment_category = "neutral"
        sentiment_counts[sentiment_category] += 1
        processed_reviews.append(
            {"text": review, "sentiment": sentiment_category})
    return processed_reviews, sentiment_counts


def save_to_mongodb(movie_details, reviews, sentiment_counts):
    movie_data = {
        **movie_details,
        "reviews": reviews,
        "sentiment_summary": sentiment_counts,
    }
    record = db.create(movie_data)
    return record.inserted_id


# /help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_COMMAND_RESPONSE)


# Message handler for processing movie names
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        raw_text = update.message.text.strip()
        movie_name = clean_movie_name(raw_text)  # Clean the input

        if movie_name:
            processing_message = await update.message.reply_text("🌀 Wait for it...🌀")

            details = get_movie_details(movie_name.strip())
            if isinstance(details, dict) and details.get("imdbID"):
                reviews = get_imdb_reviews(imdb_id=details.get("imdbID"))

                # Preprocessing
                cleaned_reviews = preprocessing(reviews)
                processed_reviews, sentiment_counts = analyze_sentiments(
                    cleaned_reviews)

                # Save to MongoDB
                record_id = save_to_mongodb(
                    details, processed_reviews, sentiment_counts)

                # Update the "Processing..." message with the final result
                await context.bot.edit_message_text(
                    chat_id=processing_message.chat_id,
                    message_id=processing_message.message_id,
                    text=PROCESS_DONE_MESSAGE.format(
                        movie_name=details.get('Title') +
                        ' (' + details.get('Year') + ')',
                        review_count=len(reviews),
                        record_id=record_id
                    )
                )
            else:
                await context.bot.edit_message_text(
                    chat_id=processing_message.chat_id,
                    message_id=processing_message.message_id,
                    text=details
                )
        else:
            await update.message.reply_text("Please send a valid movie name.")
    except Exception as e:
        print(f"Error: {e}")


# Main function for bot execution
def main():
    # Initialize the application
    app = ApplicationBuilder().token(settings.telegram_bot).proxy(
        proxy="socks5://127.0.0.1:2080").build()

    # Register command and message handlers
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    try:
        print("Bot is running...")
        app.run_polling()
    except Exception as e:
        print(f"Error running the bot: {e}")


if __name__ == "__main__":
    main()
