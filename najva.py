import sqlite3
from hashlib import md5
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
        conn = sqlite3.connect('najva.db')
        cur = conn.cursor()
        cur.execute(f'''SELECT * FROM messages WHERE message_id = "{query.data}"''')

        All = cur.fetchall()
        message = All[0][0]
        sender = All[0][1]
        receiver = All[0][2]
        username = query.from_user.username.lower()

        # _ Validation username or user id _
        try:
            getChatId = await app.get_chat(f"{receiver}")
            getChatId = str(getChatId.id).replace(" ", "")
            getChatId = int(getChatId)
        except:
            getChatId = None
        # __________________________________

        if getChatId == None:
            await app.answer_callback_query(query.id, "ایدی یا یوزرنیم وارد شده نامعتبر است!")

        else:
            if getChatId == query.from_user.id:
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
                conn.commit()
                conn.close()

            elif query.from_user.id == sender:
                await app.answer_callback_query(query.id, message, show_alert=True)

            else:
                await app.answer_callback_query(query.id, "شرمنده نمیتونم این پیغام رو بهت نشون بدم :)")

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
        message_id = str(md5(str(receiver+message+datetime.now().strftime("%H%m%S%D")).encode('utf-8')).hexdigest())
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
    except:
        pass

app.run()
