class node:
	def __init__(self,g):
		self.data = g
		self.children = list()
		
#Turn ; X: 1 , Y: -1

def broadcast(g=[0,0,0,0,0,0,0,0,0],turn=1):
	lis = list()
	i=-1
	for ch in range(g.count(0)):
		lis.append(g.copy())
		for h in range(9):
			if  h>i and lis[ch][h]==0:
				lis[ch][h]=turn
				i = h
				break
				
	return lis



def moods(g=[0,0,0,0,0,0,0,0,0],turn=1):
	
	if g.count(0)>3:
		return broadcast(g.copy(),turn)
	else:
		lis = list()
		removedI = -1
		
		insertI = list()
		insertI.append(g.index(0))
		insertI.append(g.index(0,insertI[0]+1))
		insertI.append(g.index(0,insertI[1]+1))
		
		for ch in range(3):
			removedI = g.index(turn,removedI+1)
			for r in insertI:
				lt = g.copy()
				lt[removedI] = 0
				lt[r]=turn
				
				lis.append(lt)
				
		return lis


		
def tree(g,d,turn=1):
		parent = node(g.copy())
		queue = [parent]
		
		x = turn
		y = str()
		
		if x ==1:
			y=-1
		else:
			y=1
			
			
		for n in range(d):
			for _ in range(len(queue)):
				current = queue.pop(0)
				
				if not n%2:
					for ch in moods(current.data,x):
						child = node(ch)
						current.children.append(child)
						queue.append(child)
			
				else:
					for ch in moods(current.data,y):
						child = node(ch)
						current.children.append(child)
						queue.append(child)
			
		return parent		
		

def print_tree(node, level=0):
    if node is None:
        return
    
    print('  ' * level , node.data)
    for child in node.children:
        print_tree(child, level + 1)


		



	