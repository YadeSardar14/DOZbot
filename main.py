from bot import bot
from app import app
from threading import Thread

def RunBot():
	bot.infinity_polling()
      
def RunApp():
    app.run(debug=False)

if __name__ == "__main__":
    Thread(target=RunBot).start()
    Thread(target=RunApp).start()

