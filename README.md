# Najva Bot

the Robot sending secret messages in Telegram

## Installation pyrogram
```bash
pip install pyrogram
```
## Create database
```bash
import sqlite3

conn = sqlite3.connect('najva1.db')

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
