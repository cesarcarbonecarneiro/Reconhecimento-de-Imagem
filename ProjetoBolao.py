import sys
import cv2
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer,QCoreApplication,QRect
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtWidgets import QApplication, QDialog,QMessageBox,QToolTip,QWidget,QPushButton,QLineEdit,QInputDialog,QMainWindow
from PyQt5.uic import loadUi
from Cartela import Cartela
import os
import csv
from datetime import date

class WebCam(QMainWindow):
    rows=[]
    file=None
    writer=None
    nomeArquivo=None
    def __init__(self):
        super(WebCam,self).__init__()
        loadUi('mainBolao.ui',self)
        self.auxcal=False
        self.auxrep=False
        self.aux=True
        self.auxstart=True
        self.imagem=None
        self.usuario=None
        self.ligar.clicked.connect(self.start_webcam) 
        self.desligar.clicked.connect(self.stop_webcam)
        self.capturar.clicked.connect(self.tirar_foto)
        self.adicionar.clicked.connect(self.mesmo_usuario)
        self.calibrar.clicked.connect(self.verificar_calibragem)
        self.comentarios_botoes()
        self.iniciar_icones()
        self.iniciar_labels()
        self.msgstatus.setText("Ligue a Web Cam para iniciar o sistema")

    def verificar_calibragem(self):
        if(self.auxcal==True):
            cv2.imwrite('teste2.png',self.imagem)
            imagemteste=cv2.imread("teste2.png",1)
            img=cv2.flip(imagemteste,1)
            cv2.imwrite('teste2.png',img)
            c=Cartela(img)
            if(c.cart1==True and c.cart2==True):
                if(c.teste_precisao()==False):
                    self.msgstatus.setText("Erro de calibragem, \nprocure deixar a borda demarcada em volta da cartela vazia")
                else:
                    self.msgstatus.setText("Cartela calibrada com Sucesso")
                    self.aux=False
            else:
                self.msgstatus.setText("Não foi detectada a presença de uma cartela")
        else:
            self.msgstatus.setText("Necessário ligar a Webcam")
                    


    def comentarios_botoes(self):
        self.ligar.setToolTip("Iniciar a Webcam")
        self.adicionar.setToolTip("Adicionar mais de uma aposta para um único jogador")
        self.capturar.setToolTip("Tirar foto da cartela")
        self.desligar.setToolTip("Salvar e Sair")
        self.calibrar.setToolTip("Verifica a calibragem da câmera")
        
    def iniciar_icones(self):
        self.ligar.setIcon(QtGui.QIcon("only.png"))
        self.desligar.setIcon(QtGui.QIcon("off.png"))
        self.capturar.setIcon(QtGui.QIcon("bola.jpg"))
        self.adicionar.setIcon(QtGui.QIcon("usuario.png"))
        self.calibrar.setIcon(QtGui.QIcon("camera.png"))
        self.ligar.setIconSize(QtCore.QSize(50,50))
        self.desligar.setIconSize(QtCore.QSize(40,40))
        self.capturar.setIconSize(QtCore.QSize(40,40))
        self.adicionar.setIconSize(QtCore.QSize(40,40))
        self.calibrar.setIconSize(QtCore.QSize(40,40))

    def iniciar_labels(self):
        self.telefone.setText('')
        self.aposta.setText('')
        self.telefone2.setText('')
        self.aposta2.setText('')
        self.telefone3.setText('')
        self.aposta3.setText('')
        self.telefone4.setText('')
        self.aposta4.setText('')
        self.telefone5.setText('')
        self.aposta5.setText('')
        self.msgstatus.setText('')
        
    def rodar_labels(self,c):
        self.telefone5.setText(str(self.telefone4.text()))
        self.telefone4.setText(str(self.telefone3.text()))
        self.telefone3.setText(str(self.telefone2.text()))
        self.telefone2.setText(str(self.telefone.text()))
        self.telefone.setText(str(c.telefone))
        self.aposta5.setText(str(self.aposta4.text()))
        self.aposta4.setText(str(self.aposta3.text()))
        self.aposta3.setText(str(self.aposta2.text()))
        self.aposta2.setText(str(self.aposta.text()))   
        self.aposta.setText(str(c.aposta).replace("[","").replace("]",""))
        
    def mesmo_usuario(self):
        if(self.auxrep==True):
            if (self.aux==False):
                cv2.imwrite('teste2.png',self.imagem)
                img=cv2.imread("teste2.png",1)
                img=cv2.flip(img,1)
                c=Cartela(img)
                c.telefone=self.usuario
                self.rows = []
                if(c.cart1==True and c.cart2==True):
                    if(c.telefone>0 and type (c.aposta) is list):
                        self.rodar_labels(c)
                        self.msgstatus.setText("Aposta cadastrada com Sucesso!")
                        f = open(self.nomeArquivo, "a")
                        f.write(str(c.telefone) + ";")
                        row = []
                        row.append(str(c.telefone))
                        for i in range (0,9):
                            f.write(str(c.aposta[i]) + ";")
                            row.append(str(c.aposta[i]))
                        f.write(str("\n"))
                        self.rows.append(row)
                        self.usuario=c.telefone
                    else:
                        if(c.telefone>0):
                            if (c.aposta==0):
                                self.msgstatus.setText("Aposta: \nfoi detecado um total de apostas inferior a 10 números")
                                self.mensagem_erro()
                            else:
                                self.msgstatus.setText("Aposta: \nfoi detectado um total de apostas superior a 10 números")
                                self.mensagem_erro()
                        else:
                            if(c.telefone==0):
                                if(type(c.aposta) is list):
                                    self.msgstatus.setText("Celular: \nColuna(s) vazia(s) foram detectadas")
                                    self.mensagem_erro()
                                else:
                                    if(c.aposta==-1):
                                        self.msgstatus.setText("Celular: \nColuna(s) vazia(s) foram detectadas \nAposta: \nfoi detectado um total de apostas superior a 10 números")
                                        self.mensagem_erro()
                                    else:
                                        self.msgstatus.setText("Celular: \nColuna(s) vazia(s) foram detectadas \nAposta: \nfoi detectado um total de apostas inferior a 10 números")
                                        self.mensagem_erro()
                            else:
                                if(c.telefone==-1):
                                    if(type(c.aposta) is list):
                                        self.msgstatus.setText("Celular: \nColuna(s) com mais de um número assinalado foi detectada")
                                        self.mensagem_erro()
                                    else:
                                        if(c.aposta==-1):
                                            self.msgstatus.setText("Celular: \nColuna(s) com mais de um número assinalado foi detectada \nAposta: \nfoi detectado um total de apostas superior a 10 números")
                                            self.mensagem_erro()
                                        else:
                                            self.msgstatus.setText("Celular: \nColuna(s) com mais de um número assinalado foi detectada \nAposta: \nfoi detectado um total de apostas inferior a 10 números")
                                            self.mensagem_erro()
                                else:
                                    if(type(c.aposta) is list):
                                        self.msgstatus.setText("Celular: \nPrimeira coluna assinalada indevidamente com 0")
                                        self.mensagem_erro()
                                    else:
                                        if(c.aposta==-1):
                                            self.msgstatus.setText("Celular: \nPrimeira coluna assinalada indevidamente com 0 \nAposta: \nfoi detectado um total de apostas superior a 10 números")
                                            self.mensagem_erro()
                                        else:
                                            self.msgstatus.setText("Celular: \nPrimeira coluna assinalada indevidamente com 0 \nAposta: \nfoi detectado um total de apostas inferior a 10 números")
                                            self.mensagem_erro()
            else:
                self.msgstatus.setText("Necessário calibrar a Webcam")
        else:
            self.msgstatus.setText("Necessário cadastrar uma aposta inicial")

    def ArquivoNome(self):
        dir = './Arquivos_bolão'
        text,ok=QInputDialog.getText(None,'Nome','Nome do arquivo:')
        if text=='':
            self.files=os.listdir(dir)
            count  = 1
            encontrou = False
            while(not encontrou):
                encontrou = True
                numero = str(count)
                for file in self.files:
                    nomeTeste = 'arquivo_' + numero + ".txt"
                    if(file == nomeTeste):
                        encontrou = False
                        count = count+1
            numero = str(count)
            text='arquivo_'+numero
            self.nomeArquivo = dir+'/'+ text + ".txt"
            self.file = open(self.nomeArquivo, 'w')
            self.writer = csv.writer(self.file,dialect='excel')
        else: 
            self.nomeArquivo = dir+'/'+ text + ".txt"
            self.file = open(self.nomeArquivo, 'w')
            self.writer = csv.writer(self.file,dialect='excel')
            

    def tirar_foto(self):
        if (self.aux==False):
            self.auxrep=True
            cv2.imwrite('teste2.png',self.imagem)
            imagemteste=cv2.imread("teste2.png",1)
            img=cv2.flip(imagemteste,1)
            cv2.imwrite('teste2.png',img)
            c=Cartela(img)
            self.rows = []
            if(c.cart1==True and c.cart2==True):
                if(c.telefone>0 and type (c.aposta) is list):
                    self.rodar_labels(c)
                    self.msgstatus.setText("Aposta cadastrada com Sucesso!")
                    f = open(self.nomeArquivo, "a")
                    f.write(str(c.telefone) + ";")
                    row = []
                    row.append(str(c.telefone))
                    for i in range (0,10):
                        f.write(str(c.aposta[i]) + ";")
                        row.append(str(c.aposta[i]))
                    f.write(str("\n"))
                    self.rows.append(row)
                    self.usuario=c.telefone
                else:
                    if(c.telefone>0):
                        if (c.aposta==0):
                            self.msgstatus.setText("Aposta: \nfoi detecado um total de apostas inferior a 10 números")
                            self.mensagem_erro()
                        else:
                            self.msgstatus.setText("Aposta: \nfoi detectado um total de apostas superior a 10 números")
                            self.mensagem_erro()
                    else:
                        if(c.telefone==0):
                            if(type(c.aposta) is list):
                                self.msgstatus.setText("Celular: \nColuna(s) vazia(s) foram detectadas")
                                self.mensagem_erro()
                            else:
                                if(c.aposta==-1):
                                    self.msgstatus.setText("Celular: \nColuna(s) vazia(s) foram detectadas \nAposta: \nfoi detectado um total de apostas superior a 10 números")
                                    self.mensagem_erro()
                                else:
                                    self.msgstatus.setText("Celular: \nColuna(s) vazia(s) foram detectadas \nAposta: \nfoi detectado um total de apostas inferior a 10 números")
                                    self.mensagem_erro()
                        else:
                            if(c.telefone==-1):
                                if(type(c.aposta) is list):
                                    self.msgstatus.setText("Celular: \nColuna(s) com mais de um número assinalado foi detectada")
                                    self.mensagem_erro()
                                else:
                                    if(c.aposta==-1):
                                        self.msgstatus.setText("Celular: \nColuna(s) com mais de um número assinalado foi detectada \nAposta: \nfoi detectado um total de apostas superior a 10 números")
                                        self.mensagem_erro()
                                    else:
                                        self.msgstatus.setText("Celular: \nColuna(s) com mais de um número assinalado foi detectada \nAposta: \nfoi detectado um total de apostas inferior a 10 números")
                                        self.mensagem_erro()
                            else:
                                if(type(c.aposta) is list):
                                    self.msgstatus.setText("Celular: \nPrimeira coluna assinalada indevidamente com 0")
                                    self.mensagem_erro()
                                else:
                                    if(c.aposta==-1):
                                        self.msgstatus.setText("Celular: \nPrimeira coluna assinalada indevidamente com 0 \nAposta: \nfoi detectado um total de apostas superior a 10 números")
                                        self.mensagem_erro()
                                    else:
                                        self.msgstatus.setText("Celular: \nPrimeira coluna assinalada indevidamente com 0 \nAposta: \nfoi detectado um total de apostas inferior a 10 números")
                                        self.mensagem_erro()


                
        else:
            self.msgstatus.setText("Necessário calibrar a Webcam")


    def start_webcam(self):
        data_atual=date.today()
        if(data_atual.year<=2019):
            if (self.auxstart==True):
                self.ArquivoNome()
                self.msgstatus.setText("- Insira uma cartela vazia \n- Posicione a câmera ajustando a cartela com o enquadramento na tela")
                self.capture=cv2.VideoCapture(1)
                self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
                self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,640)
                self.timer=QTimer(self)
                self.timer.timeout.connect(self.update_frame)
                self.timer.start(5)
                self.auxcal=True
                self.auxstart=False

    def update_frame(self):
        ret,self.imagem=self.capture.read()
        self.imagem=cv2.flip(self.imagem,1)
        self.displayImagem(self.imagem,1)

    def stop_webcam(self):
        if self.aux==False:
            reply=QMessageBox.question(self,"Sair","Deseja mesmo salvar os dados e fechar o aplicativo?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.timer.stop()
                self.aux=True
                QCoreApplication.instance().quit()
        else:
            QCoreApplication.instance().quit()
        
    def displayImagem(self,img,window=1):
        qformat=QImage.Format_Indexed8
        if(len(img.shape)==3): #[0]=rows,[1]=col, [2]=channels
            if img.shape[2]==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888
        outImage=QImage(img,img.shape[1],img.shape[0],img.strides[0],qformat)
        #BGB>>RGB
        outImage=outImage.rgbSwapped()
        if window==1:
            self.webcam.setPixmap(QPixmap.fromImage(outImage))
            self.webcam.setScaledContents(True)
    def mensagem_erro(self):
        msg=QMessageBox()
        msg.setWindowTitle("Erro!")
        msg.setText("Um erro de leitura foi verificado")
        msg.setIcon(QMessageBox.Information)
        x=msg.exec_()



if __name__=='__main__':
    app=QApplication(sys.argv)
    window=WebCam()
    window.show()
    sys.exit(app.exec_())