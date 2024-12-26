from MiniMax import tree,minimax,win_Check
from telebot import types,TeleBot
from telebot.types import WebAppData,WebAppInfo
from json import load,dump
from Config import TOKEN,AdminID

turn = False
RePlace = False
dooz = [0,0,0,0,0,0,0,0,0]
startfill = False
log_kebords =[]
current_doz_id = 0
LastUser = 0

Users : list

try:
	with open("Users.json","r") as users:
		Users = load(users)
except:
		Users =[]


bot = TeleBot(TOKEN)


butten = types.InlineKeyboardButton
DefultHome = [butten(" ",callback_data=1),butten(" ",callback_data=2),butten(" ",callback_data=3),butten(" ",callback_data=4),butten(" ",callback_data=5),butten(" ",callback_data=6),butten(" ",callback_data=7),butten(" ",callback_data=8),butten(" ",callback_data=9)]

kebord = types.InlineKeyboardMarkup(row_width=3)

class Dooz:
	def __init__(self,id,dooz=dooz.copy(),Homes=DefultHome.copy(), current_doz_id = current_doz_id) :
		self.id = id
		self.dooz = dooz
		self.Homes = Homes
		self.kebord = types.InlineKeyboardMarkup(row_width=3)
		self.kebord.add(*self.Homes)
		
				
		self.turn = turn
		self.RePlace = RePlace
		self.current_doz_id = current_doz_id

	
DoozList = list()


# kebord_turn =  types.InlineKeyboardMarkup(row_width=2)
# kebord_turn.add(butten("Me",callback_data="turn_me"),butten("AI",callback_data="turn_ai"))



def WebLost(user,dooz):
    H = DefultHome.copy()
    newkebord = types.InlineKeyboardMarkup(row_width=3)
    for i in range(9):
        if dooz[i]==0: H[i] = butten(" ",callback_data=i+1)
        elif dooz[i]==1: H[i] = butten("🔴",callback_data=i+1)
        elif dooz[i]==-1: H[i] = butten("🟢",callback_data=i+1)
        
    
    newkebord.add(*H)
    bot.send_message(AdminID,str(user),reply_markup=newkebord)


def UserShow(user):
	global Users

	if not user.id in Users:
		Users.append(user.id)
		bot.send_message(AdminID,f"New User:\n\nFN: {user.first_name}\nLN: {user.last_name}\nUN: @{user.username}\nID: {user.id}")

	try:
		with open("Users.json","w") as users:
			dump(Users,users)
	except:
		pass


def UpdateDoz(dooz : Dooz):
	global kebord

	for i in range(9):
		if dooz.dooz[i]==0: dooz.Homes[i] = butten(" ",callback_data=i+1)
		elif dooz.dooz[i]==1: dooz.Homes[i] = butten("🔴",callback_data=i+1)
		elif dooz.dooz[i]==-1: dooz.Homes[i] = butten("🟢",callback_data=i+1)

	dooz.kebord = types.InlineKeyboardMarkup(row_width=3)
	dooz.kebord.add(*dooz.Homes)

def ClaerDoz(index):
	global kebord
	del DoozList[index]
	kebord = types.InlineKeyboardMarkup(row_width=3)


def UserChoiceProcess(game : Dooz,home,i,game_index):
	global startfill,DoozList
	
	chat_id = home.message.chat.id
	message_id = home.message.message_id

	if game.dooz.count(0)==3 and not game.RePlace:
		if game.dooz[i] != -1:
			bot.answer_callback_query(home.id,text='شما میتوانید یکی از مهره های خود را جا به جا کنید.',show_alert=True)
		else:
			game.dooz[i] = 0
			UpdateDoz(game)
			bot.edit_message_text("DooooooooooooooZ",chat_id,message_id,reply_markup=game.kebord)
			game.RePlace = True

		return 0

	if game.dooz[i] != 0:
		bot.answer_callback_query(home.id,text='یکی از خانه های خالی را انتخاب کنید.',show_alert=True)
		return 0

	game.dooz[i] = -1
	UpdateDoz(game)
	bot.edit_message_text("DooooooooooooooZ",chat_id,message_id,reply_markup=game.kebord)
	game.RePlace = False
	
	if win_Check(game.dooz) != 0:
		log_kebords.append(game.kebord)
		ClaerDoz(game_index)
		bot.edit_message_text("YooooooooooU WIN!",chat_id,message_id,reply_markup=log_kebords[-1])
		bot.send_message(AdminID,f"@{home.from_user.username} WIN!",reply_markup=log_kebords[-1])
		
	game.turn = True
	startfill = False


def AIChoiceProcess(game : Dooz ,chat_id,message_id, game_index ,username=""):
		
		parent = tree(game.dooz,4)
		AIDooz = minimax(parent)
		game.dooz = AIDooz[1]
		UpdateDoz(game)
		bot.edit_message_text("DooooooooooooooZ",chat_id,message_id,reply_markup=game.kebord)
		
		if win_Check(game.dooz) != 0:
			log_kebords.append(game.kebord)
			ClaerDoz(game_index)
			bot.edit_message_text("YooooooooooU LOST!",chat_id,message_id,reply_markup=log_kebords[-1])
			bot.send_message(AdminID,f"@{username} LOST!",reply_markup=log_kebords[-1])

		game.turn = False


#-----------------------------------

@bot.message_handler(commands=["start"])
def  startation(message):
	global startfill,LastUser

	if message.chat.id != LastUser: startfill = False
	if not startfill:
		kebord_turn =  types.InlineKeyboardMarkup(row_width=2)
		kebord_turn.add(butten("Me",callback_data="turn_me"),butten("AI",callback_data="turn_ai"))
		kebord_turn.add(butten(text="Game",web_app=WebAppInfo(url=f"https://testaccount1.pythonanywhere.com?userid={message.chat.id}")))
		
		bot.send_message(message.chat.id,"اولین حرکت:           \u200c",reply_markup=kebord_turn)
		startfill = True
		LastUser = message.chat.id
		UserShow(message.from_user)



@bot.callback_query_handler(func=lambda call: call.data.startswith('turn'))
def TurnProcess(call):
	global DoozList,kebord
	
	try :
		index = next((index for index, obj in enumerate(DoozList) if obj.id == call.message.chat.id))
		ClaerDoz(index)
	except:
		pass

	if call.data == "turn_me" :
		kebord = types.InlineKeyboardMarkup(row_width=3)
		kebord.add(*DefultHome)
	doz = bot.send_message(call.message.chat.id,"DoooooooooooZ",reply_markup=kebord)
	ob = Dooz(id=call.message.chat.id,current_doz_id= doz.message_id,dooz= dooz.copy())
	# current_doz_id = doz.message_id

	try:
		bot.delete_message(doz.chat.id,doz.message_id-1)
	except:
		pass

	if call.data=="turn_me":
		ob.turn = False
	elif call.data=="turn_ai":
		ob.turn = True
		
		AIChoiceProcess(ob,doz.chat.id,doz.message_id,None)
		ob.turn = False

	
	DoozList.append(ob)


@bot.callback_query_handler()
def Processing(home):
	global turn,dooz,RePlace
	# text = "D🔴🔴🔴🔴🔴🔴Z" if turn else  "D🟢🟢🟢🟢🟢🟢Z"
	
	try :
		index = next((index for index, obj in enumerate(DoozList) if obj.id == home.message.chat.id))
		game : Dooz = DoozList[index]
	except:
		return
	

	if home.message.message_id== game.current_doz_id and not game.turn:
		i = int(home.data)-1
		if UserChoiceProcess(game,home,i,game_index= index)==0: return
		AIChoiceProcess(game,home.message.chat.id,home.message.message_id,username=home.from_user.username,game_index= index)



# bot.infinity_polling()
      


