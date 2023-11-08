class molecule:
    def __init__(self, location, radius):
        self.location = location
        self.radius = radius
        self.text = None
        self.show = True
        
    def setLocation(self, loco):
        if loco[0] < 0:
            loco = (0, loco[1])
        if loco[0] > 800:
            loco = (800, loco[1])
        if loco[1] < 0:
            loco = (loco[0], 0)
        if loco[1] > 800:
            loco = (loco[0], 800)       
        self.location = loco
        
class moleculeArr:
    def __init__(self, start, radius):
        self.array = []
        self.strtLoco = start
        self.rad = radius
        self.links = {}
    def addMolecule(self):
        newMol = molecule(self.strtLoco, self.rad)
        self.array.append(newMol)
    def deleteMol(self, ind):
        self.array[ind].show = False
        for n in self.links:
            if ind in self.links[n]:
                self.links[n].remove(ind)
        if ind in self.links:
            del self.links[ind]
        
    def checkCollisions(self, mouse_x, mouse_y):
        for i in range(len(self.array)):
            distance = ((mouse_x - self.array[i].location[0])**2 + (mouse_y - self.array[i].location[1])**2)**0.5
            if distance <= self.array[i].radius:
                return i
        return -1
    def checkCollision(self, ind, mouse_x, mouse_y):
        distance = ((mouse_x - self.array[ind].location[0])**2 + (mouse_y - self.array[ind].location[1])**2)**0.5
        if distance <= self.array[ind].radius:
            return True
        return False
    def setMolLocation(self, ind, mouse_pos):
        self.array[ind].setLocation(mouse_pos)
    def createLink(self, node1, node2):
        if node1 not in self.links:
            self.links[node1] = set()
        if node2 not in self.links:
            self.links[node2] = set()     
                  
        self.links[node1].add(node2)
        self.links[node2].add(node1)
    def deleteLink(self, node1, node2):
        if node1 not in self.links or node2 not in self.links or node2 not in self.links[node1] or node1 not in self.links[node2]:
            return
        self.links[node1].remove(node2)
        self.links[node2].remove(node1)
    def changeText(self, ind, newText):
        self.array[ind].text = newText
        
        
        