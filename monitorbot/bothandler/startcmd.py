from telegram import Update
from telegram.ext import CommandHandler, CallbackContext


def dispatch(update: Update, context: CallbackContext) -> None:
    pass


def handler() -> CommandHandler:
    return CommandHandler('start', dispatch)
