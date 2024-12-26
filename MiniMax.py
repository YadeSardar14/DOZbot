from tree import tree,node
from numpy import array


def index(i,j):
	return (i-1)*3+j
	
	
def heuristic(g: list,sy):
	score = list()
	
	row = [g[0],g[4],g[8]]
	column = [g[2],g[4],g[6]]
	
	for i in range(3+1):
		#print(column,row)
		
		if row.count(sy)==1 and row.count(0)==2:
			score.append(5)
		elif row.count(sy)==2 and row.count(0)==1:
			score.append(10)
		elif row.count(sy)==3:
			return 100
			# if sy == 1: return 100
			# else: return 50
			#score.append(10)
			
			
		if column.count(sy)==1 and column.count(0)==2:
			score.append(5)
		elif column.count(sy)==2 and column.count(0)==1:
			score.append(10)
		elif column.count(sy)==3:
			return 100
			# if sy == 1: return 100
			# else: return 50
			#score.append(10)
		
			
		row.clear()
		column.clear()
			
		for j in range(3):
			row.append(g[index(i,j)])
			column.append(g[index(j,i)])
			
		
		
	if score.count(10)>1:
		score.append(25)
		
	return sum(score)




def minimax(root : node,turn=True):
	
	if not root.children:
		#print(root.data)
		#return 0
		score = heuristic(root.data,1)-heuristic(root.data,-1)
		return score,[]
		
	chList = list()
	
	for child in root.children:
		if win_Check(child.data) != 0:
			chList.append((heuristic(child.data,1)-heuristic(child.data,-1),child.data))
			continue	
		chList.append((minimax(child,not turn)[0],child.data))

	
	if turn:
		return  max(chList,key=lambda x: x[0])
	else:
		return  min(chList,key=lambda x: x[0])



def win_Check(g:list):
	dooz = array([g[0:3],g[3:6],g[6:9]])
	for i in dooz:
		if len(set(i)) == 1 and i[0] != 0:
			return i[0]
		
	for i in dooz.T:
		if len(set(i)) == 1 and i[0] != 0:
			return i[0]
		
	if (g[0]==g[4] and g[4]==g[8]) or (g[2]==g[4] and g[4]==g[6] and g[4] != 0):
		return g[4]
	  
	return 0

