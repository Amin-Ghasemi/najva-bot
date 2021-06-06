# Najva Bot

the Robot sending secret messages in Telegram

## Installation pyrogram
```bash
pip install Pyrogram
```
## Create database
```bash
import sqlite3

conn = sqlite3.connect('najva.db')

cur = conn.cursor()

cur.execute("""CREATE TABLE "messages" (
	"message"	TEXT,
	"sender"	INTEGER,
	"receiver"	TEXT,
	"message_id"	TEXT NOT NULL,
	PRIMARY KEY("message_id")
    );
""")
```
