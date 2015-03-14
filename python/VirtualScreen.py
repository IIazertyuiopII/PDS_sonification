import math

class VirtualScreen: #cet ecran est normal a l'axe Z du Leap
	
	def __init__(self,Xoffset=0,Yoffset=50,Zoffset=-50,Zlimit=220,length=350,height=300): #en mm
		
		self.Xoffset = Xoffset; # position du milieu du bord bas de l'ecran par rapport au centre du Leap
		self.Yoffset = Yoffset; # position du milieu du bord bas de l'ecran par rapport au centre du Leap
		self.Zoffset = Zoffset; # position du milieu du bord bas de l'ecran par rapport au centre du Leap

		self.Zlimit = Zlimit # profondeur de la zone

		self.length = length;
		self.height = height;

		self.UpperLeftCorner = [Xoffset-length/float(2),Yoffset+height]

		self.Center = [self.Xoffset,self.Yoffset+0.5*self.height,Zoffset+0.5*Zlimit]

		self.zoneUpperLeftCornerArray = [];
		self.zoneHeight = height / float(2);
		self.zoneLength = length / float(3);

		for i in range(0,2):
			for j in range(0,3):
				self.zoneUpperLeftCornerArray.append([self.UpperLeftCorner[0]+self.zoneLength*j,self.UpperLeftCorner[1]-self.zoneHeight*i])

		# print self.zoneUpperLeftCornerArray

	def distanceFromScreen(self,position):
		dX = max( max( position[0] - (self.Xoffset+self.length/float(2)), 0 ) , max (self.Xoffset-self.length/float(2) - position[0], 0 ) )
		dY = max( max( position[1] - (self.Yoffset+self.height) , 0 ) , max (self.Yoffset - position[1], 0 ) )
		dZ = max( max(self.Zoffset - position[2], 0 ) , max(position[2] - (self.Zlimit + self.Zoffset) , 0 ) )
		return math.sqrt(dX**2+dY**2+dZ**2) 

	def isFacingTheScreen(self,position): #donner un vecteur position 3d en mm suivant les axes du Leapmotion ([x,y,z])
		isXvalid = (position[0] <= self.Xoffset+self.length/float(2)) and (position[0] >= self.Xoffset-self.length/float(2))
		isYvalid = (position[1] <= self.Yoffset+self.height) and (position[1] >= self.Yoffset)
		isZvalid = (position[2] >= self.Zoffset) and (position[2] <= self.Zlimit + self.Zoffset)
		return isXvalid and isYvalid and isZvalid

	def getScreenZonePointedAt(self,position,direction):
		if not self.isFacingTheScreen(position):
			return -1
		else:
			lambdaIntersection = (self.Zoffset-position[2])/direction[2] # (Zoffset-Zpoint)/Zdirecteur 
			xIntersection = position[0] + lambdaIntersection*direction[0] # Xpoint + lambda * Xdirecteur
			yIntersection = position[1] + lambdaIntersection*direction[1] # Ypoint + lambda * Ydirecteur
			intersection = [xIntersection,yIntersection]
			return(self.getScreenZoneFromPointOnScreen(intersection))


	def getScreenZoneFromPointOnScreen(self,onScreenPosition):
		for index,i in enumerate(self.zoneUpperLeftCornerArray):
			if(onScreenPosition[0]>=i[0] and onScreenPosition[0]<i[0]+self.zoneLength and onScreenPosition[1]<=i[1] and onScreenPosition[1]>=i[1]-self.zoneHeight):
				return index+1
		return -1

