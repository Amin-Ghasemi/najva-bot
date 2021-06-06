import sqlite3
import hashlib
from datetime import datetime
from pyrogram import Client
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            InlineQueryResultArticle,InputTextMessageContent)

# _ client _
app = Client("najva",
            api_id="",
            api_hash="",
            bot_token="",
            )
# __________

@app.on_callback_query()
async def get(_:app, query):
    if query.data == "#":
        await app.answer_callback_query(query.id, "پیغام ها پس از خوانده شدن به صورت خودکار نابود میشوند 👁‍🗨")
    else:
        try:
            conn = sqlite3.connect('najva.db')
            cur = conn.cursor()
            cur.execute(f'''SELECT * FROM messages WHERE message_id = "{query.data}"''')

            All = cur.fetchall()
            message = All[0][0]
            sender = All[0][1]
            receiver = All[0][2]

            username = query.from_user.username.lower()

            if query.from_user.id == int(sender):
                await app.answer_callback_query(query.id, message, show_alert=True)

            elif username == receiver.lower() or int(query.from_user.id) == int(receiver):
                await app.answer_callback_query(query.id, message, show_alert=True)
                await app.edit_inline_reply_markup(query.inline_message_id, reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(text="خوانده شد ✅", callback_data="#")
                        ],
                    ]
                    )
                )
                cur.execute(f'''DELETE FROM messages WHERE message_id = "{query.data}"''')

            else:
                await app.answer_callback_query(query.id, "شرمنده، نمیتونی پیغام بقیه رو بخونی :)")
            
            if username[0] == '@':
                username[0] = str(username[0]).replace("@", "")

            
            conn.commit()
            conn.close()

        except ValueError as e:
            print(e)


SCROLL_THUMB = "https://i.imgur.com/L1u0VlX.png"

@app.on_inline_query()
def answer(client, query):
    # _ Delete '@' from username _
    receiver = str(query.query).split(" ")[0]
    receiver = receiver.replace("@", "")
    receiver = receiver
    # ____________________________

    sender = query.from_user.id

    try:
        message = str(query.query).replace(receiver, "").replace("@", "")

        # _ Create hash for message id _
        message_id = str(hashlib.md5(str(receiver+message+datetime.now().strftime("%H%m%S%D")).encode('utf-8')).hexdigest())
        # ______________________________

        conn = sqlite3.connect('najva.db')
        cur = conn.cursor()

        # _ Delete empty messages _
        cur.execute(f'''DELETE FROM messages where message=""''')
        # _________________________

        cur.execute("""INSERT INTO messages(message, sender ,receiver, message_id) 
                VALUES (?,?,?,?);""", (str(message), int(sender) ,str(receiver), str(message_id)))
        conn.commit()
        conn.close()

        query.answer(

            results=[

                InlineQueryResultArticle(
                    title=f"💬 : {message}",
                    input_message_content=InputTextMessageContent(f"یک پیغام محرمانه برای {receiver} 🕵🏻‍♂️!"),
                    url="",
                    description=f"receiver : {receiver}\nsender : {sender}",
                    thumb_url=SCROLL_THUMB,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                            InlineKeyboardButton(
                                "خواندن پیغام 👀",
                                callback_data=message_id,
                            ),
                            ]
                        ]
                    )
                ),
            ],
            cache_time=1
        )
    except ValueError as e:
        print(e)

app.run()