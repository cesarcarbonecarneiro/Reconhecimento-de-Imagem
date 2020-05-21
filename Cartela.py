import cv2
import numpy as np
import re

class Cartela:
	telefone=None
	aposta=None
	imagem=None
	temp1x=None
	temp1y=None
	temp2x=None
	temp2y=None
	temp3x=None
	temp3y=None
	temp4x=None
	temp4y=None
	temp5x=None
	temp5y=None
	temp6x=None
	temp6y=None
	temp7x=None
	temp7y=None
	temp8x=None
	temp8y=None
	cart1=False
	cart2=False
	qt1=110
	qt2=60
	conttel=[0]*qt1
	contapo=[0]*qt2
	modtel=[[80,40,50,60,50,40,50,50,50,40],[60,40,50,50,40,40,40,40,40,40],[50,40,40,40,40,40,40,40,40,40],[50,40,40,40,40,40,40,40,40,40],[50,40,40,40,40,40,40,40,40,40],[50,40,40,40,40,40,40,40,40,40],[60,40,40,40,40,40,40,40,40,40],[60,60,50,40,40,40,40,40,40,50],[70,50,50,40,40,40,40,40,40,50],[80,60,60,50,40,50,50,40,50,60],[120,110,90,70,70,60,60,50,70,80]]
	modapo=[[40,60,70,90,120,140],[40,60,70,90,100,120],[40,70,70,90,100,120],[40,70,70,90,100,110],[40,70,70,80,100,110],[50,60,60,70,90,80],[40,60,70,90,110,90],[50,80,80,110,120,130],[50,80,90,120,140,140],[100,110,110,140,170,160]]
    
	def __init__(self, img):
		self.imagem=img
		self.localizartemp1()
		self.localizartemp2()
		self.localizartemp3()
		self.localizartemp4()
		self.localizartemp5()
		self.localizartemp7()
		self.localizartemp8()
		self.filtro()
		self.telefone=self.tel()
		self.aposta=self.aps()
		#cv2.imshow("foto",self.imagem)

	def teste_precisao(self):
		#print("temp8x: ",self.temp8x[0]," temp8y: ",self.temp8y[0]," temp1x: ",self.temp1x[0]," temp1y: ",self.temp1y[0])
		if((self.temp8x[0]<=501 and self.temp8x[0]>=480) and (self.temp1x[0]<=137 and self.temp1x[0]>=116) and (self.temp8y[0]<=315 and self.temp8y[0]>=298) and (self.temp1y[0]<=31 and self.temp1y[0]>=15)):
			return True
		else:
			return False
		
        
	def localizartemp1(self):
		img = self.imagem
		gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		template=cv2.imread('temp1.png',cv2.IMREAD_GRAYSCALE)
		w,h=template.shape[::-1]
		r,c=template.shape[::-1]
		result=cv2.matchTemplate(gray_img,template,cv2.TM_CCOEFF_NORMED)
		loc=np.where(result>=0.9)
		tamLoc = len(loc[0])
		self.temp1x=loc[1]
		self.temp1y=loc[0]

	def localizartemp2(self):
		img = self.imagem
		gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		template=cv2.imread('temp2.png',cv2.IMREAD_GRAYSCALE)
		w,h=template.shape[::-1]
		r,c=template.shape[::-1]
		result=cv2.matchTemplate(gray_img,template,cv2.TM_CCOEFF_NORMED)
		loc=np.where(result>=0.9)
		tamLoc = len(loc[0])
		self.temp2x=loc[1]
		self.temp2y=loc[0]

	def localizartemp3(self):
		img = self.imagem
		gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		template=cv2.imread('temp3.png',cv2.IMREAD_GRAYSCALE)
		w,h=template.shape[::-1]
		r,c=template.shape[::-1]
		result=cv2.matchTemplate(gray_img,template,cv2.TM_CCOEFF_NORMED)
		loc=np.where(result>=0.9)
		tamLoc = len(loc[0])
		self.temp3x=loc[1]
		self.temp3y=loc[0]
	

	def localizartemp4(self):
		img = self.imagem
		gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		template=cv2.imread('temp4.png',cv2.IMREAD_GRAYSCALE)
		w,h=template.shape[::-1]
		r,c=template.shape[::-1]
		result=cv2.matchTemplate(gray_img,template,cv2.TM_CCOEFF_NORMED)
		loc=np.where(result>=0.9)
		tamLoc = len(loc[0])
		self.temp4x=loc[1]
		self.temp4y=loc[0]

	def localizartemp5(self):
		img = self.imagem
		gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		template=cv2.imread('temp5.png',cv2.IMREAD_GRAYSCALE)
		w,h=template.shape[::-1]
		r,c=template.shape[::-1]
		result=cv2.matchTemplate(gray_img,template,cv2.TM_CCOEFF_NORMED)
		loc=np.where(result>=0.9)
		tamLoc = len(loc[0])
		self.temp5x=loc[1]
		self.temp5y=loc[0]

	def localizartemp7(self):
		img = self.imagem
		gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		template=cv2.imread('temp7.png',cv2.IMREAD_GRAYSCALE)
		w,h=template.shape[::-1]
		r,c=template.shape[::-1]
		result=cv2.matchTemplate(gray_img,template,cv2.TM_CCOEFF_NORMED)
		loc=np.where(result>=0.9)
		tamLoc = len(loc[0])
		self.temp7x=loc[1]
		self.temp7y=loc[0]

	def localizartemp8(self):
		img = self.imagem
		gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		template=cv2.imread('temp8.png',cv2.IMREAD_GRAYSCALE)
		w,h=template.shape[::-1]
		r,c=template.shape[::-1]
		result=cv2.matchTemplate(gray_img,template,cv2.TM_CCOEFF_NORMED)
		loc=np.where(result>=0.9)
		tamLoc = len(loc[0])
		self.temp8x=loc[1]
		self.temp8y=loc[0]

	def filtro(self):
		self.imagem[:,:,0]=0
		self.imagem[:,:,1]=0
		#cv2.imwrite('teste3.png',self.imagem)

	def tel(self):
		tamLoc = len(self.temp1x)
		#print ('telefone')
		if tamLoc > 0:
			self.cart1=True
			tam=11
			V=[0]*tam
			linha=[0]*10
			contcont=0
			for c in range(1,12):
				vazio=True
				poli=0
				for l in range (1,11):
					if (l>5 and c<=6):
						x=(33*(c-1))+self.temp2x[0]+42
						y=(20*(l-6))+self.temp2y[0]-35
						cont=0
					else:
						if(l<=5 and c<=6):
							x=(33*(c-1))+self.temp1x[0]+42
							y=(20*(l-1))+self.temp1y[0]+2
							cont=0
						else:
							if (l<=5 and c>6):
								x=(33*(c-7))+self.temp5x[0]-158
								y=(20*(l-1))+self.temp5y[0]+5
								cont=0
							else:
								if (l>5 and c>6):
									x=(33*(c-7))+self.temp7x[0]-128
									y=(20*(l-6))+self.temp7y[0]-112
									cont=0
                                
					for i in range(y,y+11):
						for  j in range(x,x+18):
							#self.imagem.itemset((i,j,1),25)
							#self.imagem.itemset((i,j,2),55)
							#self.imagem.itemset((i,j,0),155)
							if (self.imagem.item(i,j,2)<=200):
								cont=cont+1 
					#print(cont)
					self.conttel[contcont]=cont
					contcont=contcont+1
					if (cont>self.modtel[c-1][l-1]):
						V[c-1]=l-1
						vazio=False
						poli=poli+1
				#print(V)
				if (poli>1):
					n=-1
					return n
				if(vazio==True):
					n=0
					return 0
			if(V[0]==0):
				n=-2
				return n        
			n=(V[0])*(10000000000)+(V[1])*(1000000000)+(V[2])*100000000+(V[3])*10000000+(V[4])*1000000+(V[5])*100000+(V[6])*10000+(V[7])*1000+(V[8])*100+(V[9])*10+(V[10])*1                  
			return n
        

    
	def aps(self):
		tamLoc = len(self.temp3x)
		#print('aposta')
		if (tamLoc>0):
			self.cart2=True
			tam=11
			V=[0]*tam
			pos=0
			contcont=0
			for c in range(1,11):
				for l in range (1,7):
					if (l<=3 and c<=5):
						x=(34*(c-1))+self.temp3x[0]+40
						y=(22*(l-1))+self.temp3y[0]+6
						cont=0
					else:
						if(l>3 and c<=5):
							x=(34*(c-1))+self.temp4x[0]+40
							y=(22*(l-4))+self.temp4y[0]+6
							cont=0
						else:
							if(l<=3 and c>5):
								x=(34*(c-6))+self.temp7x[0]-160
								y=(22*(l-1))+self.temp7y[0]+8
								cont=0
							else:
								if(l>3 and c>5):
									x=(34*(c-6))+self.temp8x[0]-160
									y=(22*(l-4))+self.temp8y[0]+6
									cont=0

					for i in range(y,y+11):
						for j in range(x,x+18):
							#self.imagem.itemset((i,j,1),25)
							#self.imagem.itemset((i,j,2),55)
							#self.imagem.itemset((i,j,0),155)
							if (self.imagem.item(i,j,2)<=200):
								cont=cont+1
					#print (cont)
					self.contapo[contcont]=cont
					contcont=contcont+1
					if(cont>self.modapo[c-1][l-1] and pos<11):
						V[pos]=(c+(l-1)*10)
						pos=pos+1
                        
			if (pos<10):
				n=0
				return n
			if (pos>10):
				n=-1
				return n   
			V1=[0]*10
			#Ordenação crescente            
			for i in range (0,10):
				for j in range(i+1,11):
					if(V[i]>V[j]):
						x=V[i]
						V[i]=V[j]
						V[j]=x 
			for i in range (0,10):
				V1[i]=V[i+1]   
			#print(V1)
			return V1
    
    
    
    
    
		 
    
    
    
    
    
    
    
    