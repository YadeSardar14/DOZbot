from flask import Flask,render_template,request,jsonify
from MiniMax import tree,minimax
# from telebot import TeleBot,types
# from Config import TOKEN,AdminID
from bot import WebLost

app = Flask(__name__)
# bot = bot = TeleBot(TOKEN)



# def WebLost(user,dooz):
#     H = [""]*9
#     newkebord = types.InlineKeyboardMarkup(row_width=3)
#     butten = types.InlineKeyboardButton

#     for i in range(9):
#         if dooz[i]==0: H[i] = butten(" ",callback_data=i+1)
#         elif dooz[i]==1: H[i] = butten("🔴",callback_data=i+1)
#         elif dooz[i]==-1: H[i] = butten("🟢",callback_data=i+1)
        
    
#     newkebord.add(*H)
#     bot.send_message(AdminID,str(user),reply_markup=newkebord)



@app.route('/')
def loade():
    return render_template('Dooz.html')

@app.route('/GetAiDoz',methods=['POST'])
def AIproccec():

    dooz = request.get_json()
    parent = tree(dooz,4)
    AIDooz = minimax(parent)
    dooz = AIDooz[1]

    return jsonify({"status": "success", "AIdooz" : dooz})
    


@app.route('/lost',methods=['PoST'])
def Lost():

    data = request.get_json()
    if not data["type"] :
        WebLost(data["userid"],data["dooz"])
    else :
         WebLost(str(data["userid"])+" (TowGame)",data["dooz"])


    return "",204


# if __name__ == "__main__":
#     app.run(debug=False)
