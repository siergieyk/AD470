from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer


app = Flask(__name__)

bot = ChatBot("Echo")

trainer = ListTrainer(bot)
trainer.train(['what is your name?', 'My name is Echo'])
trainer.train(['who are you?', 'I am a BOT'])

trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english")

@app.route("/")
def index(): 
 return render_template("index.html") 
@app.route("/get")
def get_bot_response(): 
 userText = request.args.get('msg') 
 return str(bot.get_response(userText)) 
if __name__ == "__main__": 
 app.run(host="0.0.0.0",port=80)