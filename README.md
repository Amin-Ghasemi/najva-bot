# Najva Bot
the Robot sending secret messages in Telegram

#### Photos
![image](https://user-images.githubusercontent.com/62441713/120935612-e4668a80-c718-11eb-82da-752e2143f0cd.png)
![image](https://user-images.githubusercontent.com/62441713/120935749-7b334700-c719-11eb-8845-17300b1c3864.png)
![image](https://user-images.githubusercontent.com/62441713/120935630-fa744b00-c718-11eb-8e9d-663e34e04918.png)

## Installation pyrogram
#### Windows
```bash
pip install Pyrogram
```
#### Linux
```bash
pip3 install Pyrogram
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
