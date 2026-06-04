from pyrogram import Client
import config

app = Client("my_bot", config.API_ID, config.API_HASH, 
             session_string=config.STRING, 
             plugins=dict(root="plugins"))

if __name__ == "__main__":
    app.run()
