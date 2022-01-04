import time
import datetime

import pyfiglet
import logging
import logging.config
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Poll
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    PollHandler,
)
import telegram
from meal_request_handler import MealRequestHandler
from _model import *

meal_request_handler = MealRequestHandler()
import config_util


def sabji_command_handler(update, context):
    """Send a message when the command /s is issued."""
    meal_command_handler(update, context, 'S')


def dal_command_handler(update, context):
    """Send a message when the command /d is issued."""
    meal_command_handler(update, context, 'D')


def parantha_command_handler(update, context):
    """Send a message when the command /p is issued."""
    meal_command_handler(update, context, 'P')


def breakfast_command_handler(update, context):
    """Send a message when the command /b is issued."""
    meal_command_handler(update, context, 'B')


def meal_command_handler(update, context, meal_type):
    add_typing(update, context)
    meal, ingredients = meal_request_handler.get_random_meal(meal_type)
    if meal:
        meal_suggestion = MealSuggestion()
        meal_suggestion.meal = meal
        meal_suggestion.meal_type = meal_type
        meal_suggestion.ingredients = ingredients.copy()
        meal_suggestion.ingredients.append("accept")
        send_meal_suggestion(update, context, meal_suggestion)
    else:
        add_text_message(update, context, "Yay! Let's order something")


def reset_command_handler(update, context):
    """Send a message when the command /r is issued."""
    meal_request_handler.reset_unavailable_ingredients()


def get_selected_options(update):
    options = update.poll.options
    ret = []
    for option in options:
        if option.voter_count == 1:
            ret.append(option.text)
    return ret


def poll_handler(update, context):
    logging.info(f"suggestion : {update.poll.question}")
    logging.info(f"suggestion : {update.poll.question.split(':')[0]}")
    # logging.info(f"correct option : {update.poll.correct_option_id}")
    # logging.info(f"option #1 : {update.poll.options[0]}")
    # logging.info(f"option #2 : {update.poll.options[1]}")
    # logging.info(f"option #3 : {update.poll.options[2]}")

    selected_options = get_selected_options(update)
    if is_meal_suggestion_accepted(selected_options):
        add_typing(update, context)
        add_text_message(update, context, f"Happy Cooking {update.poll.question.split(':')[1]}")
    else:
        meal_request_handler.add_unavailable_ingredients(selected_options)
        meal_command_handler(update, context, update.poll.question.split(":")[0])


def is_meal_suggestion_accepted(selected_options):
    return "accept" in selected_options


def get_chat_id(update, context):
    chat_id = -1

    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]

    return chat_id


def get_user(update):
    user: User = None

    _from = None

    if update.message is not None:
        _from = update.message.from_user
    elif update.callback_query is not None:
        _from = update.callback_query.from_user

    if _from is not None:
        user = User()
        user.id = _from.id
        user.first_name = _from.first_name if _from.first_name is not None else ""
        user.last_name = _from.last_name if _from.last_name is not None else ""
        user.lang = _from.language_code if _from.language_code is not None else "n/a"

    logging.info(f"from {user}")

    return user


def help_command_handler(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Type "
                              "/s for sabji suggestion \n "
                              "/p for parantha suggestion \n "
                              "/d for dal suggestion \n "
                              "/b for breakfast suggestion \n "
                              "/r for reset")


def new_member(update, context):
    logging.info(f"new_member : {update}")

    add_typing(update, context)
    add_text_message(update, context, f"New user")


def main_handler(update, context):
    logging.info(f"update : {update}")

    if update.message is not None:
        user_input = get_text_from_message(update)
        logging.info(f"user_input : {user_input}")

        # reply
        add_typing(update, context)
        add_text_message(update, context, f"You said: {user_input}")


def add_typing(update, context):
    context.bot.send_chat_action(
        chat_id=get_chat_id(update, context),
        action=telegram.ChatAction.TYPING,
        timeout=1,
    )
    time.sleep(1)


def add_text_message(update, context, message):
    context.bot.send_message(chat_id=get_chat_id(update, context), text=message)


def send_meal_suggestion(update, context, meal_suggestion):
    message = context.bot.send_poll(
        chat_id=get_chat_id(update, context),
        question=meal_suggestion.meal_type + ":" + meal_suggestion.meal,
        options=meal_suggestion.ingredients,
        type=Poll.REGULAR,
        allows_multiple_answers=True,
        correct_option_id=meal_suggestion.accept_position,
        open_period=300,
        is_anonymous=True,
        explanation="With love",
        explanation_parse_mode=telegram.ParseMode.MARKDOWN_V2,
    )

    # Save some info about the poll the bot_data for later use in receive_quiz_answer
    context.bot_data.update({message.poll.id: message.chat.id})


def get_text_from_message(update):
    return update.message.text


def get_text_from_callback(update):
    return update.callback_query.data


def error(update, context):
    """Log Errors caused by Updates."""
    logging.warning('Update "%s" ', update)
    logging.exception(context.error)


def main():
    updater = Updater(DefaultConfig.TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    # command handlers
    dp.add_handler(CommandHandler("help", help_command_handler))
    dp.add_handler(CommandHandler("s", sabji_command_handler))
    dp.add_handler(CommandHandler("d", dal_command_handler))
    dp.add_handler(CommandHandler("b", breakfast_command_handler))
    dp.add_handler(CommandHandler("p", parantha_command_handler))
    dp.add_handler(CommandHandler("r", reset_command_handler))

    # message handler
    dp.add_handler(MessageHandler(Filters.text, main_handler))

    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))

    # suggested_actions_handler
    dp.add_handler(
        CallbackQueryHandler(main_handler, pass_chat_data=True, pass_user_data=True)
    )

    # quiz answer handler
    dp.add_handler(PollHandler(poll_handler, pass_chat_data=True, pass_user_data=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    if DefaultConfig.MODE == "webhook":

        updater.start_webhook(
            listen="0.0.0.0",
            port=int(DefaultConfig.PORT),
            url_path=DefaultConfig.TELEGRAM_TOKEN,
        )
        updater.bot.setWebhook(DefaultConfig.WEBHOOK_URL + DefaultConfig.TELEGRAM_TOKEN)

        logging.info(f"Start webhook mode on port {DefaultConfig.PORT}")
    else:
        updater.start_polling()
        logging.info(f"Start polling mode")

    updater.idle()


class DefaultConfig:
    PORT = int(os.environ.get("PORT", 3978))
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", config_util.read_telegram_bot_token())
    MODE = os.environ.get("MODE", "polling")
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")

    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

    @staticmethod
    def init_logging():
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=DefaultConfig.LOG_LEVEL,
        )


if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("SampleTelegramQuiz")
    print(ascii_banner)

    # Enable logging
    DefaultConfig.init_logging()

    main()
