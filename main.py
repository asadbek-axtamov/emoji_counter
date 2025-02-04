from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from tinydb import TinyDB, Query
import os



like_count = 0
dislike_count = 0


def start(update: Update, context: CallbackContext):
    global like_count, dislike_count

    photo = open("nature.webp", "rb")

    keyboard = [
        [InlineKeyboardButton(f"👍 {like_count}", callback_data="like"), 
         InlineKeyboardButton(f"👎 {dislike_count}", callback_data="dislike")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_photo(photo=photo, reply_markup=reply_markup)



def query(update: Update, context: CallbackContext):
    global like_count, dislike_count

    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id

    if data == "like":
        like_count += 1
    elif data == "dislike":
        dislike_count += 1

    keyboard = [
        [InlineKeyboardButton(f"👍 {like_count}", callback_data="like"), 
         InlineKeyboardButton(f"👎 {dislike_count}", callback_data="dislike")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.message.edit_reply_markup(reply_markup=reply_markup)
    print(data, chat_id)


    db = TinyDB('db.json', indent = 4)
    User = Query()
    new_response = db.search(User.chat_id == chat_id)

    if not new_response:
        db.insert({"chat_id": chat_id, "data": data})
   

TOKEN = os.getenv("TOKEN")
updater = Updater(TOKEN) 
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(query))

updater.start_polling()
updater.idle()
