import os
import numpy as np 
import time
import matplotlib.pyplot as plt





###############################################################
###############################################################
#########  Neural network   ###################################
###############################################################
###############################################################



#Neural network 3 layers--------------------------------------------------------------------------------------------------------------------
class nnet3:

    #global variables-------------------------------------------------------------------------
    def __init__ (self, norma=1, normout=1, nn1c=1, nn2c=5, nn3c=1, rate=0.01, epochs=1000, fa2c=5, fa3c=0, cost=0, regu=0, namenet='', shift=1, iteconv=0, conv=0, sbw=1, c1=2, txt=0, sdnoise=0, c2=0.01, c3=1.33):
        
        self.nn1c=nn1c
        self.nn2c=nn2c
        self.nn3c=nn3c
        self.rate=rate
        self.epochs=epochs
        self.fa2c=fa2c
        self.fa3c=fa3c
        self.norma=norma
        self.normout=normout
        self.cost=cost
        self.regu=regu
        self.namenet=namenet
        self.shift=shift
        self.iteconv=iteconv
        self.conv=conv
        self.sbw=sbw
        self.c1=c1
        self.txt=txt
        self.sdnoise=sdnoise
        self.c2=c2
        self.c3=c3



###############################################################
###############################################################
#########  Auxliar function to normalization   ################
###############################################################
###############################################################


    #data normalization by calculating maximums and minimums, inlet------------------------------------------
    def Normalize(self, data, maxiname, mininame, medianame, desvioname):          

        #=-1, standardization
        #=0, do anything
        #=1, between 0 and 1
        #=2, between -1 and 1
        #=3, divide by the average
        #=4, divide by the average and -1 to centralize in zero
       
        vetormax = np.max(data,0) 
        vetormin = np.min(data,0)

        if self.shift>1: #aplica o esticamento se tiver
            vetormax=np.where(vetormax < 0, vetormax*(1/self.shift), vetormax*self.shift)
            vetormin=np.where(vetormin < 0, vetormin*self.shift, vetormin*(1/self.shift))

        vetormed = (vetormax+vetormin)/2
        media = np.mean(data,0)
        desvio = np.std(data,0)        

        if (self.norma==0):
            normalized = data *1
                                    
        if (self.norma==1):
            vetoraux = (vetormax - vetormin)
            vetoraux = np.where(vetoraux==0, 1 , vetoraux)
            normalized = (data - vetormin) / vetoraux
            
        if (self.norma==2):
            vetoraux = (vetormax - vetormed)
            vetoraux = np.where(vetoraux==0, 1 , vetoraux)
            normalized = (data - vetormed) / vetoraux

        if (self.norma==-1):
            vetoraux = desvio
            vetoraux = np.where(vetoraux==0, 1 , vetoraux)
            normalized = (data - media)/vetoraux

        if (self.norma==3):
            normalized = data / media

        if (self.norma==4):
            normalized = (data / media)-1


        np.save(maxiname, vetormax)
        np.save(mininame, vetormin)
        np.save(medianame, media)
        np.save(desvioname, desvio)
        
        return normalized



    #data normalization by calculating maximums and minimums, outlet------------------------------------------
    def Normalizeout(self, data, maxiname, mininame, medianame, desvioname):          

        #=-1, standardization
        #=0, do anything
        #=1, between 0 and 1
        #=2, between -1 and 1 
        
        vetormax = np.max(data,0) 
        vetormin = np.min(data,0)

        if self.shift>1: #aplica o esticamento se tiver
            vetormax=np.where(vetormax < 0, vetormax*(1/self.shift), vetormax*self.shift)
            vetormin=np.where(vetormin < 0, vetormin*self.shift, vetormin*(1/self.shift))

        vetormed = (vetormax+vetormin)/2
        media = np.mean(data,0)
        desvio = np.std(data,0)
        
        if (self.normout==0):
            normalized = data *1
                                    
        if (self.normout==1):
            vetoraux = (vetormax - vetormin)
            vetoraux = np.where(vetoraux==0, 1 , vetoraux)
            normalized = (data - vetormin) / vetoraux
            
        if (self.normout==2):
            vetoraux = (vetormax - vetormed)
            vetoraux = np.where(vetoraux==0, 1 , vetoraux)
            normalized = (data - vetormed) / vetoraux

        if (self.normout==-1):
            vetoraux = desvio
            vetoraux = np.where(vetoraux==0, 1 , vetoraux)
            normalized = (data - media)/vetoraux

        if (self.normout==3):
            normalized = data / media

        if (self.normout==4):
            normalized = (data / media)-1

        np.save(maxiname, vetormax)
        np.save(mininame, vetormin)
        np.save(medianame, media)
        np.save(desvioname, desvio)
        
        return normalized


    #normalizing the data by entering maximums and minimums-----------------------------------------------
    def Normalize2(self, data, maxiname, mininame, medianame, desvioname):         

        vetormax = np.load(maxiname) 
        vetormin = np.load(mininame) 
        vetormed = (vetormax+vetormin)/2
        media = np.load(medianame)
        desvio = np.load(desvioname)  

        normalized = data*1 #==0, não faz nada

        if (self.norma==0):
            normalized = data *1
                                                
        if (self.norma==1):  
            normalized = (data - vetormin) / (vetormax - vetormin)
            
        if (self.norma==2):    
            normalized = (data - vetormed) / (vetormax - vetormed)                                 

        if (self.norma==-1):
            normalized = (data - media)/desvio

        if (self.norma==3):
            normalized = data / media

        if (self.norma==4):
            normalized = (data / media)-1
        
        return normalized


    #normalizing the data by entering maximums and minimums-----------------------------------------------
    def Normalize2out(self, data, maxiname, mininame, medianame, desvioname):         

        vetormax = np.load(maxiname) 
        vetormin = np.load(mininame) 
        vetormed = (vetormax+vetormin)/2
        media = np.load(medianame)
        desvio = np.load(desvioname)  

        normalized = data*1 #==0, não faz nada

        if (self.normout==0):
            normalized = data *1
                                                
        if (self.normout==1):  
            normalized = (data - vetormin) / (vetormax - vetormin)
            
        if (self.normout==2):    
            normalized = (data - vetormed) / (vetormax - vetormed)                                 

        if (self.normout==-1):
            normalized = (data - media)/desvio

        if (self.normout==3):
            normalized = data / media

        if (self.normout==4):
            normalized = (data / media)-1
        
        return normalized



    #data denormalization by entering maximums and minimums--------------------------------------------
    def DesNormalize(self, normalized, maxiname, mininame, medianame, desvioname):         

        vetormax = np.load(maxiname) 
        vetormin = np.load(mininame) 
        vetormed = (vetormax+vetormin)/2
        media = np.load(medianame)
        desvio = np.load(desvioname) 
        
        desnorma = normalized*1 #==0, nada
                            
        if (self.norma==1):  
            desnorma = normalized * (vetormax - vetormin) + vetormin
            
        if (self.norma==2):  
            desnorma = normalized * (vetormax - vetormed) + vetormed

        if (self.norma==-1):          
            desnorma = normalized*desvio + media

        if (self.norma==3): 
            desnorma = normalized*media

        if (self.norma==4):
            desnorma = (normalized+1)*media
                           
        return desnorma



    #data denormalization by entering maximums and minimums--------------------------------------------
    def DesNormalizeout(self, normalized, maxiname, mininame, medianame, desvioname):         

        vetormax = np.load(maxiname) 
        vetormin = np.load(mininame) 
        vetormed = (vetormax+vetormin)/2
        media = np.load(medianame)
        desvio = np.load(desvioname) 
        
        desnorma = normalized*1 #==0, nada
                            
        if (self.normout==1):  
            desnorma = normalized * (vetormax - vetormin) + vetormin
            
        if (self.normout==2):  
            desnorma = normalized * (vetormax - vetormed) + vetormed

        if (self.normout==-1):          
            desnorma = normalized*desvio + media

        if (self.normout==3): 
            desnorma = normalized*media

        if (self.normout==4):
            desnorma = (normalized+1)*media
                           
        return desnorma



###############################################################
###############################################################
################ Activation functions   #######################
###############################################################
###############################################################



    #Definition of activation functions---------------------------------------------------------
    def Activation(self, typee, x):

        if (typee==0): #linear (-inf,inf)
            y = x
            return y
    
        if (typee==1): #Sigmoide (0,1)
            y = 1/(1+np.exp(-x))
            return y

        if (typee==2): #softpluss (0,inf)
            y = np.log(1+np.exp(x)) #log é na base natural
            return y

        if (typee==3): #gaussinana (0,1)
            y = np.exp(-1*(x**2)) 
            return y

        if (typee==4): #ReLU (0,inf)            
            y=np.where(x < 0, 0, x)
            return y

        if (typee==5): #tanh (-1,1)
            y = (np.exp(x)-np.exp(-x))/(np.exp(x)+np.exp(-x))
            return y

        if (typee==6): #LReLU (-inf,inf)
            y=np.where(x <= 0, x*0.01, x)
            return y
        
        if (typee==7): #arctan (-inf, inf)
            y = np.arctan(x)
            return y

        if (typee==8): #exp (-inf, inf)
            y = np.exp(x)
            return y
    
        if (typee==9): #seno (-inf, inf)
            y = np.sin(x)
            return y

        if (typee==10): #swish (0, inf)
            y = x/(1+np.exp(-x))
            return y

        if (typee==11): #selu (-1, inf)
            y=np.where(x >= 0, x, np.exp(x)-1)
            return y
      
        if (typee==12): #logsigmoide (0,1)
            y = np.log( 1/(1+np.exp(-x)) )
            return y

        if (typee==13): #x^n (inf,inf)
            y = (abs(x))**self.c1
            return y

        if (typee==14): #ELU (-1,inf)
            y=np.where(x <= 0, 1e-8 + 0.1*(np.exp(x)-1), x)
            return y

        if (typee==15): # GoldRelU (inf,inf)
            y = np.where(x > 0, x*1.61803398, x*0.61803398)
            return y

        if (typee==16): # Metallic mean (inf,inf)
            y = (x + (x**2 + 4)**0.5)/2
            return y

        if (typee==17): #NoiseReLU (0,inf)            
            y=np.where(x < 0, 0, x * np.random.normal(1,self.c2) )
            return y

        if (typee==18): #ReLUquad (-inf,inf)            
            y=np.where(x < 0, 0, abs(x)**self.c3)
            return y


    def DeActivation(self, typee,x):

        if (typee==0): #linear (-inf,inf)
            y = 1
            return y    
    
        if (typee==1): #Sigmoide (0,1)
            w = 1/(1+np.exp(-x))
            y = w*(1-w)
            return y

        if (typee==2): #softpluss (0,inf)
            y = 1/(1 + np.exp(-x))
            return y
    
        if (typee==3): #gaussinana (0,1)
            y = -2*x*np.exp(-1*(x**2)) 
            return y

        if (typee==4): #ReLU (0,inf)            
            y=np.where(x < 0, 0, 1)
            return y

        if (typee==5): #tanh (-1,1)
            w = (np.exp(x)-np.exp(-x))/(np.exp(x)+np.exp(-x))
            y = 1 - w**2
            return y
    
        if (typee==6): #LReLU (-inf,inf)
            y=np.where(x <= 0, 0.01, 1)        
            return y
    
        if (typee==7): #arctan (-inf, inf)
            y = 1/(1+x**2)
            return y

        if (typee==8): #exp (-inf, inf)
            y = np.exp(x)
            return y

        if (typee==9): #seno (-inf, inf)
            y = np.cos(x)
            return y  

        if (typee==10): #swish (0, inf)
            y = (x/(1+np.exp(-x))) + (1/(1+np.exp(-x)))*(1 - (x/(1+np.exp(-x))) )
            return y

        if (typee==11): #selu (-1, inf)
            y = np.where(x >= 0, 1, np.exp(x))        
            return y        

        if (typee==12): #logsigmoide (0,1)
            y = np.exp(-x)/(1+np.exp(-x))
            return y

        if (typee==13): #x^n (inf,inf)
            y = self.c1*((abs(x))**(self.c1-1))
            return y

        if (typee==14): #ELU (inf,inf)
            y=np.where(x <= 0, 0.1*np.exp(x), 1)
            return y

        if (typee==15): # GoldRelU (inf,inf)
            y = np.where(x > 0, 1.61803398, 0.61803398)
            return y

        if (typee==16): # Metallic mean (inf,inf)
            y = 0.5*((x/((x**2 + 4)**0.5))+1)            
            return y

        if (typee==17): #RandReLU (0,inf)
            y=np.where(x < 0, 0, 1)
            return y

        if (typee==18): #ReLUquad (-inf,inf)            
            y=np.where(x < 0, 0, self.c3*(abs(x)**(self.c3-1)) )
            return y
        
###############################################################
###############################################################
################ Machine learning   ###########################
###############################################################
###############################################################
        

    #machine learning,  single batch with ADAM accelerator-----------------------------------------------------
    def Fit_ADAM(self, matX, matY, matX2=[0], matY2=[0]):
        
        tinicio = time.time()
     
        if np.ndim(matY) == 1: #ajusta caso for um vetor p/ matriz de 1 coluna
            matY = np.reshape(matY, (-1, 1))
            if (len(matY2)>1):
                matY2 = np.reshape(matY2, (-1, 1))

        #Criação ou leitura da matriz dos pesos--------

        #pesos
        P12 = np.zeros((self.nn1c,self.nn2c))
        P23 = np.zeros((self.nn2c,self.nn3c))

        #bias
        B2= np.zeros((self.nn2c))
        B3= np.zeros((self.nn3c))

        #pesos memorizados
        P12m = np.zeros((self.nn1c,self.nn2c))
        P23m = np.zeros((self.nn2c,self.nn3c))

        #bias memorizados
        B2m = np.zeros((self.nn2c))
        B3m = np.zeros((self.nn3c))

        #variaçao pesos
        VP12 = np.zeros((self.nn1c,self.nn2c))
        VP23 = np.zeros((self.nn2c,self.nn3c))

        #variaçao bias
        VB2= np.zeros((self.nn2c))
        VB3= np.zeros((self.nn3c))
 
        #velocidade pesos
        veloP12 = np.zeros((self.nn1c,self.nn2c))
        veloP23 = np.zeros((self.nn2c,self.nn3c))

        #velocidade bias
        veloB2= np.zeros((self.nn2c))
        veloB3= np.zeros((self.nn3c))

        #massa pesos
        massaP12 = np.zeros((self.nn1c,self.nn2c))
        massaP23 = np.zeros((self.nn2c,self.nn3c))

        #massa bias
        massaB2= np.zeros((self.nn2c))
        massaB3= np.zeros((self.nn3c))

        #camadas
        c1= np.zeros((self.nn1c))
        c2= np.zeros((self.nn2c))
        c3= np.zeros((self.nn3c))

        #derivadas
        d1= np.zeros((self.nn1c))
        d2= np.zeros((self.nn2c))
        d3= np.zeros((self.nn3c))

        #erros
        e1= np.zeros((self.nn1c))
        e2= np.zeros((self.nn2c))
        e3= np.zeros((self.nn3c))

        #resultados
        R = np.zeros((self.nn3c))


        #ajuste do local de salvamento, se especificado
        if (self.namenet==''):
            nomepasta=''
        else:
            nomepasta = self.namenet + '/'
            if not os.path.exists(self.namenet):
                os.mkdir(self.namenet)



        try: #Inicializa com pesos ja salvos, se existir esses arquivos-------------------------------------

            net02 = np.load(nomepasta + "net.npy")            
            net01 = self.nn1c + self.nn2c*1e3 + self.nn3c*1e6
            if (net01 != net02):
                input('Neural network saves this different from configured network')
                exit()

            net03 = np.load(nomepasta + "netati.npy")            
            net04 = self.fa2c + self.fa3c*1e3
            if (net03 != net04):
                input('Activation functions saves this different from configured network')
                exit()

            net05 = np.load(nomepasta + "norm.npy")            
            net06 = self.norma + self.normout*1e3
            if (net05 != net06):
                input('Normalization saves this different from configured network')
                exit()

            P12 = np.load(nomepasta + "P12.npy")
            P23 = np.load(nomepasta + "P23.npy")           
            B2 = np.load(nomepasta + "B2.npy")
            B3 = np.load(nomepasta + "B3.npy")

        except: #Inicializa randomicamente-------------------------------

            B2 = -0.1 + 2*0.1*(np.random.rand(self.nn2c))
            B3 = -0.1 + 2*0.1*(np.random.rand(self.nn3c))  
            P12 = -0.1 + 2*0.1*(np.random.rand(self.nn1c,self.nn2c))
            P23 = -0.1 + 2*0.1*(np.random.rand(self.nn2c,self.nn3c))


        #Normaliza os parametros-------------------------
        matX = self.Normalize(matX,nomepasta + "vmax_in.npy",nomepasta + "vmin_in.npy",nomepasta + "media_in.npy",nomepasta + "desvio_in.npy")                
        matY = self.Normalizeout(matY,nomepasta + "vmax_out.npy",nomepasta + "vmin_out.npy",nomepasta + "media_out.npy",nomepasta + "desvio_out.npy")

        #Para validacao cruzada se houver------
        if (len(matX2)>1):
            matX2 = self.Normalize2(matX2,nomepasta + "vmax_in.npy",nomepasta + "vmin_in.npy",nomepasta + "media_in.npy",nomepasta + "desvio_in.npy") 
            matY2 = self.Normalize2out(matY2,nomepasta + "vmax_out.npy",nomepasta + "vmin_out.npy",nomepasta + "media_out.npy",nomepasta + "desvio_out.npy") 


        #Processo de aprendizado------------------------------------------------------------
                
        VetorErro = [0]
        MenorErro = 999999999
        
        NumdataEstudo = len(matX) #dados de entrada 
        if (len(matX2)==1):
            NumdataEstudo2 = NumdataEstudo
            matXX = matX*1
            matYY = matY*1          
        else:            
            NumdataEstudo2 = len(matX2)
            matXX = matX2*1
            matYY = matY2*1
            
        Calculated = np.zeros((NumdataEstudo2, self.nn3c)) #inicializa a matriz dos resultados 

        monit=0
        iteconv = self.iteconv
        for ite in range(0,self.epochs): #Processo iterativo global, epocas, cada epoca passa por todos os dados de aprendizagem-----------------
            Tempo = ite+1
    
            if ite > (self.epochs*monit/100): #só um monitor de progresso
                print(str(monit) + '%')
                monit=monit+10
           
            if (self.sbw==1): #Calculo do erro-----------------------------------

                regulariza=0
                if (self.regu!=0): #adiciona a regularização se houver                    
                    regulariza = self.regu*( np.sum(P12*P12) + np.sum(P23*P23) + np.sum(B2*B2) + np.sum(B3*B3) )
    
                EMQ = 0
                for caso in range (0, NumdataEstudo2): #Verificação do aprendizado---

                    #Camada 1, data de entrada  
                    c1 = matXX[caso,:self.nn1c]                                               

                    #propagacao sinal
                    c2 = np.dot(c1,P12)- B2        
                    c2 = self.Activation(self.fa2c,c2)

                    c3 = np.dot(c2,P23)- B3
                    c3 = self.Activation(self.fa3c,c3)

                    Calculated[caso][:] = c3[:] 

                #calculo efetivo do erro ------------ 
                if (self.cost==0):#erro medio quadratico                 
                    EMQ = ( np.sum( 0.5*((Calculated - matYY)**2) + regulariza ) )/(NumdataEstudo2*self.nn3c)                    
                else: #BCE, entropia cruzada binaria
                    EMQ = ( np.sum( (-1*(matYY*np.log(Calculated +1e-10)+(1-matYY)*np.log((1-Calculated) +1e-10)) + regulariza) ) )/(NumdataEstudo2*self.nn3c)
                
                VetorErro.append(EMQ)
                                               

                #memorização dos melhores pesos-----------
                if (EMQ < MenorErro):
                    itememo = ite+1
                    MenorErro = EMQ
                    P12m = P12*1
                    P23m = P23*1
                    B2m = B2*1
                    B3m = B3*1

                #encerra o processamento se atender o criterio de convergencia apos n iteracoes---------            
                if (self.conv!=0):
                    if (ite>iteconv):          
                        convcalc = VetorErro[ite+1]/VetorErro[ite+1-self.iteconv]                    
                        iteconv  += self.iteconv                    
                        if (convcalc>=self.conv and convcalc<1):                        
                            break


            #começa os ajustes dos pesos-------------------
            regulariza=0
            if (self.regu!=0): #adiciona a regularização se houver                    
                regulariza = 2*self.regu*( np.sum(P12) + np.sum(P23) + np.sum(B2) + np.sum(B3) )


            #Aplica o ruido nos dados de entrada para ajudar a evitar overfiting------------------
            if (self.sdnoise!=0):
                random_matrix = np.random.normal(1, self.sdnoise, size=(NumdataEstudo, self.nn1c))
                matXr = matX*random_matrix                       
            else:
                matXr = matX*1


            for caso in range (0, NumdataEstudo): #varredura em todos os casos de estudo--------

                #Camada 1, data de entrada
                c1 = matXr[caso,:self.nn1c]
                R = matY[caso,:]                        
                
                #propagacao sinal
                c2 = np.dot(c1,P12)- B2
                d2 = self.DeActivation(self.fa2c,c2)
                c2 = self.Activation(self.fa2c,c2)

                c3 = np.dot(c2,P23)- B3
                d3 = self.DeActivation(self.fa3c,c3)
                c3 = self.Activation(self.fa3c,c3)

                #Calcula o erro da ultima camada
                if (self.cost==0):#EMQ
                    e3 = d3 * ( (R - c3) + regulariza )
                else: #BCE
                    e3 = d3 * ( (R/(c3 +1e-7)) - ((1-R)/(1-c3 +1e-7)) + regulariza )
                
                #Propagação do erro para traz, backprop    
                e2 = np.dot(e3, np.transpose(P23))
                e2 = d2 * e2

                #Calculo da variação acumulativa bruta dos pesos                
                VP12 += np.dot(c1.reshape(-1, 1), e2.reshape(1, -1))                
                VP23 += np.dot(c2.reshape(-1, 1), e3.reshape(1, -1))
                
                VB2 += - e2         
                VB3 += - e3           

            #Atualização efetiva dos pesos----------------------------------

            Gd12 = VP12 / NumdataEstudo
            Gd23 = VP23 / NumdataEstudo

            massaP12 = 0.9*massaP12 + (1-0.9)*Gd12 
            massaP23 = 0.9*massaP23 + (1-0.9)*Gd23 

            veloP12 = 0.999*veloP12 + (1-0.999)*(Gd12**2) +1e-10
            veloP23 = 0.999*veloP23 + (1-0.999)*(Gd23**2) +1e-10 

            aux1= 1-(0.9**Tempo)
            aux2 = 1 - (0.999**Tempo)
    
            P12 = P12 + self.rate*( (massaP12/aux1) / np.sqrt(veloP12/aux2) )
            P23 = P23 + self.rate*( (massaP23/aux1) / np.sqrt(veloP23/aux2) )

            Gd2 = VB2 / NumdataEstudo
            Gd3 = VB3 / NumdataEstudo

            massaB2 = 0.9*massaB2 + (1-0.9)*Gd2 
            massaB3 = 0.9*massaB3 + (1-0.9)*Gd3 

            veloB2 = 0.999*veloB2 + (1-0.999)*(Gd2**2) +1e-10 
            veloB3 = 0.999*veloB3 + (1-0.999)*(Gd3**2) +1e-10 
    
            B2 = B2 + self.rate*( (massaB2/aux1) / np.sqrt(veloB2/aux2) )
            B3 = B3 + self.rate*( (massaB3/aux1) / np.sqrt(veloB3/aux2) )
 
            VP12 = np.zeros((self.nn1c,self.nn2c))
            VP23 = np.zeros((self.nn2c,self.nn3c))
            VB2= np.zeros((self.nn2c))
            VB3= np.zeros((self.nn3c))


        print('100%')

        if (self.sbw==1): 
            P12 = P12m*1
            P23 = P23m*1
            B2 = B2m*1
            B3 = B3m*1


        #Salva os pesos e bias em arquivos txt----------------------------------------------------------
        np.save(nomepasta + "net.npy", self.nn1c + self.nn2c*1e3 + self.nn3c*1e6)
        np.save(nomepasta + "netati.npy", self.fa2c + self.fa3c*1e3)
        np.save(nomepasta + "norm.npy", self.norma + self.normout*1e3)
        
        np.save(nomepasta + "P12.npy", P12)
        np.save(nomepasta + "P23.npy", P23)
        np.save(nomepasta + "B2.npy", B2)
        np.save(nomepasta + "B3.npy", B3)

        if (self.sbw==1):
            VetorErro[0] = itememo
            np.save(nomepasta + "Convergencia.npy", VetorErro)

        #Salva os pesos para checagem humana
        np.savetxt(nomepasta + "P12.txt", P12)
        np.savetxt(nomepasta + "P23.txt", P23)
        np.savetxt(nomepasta + "B2.txt", B2)
        np.savetxt(nomepasta + "B3.txt", B3)     

        tfim = time.time()
        print('runtime(s) = ' , tfim-tinicio)







    #machine learning stochastic case by case------------------------------------------------------
    def Fit_STOC(self, matX, matY, matX2=[0], matY2=[0]):

        tinicio = time.time()

        if np.ndim(matY) == 1: #ajusta caso for um vetor p/ matriz de 1 coluna
            matY = np.reshape(matY, (-1, 1))
            if (len(matY2)>1):
                matY2 = np.reshape(matY2, (-1, 1))

        #Criação ou leitura da matriz dos pesos--------

        #pesos
        P12 = np.zeros((self.nn1c,self.nn2c))
        P23 = np.zeros((self.nn2c,self.nn3c))

        #bias
        B2= np.zeros((self.nn2c))
        B3= np.zeros((self.nn3c))

        #pesos memorizados
        P12m = np.zeros((self.nn1c,self.nn2c))
        P23m = np.zeros((self.nn2c,self.nn3c))

        #bias memorizados
        B2m = np.zeros((self.nn2c))
        B3m = np.zeros((self.nn3c))

        #camadas
        c1= np.zeros((self.nn1c))
        c2= np.zeros((self.nn2c))
        c3= np.zeros((self.nn3c))

        #derivadas
        d1= np.zeros((self.nn1c))
        d2= np.zeros((self.nn2c))
        d3= np.zeros((self.nn3c))

        #erros
        e1= np.zeros((self.nn1c))
        e2= np.zeros((self.nn2c))
        e3= np.zeros((self.nn3c))

        #resultados
        R = np.zeros((self.nn3c))


        #ajuste do local de salvamento, se especificado
        if (self.namenet==''):
            nomepasta=''
        else:
            nomepasta = self.namenet + '/'
            if not os.path.exists(self.namenet):
                os.mkdir(self.namenet)


        try: #Inicializa com pesos ja salvos, se existir esses arquivos-------------------------------------

            net02 = np.load(nomepasta + "net.npy")            
            net01 = self.nn1c + self.nn2c*1e3 + self.nn3c*1e6
            if (net01 != net02):
                input('Neural network saves this different from configured network')
                exit()

            net03 = np.load(nomepasta + "netati.npy")            
            net04 = self.fa2c + self.fa3c*1e3
            if (net03 != net04):
                input('Activation functions saves this different from configured network')
                exit()

            net05 = np.load(nomepasta + "norm.npy")            
            net06 = self.norma + self.normout*1e3
            if (net05 != net06):
                input('Normalization saves this different from configured network')
                exit()

            P12 = np.load(nomepasta + "P12.npy")
            P23 = np.load(nomepasta + "P23.npy")           
            B2 = np.load(nomepasta + "B2.npy")
            B3 = np.load(nomepasta + "B3.npy")

        except: #Inicializa randomicamente-------------------------------

            B2 = -0.1 + 2*0.1*(np.random.rand(self.nn2c))
            B3 = -0.1 + 2*0.1*(np.random.rand(self.nn3c))   
            P12 = -0.1 + 2*0.1*(np.random.rand(self.nn1c,self.nn2c))
            P23 = -0.1 + 2*0.1*(np.random.rand(self.nn2c,self.nn3c))


        #Normaliza os parametros-------------------------
        matX = self.Normalize(matX,nomepasta + "vmax_in.npy",nomepasta + "vmin_in.npy",nomepasta + "media_in.npy",nomepasta + "desvio_in.npy")                
        matY = self.Normalizeout(matY,nomepasta + "vmax_out.npy",nomepasta + "vmin_out.npy",nomepasta + "media_out.npy",nomepasta + "desvio_out.npy")

        #Para validacao cruzada se houver------
        if (len(matX2)>1):
            matX2 = self.Normalize2(matX2,nomepasta + "vmax_in.npy",nomepasta + "vmin_in.npy",nomepasta + "media_in.npy",nomepasta + "desvio_in.npy") 
            matY2 = self.Normalize2out(matY2,nomepasta + "vmax_out.npy",nomepasta + "vmin_out.npy",nomepasta + "media_out.npy",nomepasta + "desvio_out.npy") 


        #Processo de aprendizado------------------------------------------------------------

        VetorErro = [0]
        MenorErro = 999999999

        NumdataEstudo = len(matX) #dados de entrada 
        if (len(matX2)==1):
            NumdataEstudo2 = NumdataEstudo
            matXX = matX*1
            matYY = matY*1          
        else:            
            NumdataEstudo2 = len(matX2)
            matXX = matX2*1
            matYY = matY2*1

        Calculated = np.zeros((NumdataEstudo2, self.nn3c)) #inicializa a matriz dos resultados 

        monit=0
        iteconv = self.iteconv
        for ite in range(0,self.epochs): #Processo iterativo global, epocas, cada epoca passa por todos os dados de aprendizagem-----------------
            Tempo = ite+1
    
            if ite > (self.epochs*monit/100): #só um monitor de progresso
                print(str(monit) + '%')
                monit=monit+10


            if (self.sbw==1): #Calculo do erro-----------------------------------
            
                regulariza=0
                if (self.regu!=0): #adiciona a regularização se houver                    
                    regulariza = self.regu*( np.sum(P12*P12) + np.sum(P23*P23) + np.sum(B2*B2) + np.sum(B3*B3) )

                EMQ = 0
                for caso in range (0, NumdataEstudo2): #Verificação do aprendizado---

                    #Camada 1, data de entrada
                    c1 = matXX[caso,:self.nn1c]           
                
                    #propagacao sinal
                    c2 = np.dot(c1,P12)- B2        
                    c2 = self.Activation(self.fa2c,c2)

                    c3 = np.dot(c2,P23)- B3
                    c3 = self.Activation(self.fa3c,c3)      

                    Calculated[caso][:] = c3[:] 
               

                #calculo efetivo do erro ------------ 
                if (self.cost==0):#erro medio quadratico                 
                    EMQ = ( np.sum( 0.5*((Calculated - matYY)**2) + regulariza ) )/(NumdataEstudo2*self.nn3c)                    
                else: #BCE, entropia cruzada binaria
                    EMQ = ( np.sum( (-1*(matYY*np.log(Calculated +1e-10)+(1-matYY)*np.log((1-Calculated) +1e-10)) + regulariza) ) )/(NumdataEstudo2*self.nn3c)
                
                VetorErro.append(EMQ)
                      
 
                #memorização dos melhores pesos------------
                if (EMQ < MenorErro):
                    itememo = ite+1
                    MenorErro = EMQ
                    P12m = P12*1
                    P23m = P23*1
                    B2m = B2*1
                    B3m = B3*1

                #encerra o processamento se atender o criterio de convergencia apos n iteracoes---------            
                if (self.conv!=0):
                    if (ite>iteconv):          
                        convcalc = VetorErro[ite+1]/VetorErro[ite+1-self.iteconv]                    
                        iteconv  += self.iteconv                    
                        if (convcalc>=self.conv and convcalc<1):                        
                            break


            #Aplica o ruido nos dados de entrada para ajudar a evitar overfiting------------------
            if (self.sdnoise!=0):
                random_matrix = np.random.normal(1, self.sdnoise, size=(NumdataEstudo, self.nn1c))
                matXr = matX*random_matrix                       
            else:
                matXr = matX*1


            for caso in range (0, NumdataEstudo): #varredura em todos os casos, mas no estocastico, atualiza os pesos caso a caso---

                #Camada 1, data de entrada
                c1 = matXr[caso,:self.nn1c]
                R = matY[caso,:]                        
                
                #propagacao sinal
                c2 = np.dot(c1,P12)- B2
                d2 = self.DeActivation(self.fa2c,c2)
                c2 = self.Activation(self.fa2c,c2)

                c3 = np.dot(c2,P23)- B3
                d3 = self.DeActivation(self.fa3c,c3)
                c3 = self.Activation(self.fa3c,c3)

                regulariza=0
                if (self.regu!=0): #adiciona a regularização se houver                    
                    regulariza = 2*self.regu*( np.sum(P12) + np.sum(P23) + np.sum(B2) + np.sum(B3) )

                #Calcula o erro da ultima camada
                if (self.cost==0):#EMQ
                    e3 = d3 * ( (R - c3) + regulariza )
                else: #BCE
                    e3 = d3 * ( (R/(c3 +1e-7)) - ((1-R)/(1-c3 +1e-7)) + regulariza )
                 
                #Propagação do erro para traz, backprop    
                e2 = np.dot(e3, np.transpose(P23))
                e2 = d2 * e2

                #Atualização dos pesos
                P12 += self.rate*(np.dot(c1.reshape(-1, 1), e2.reshape(1, -1)))
                P23 += self.rate*(np.dot(c2.reshape(-1, 1), e3.reshape(1, -1)))               
                B2 += - self.rate * e2
                B3 += - self.rate * e3


        print('100%')

        if (self.sbw==1):
            P12 = P12m*1
            P23 = P23m*1
            B2 = B2m*1
            B3 = B3m*1

        #Salva os pesos e bias em arquivos txt----------------------------------------------------------
        np.save(nomepasta + "net.npy", self.nn1c + self.nn2c*1e3 + self.nn3c*1e6)
        np.save(nomepasta + "netati.npy", self.fa2c + self.fa3c*1e3)
        np.save(nomepasta + "norm.npy", self.norma + self.normout*1e3)
        
        np.save(nomepasta + "P12.npy", P12)
        np.save(nomepasta + "P23.npy", P23)
        np.save(nomepasta + "B2.npy", B2)
        np.save(nomepasta + "B3.npy", B3)

        if (self.sbw==1):
            VetorErro[0] = itememo
            np.save(nomepasta + "Convergencia.npy", VetorErro)

        #Salva os pesos para checagem humana
        np.savetxt(nomepasta + "P12.txt", P12)
        np.savetxt(nomepasta + "P23.txt", P23)
        np.savetxt(nomepasta + "B2.txt", B2)
        np.savetxt(nomepasta + "B3.txt", B3)   

        tfim = time.time()
        print('runtime(s) = ' , tfim-tinicio)








    #machine learning,  single batch with ADAM accelerator-----------------------------------------------------
    def Fit_STOC_ADAM(self, matX, matY, matX2=[0], matY2=[0]):

        tinicio = time.time()

        if np.ndim(matY) == 1: #ajusta caso for um vetor p/ matriz de 1 coluna
            matY = np.reshape(matY, (-1, 1))
            if (len(matY2)>1):
                matY2 = np.reshape(matY2, (-1, 1))

        #Criação ou leitura da matriz dos pesos--------

        #pesos
        P12 = np.zeros((self.nn1c,self.nn2c))
        P23 = np.zeros((self.nn2c,self.nn3c))

        #bias
        B2= np.zeros((self.nn2c))
        B3= np.zeros((self.nn3c))

        #pesos memorizados
        P12m = np.zeros((self.nn1c,self.nn2c))
        P23m = np.zeros((self.nn2c,self.nn3c))

        #bias memorizados
        B2m = np.zeros((self.nn2c))
        B3m = np.zeros((self.nn3c))

        #variaçao pesos
        VP12 = np.zeros((self.nn1c,self.nn2c))
        VP23 = np.zeros((self.nn2c,self.nn3c))

        #variaçao bias
        VB2= np.zeros((self.nn2c))
        VB3= np.zeros((self.nn3c))

        #velocidade pesos
        veloP12 = np.zeros((self.nn1c,self.nn2c))
        veloP23 = np.zeros((self.nn2c,self.nn3c))

        #velocidade bias
        veloB2= np.zeros((self.nn2c))
        veloB3= np.zeros((self.nn3c))

        #massa pesos
        massaP12 = np.zeros((self.nn1c,self.nn2c))
        massaP23 = np.zeros((self.nn2c,self.nn3c))

        #massa bias
        massaB2= np.zeros((self.nn2c))
        massaB3= np.zeros((self.nn3c))

        #camadas
        c1= np.zeros((self.nn1c))
        c2= np.zeros((self.nn2c))
        c3= np.zeros((self.nn3c))

        #derivadas
        d1= np.zeros((self.nn1c))
        d2= np.zeros((self.nn2c))
        d3= np.zeros((self.nn3c))

        #erros
        e1= np.zeros((self.nn1c))
        e2= np.zeros((self.nn2c))
        e3= np.zeros((self.nn3c))

        #resultados
        R = np.zeros((self.nn3c))


        #ajuste do local de salvamento, se especificado
        if (self.namenet==''):
            nomepasta=''
        else:
            nomepasta = self.namenet + '/'
            if not os.path.exists(self.namenet):
                os.mkdir(self.namenet)



        try: #Inicializa com pesos ja salvos, se existir esses arquivos-------------------------------------

            net02 = np.load(nomepasta + "net.npy")            
            net01 = self.nn1c + self.nn2c*1e3 + self.nn3c*1e6
            if (net01 != net02):
                input('Neural network saves this different from configured network')
                exit()

            net03 = np.load(nomepasta + "netati.npy")            
            net04 = self.fa2c + self.fa3c*1e3
            if (net03 != net04):
                input('Activation functions saves this different from configured network')
                exit()

            net05 = np.load(nomepasta + "norm.npy")            
            net06 = self.norma + self.normout*1e3
            if (net05 != net06):
                input('Normalization saves this different from configured network')
                exit()

            P12 = np.load(nomepasta + "P12.npy")
            P23 = np.load(nomepasta + "P23.npy")                     
            B2 = np.load(nomepasta + "B2.npy")
            B3 = np.load(nomepasta + "B3.npy")

        except: #Inicializa randomicamente-------------------------------

            B2 = -0.1 + 2*0.1*(np.random.rand(self.nn2c))
            B3 = -0.1 + 2*0.1*(np.random.rand(self.nn3c))  
            P12 = -0.1 + 2*0.1*(np.random.rand(self.nn1c,self.nn2c))
            P23 = -0.1 + 2*0.1*(np.random.rand(self.nn2c,self.nn3c))


        #Normaliza os parametros-------------------------
        matX = self.Normalize(matX,nomepasta + "vmax_in.npy",nomepasta + "vmin_in.npy",nomepasta + "media_in.npy",nomepasta + "desvio_in.npy")                
        matY = self.Normalizeout(matY,nomepasta + "vmax_out.npy",nomepasta + "vmin_out.npy",nomepasta + "media_out.npy",nomepasta + "desvio_out.npy")

        #Para validacao cruzada se houver------
        if (len(matX2)>1):
            matX2 = self.Normalize2(matX2,nomepasta + "vmax_in.npy",nomepasta + "vmin_in.npy",nomepasta + "media_in.npy",nomepasta + "desvio_in.npy") 
            matY2 = self.Normalize2out(matY2,nomepasta + "vmax_out.npy",nomepasta + "vmin_out.npy",nomepasta + "media_out.npy",nomepasta + "desvio_out.npy") 


        #Processo de aprendizado------------------------------------------------------------

        VetorErro = [0]
        MenorErro = 999999999

        NumdataEstudo = len(matX) #dados de entrada 
        if (len(matX2)==1):
            NumdataEstudo2 = NumdataEstudo
            matXX = matX*1
            matYY = matY*1          
        else:            
            NumdataEstudo2 = len(matX2)
            matXX = matX2*1
            matYY = matY2*1

        Calculated = np.zeros((NumdataEstudo2, self.nn3c)) #inicializa a matriz dos resultados 

        monit=0
        iteconv = self.iteconv
        for ite in range(0,self.epochs): #Processo iterativo global, epocas, cada epoca passa por todos os dados de aprendizagem-----------------
            Tempo = ite+1
    
            if ite > (self.epochs*monit/100): #só um monitor de progresso
                print(str(monit) + '%')
                monit=monit+10


            if (self.sbw==1): #Calculo do erro-----------------------------------
            
                regulariza=0
                if (self.regu!=0): #adiciona a regularização se houver                    
                    regulariza = self.regu*( np.sum(P12*P12) + np.sum(P23*P23) + np.sum(B2*B2) + np.sum(B3*B3) )

                EMQ = 0
                for caso in range (0, NumdataEstudo2): #Verificação do aprendizado---

                    #Camada 1, data de entrada  
                    c1 = matXX[caso,:self.nn1c]               
                
                    #propagacao sinal
                    c2 = np.dot(c1,P12)- B2        
                    c2 = self.Activation(self.fa2c,c2)

                    c3 = np.dot(c2,P23)- B3
                    c3 = self.Activation(self.fa3c,c3)

                    Calculated[caso][:] = c3[:] 


                #calculo efetivo do erro ------------ 
                if (self.cost==0):#erro medio quadratico                 
                    EMQ = ( np.sum( 0.5*((Calculated - matYY)**2) + regulariza ) )/(NumdataEstudo2*self.nn3c)                    
                else: #BCE, entropia cruzada binaria
                    EMQ = ( np.sum( (-1*(matYY*np.log(Calculated +1e-10)+(1-matYY)*np.log((1-Calculated) +1e-10)) + regulariza) ) )/(NumdataEstudo2*self.nn3c)
                
                VetorErro.append(EMQ)


                #memorização dos melhores pesos-----------
                if (EMQ < MenorErro):
                    itememo = ite+1
                    MenorErro = EMQ
                    P12m = P12*1
                    P23m = P23*1
                    B2m = B2*1
                    B3m = B3*1

                #encerra o processamento se atender o criterio de convergencia apos n iteracoes---------            
                if (self.conv!=0):
                    if (ite>iteconv):          
                        convcalc = VetorErro[ite+1]/VetorErro[ite+1-self.iteconv]                    
                        iteconv  += self.iteconv                    
                        if (convcalc>=self.conv and convcalc<1):                        
                            break


            #Aplica o ruido nos dados de entrada para ajudar a evitar overfiting------------------
            if (self.sdnoise!=0):
                random_matrix = np.random.normal(1, self.sdnoise, size=(NumdataEstudo, self.nn1c))
                matXr = matX*random_matrix                       
            else:
                matXr = matX*1


            for caso in range (0, NumdataEstudo): #varredura em todos os casos de estudo--------

                #Camada 1, data de entrada
                c1 = matXr[caso,:self.nn1c]
                R = matY[caso,:]                        
                
                #propagacao sinal
                c2 = np.dot(c1,P12)- B2
                d2 = self.DeActivation(self.fa2c,c2)
                c2 = self.Activation(self.fa2c,c2)

                c3 = np.dot(c2,P23)- B3
                d3 = self.DeActivation(self.fa3c,c3)
                c3 = self.Activation(self.fa3c,c3)
      
                regulariza=0
                if (self.regu!=0): #adiciona a regularização se houver                    
                    regulariza = 2*self.regu*( np.sum(P12) + np.sum(P23) + np.sum(B2) + np.sum(B3) )

                #Calcula o erro da ultima camada
                if (self.cost==0):#EMQ
                    e3 = d3 * ( (R - c3) + regulariza )
                else: #BCE
                    e3 = d3 * ( (R/(c3 +1e-7)) - ((1-R)/(1-c3 +1e-7)) + regulariza )
                
                #Propagação do erro para traz, backprop     
                e2 = np.dot(e3, np.transpose(P23))
                e2 = d2 * e2
                                     
        
                #Atualização efetiva dos pesos----------------------------------

                Gd12 = np.dot(c1.reshape(-1, 1), e2.reshape(1, -1))  
                Gd23 = np.dot(c2.reshape(-1, 1), e3.reshape(1, -1)) 

                massaP12 = 0.9*massaP12 + (1-0.9)*Gd12
                massaP23 = 0.9*massaP23 + (1-0.9)*Gd23

                veloP12 = 0.999*veloP12 + (1-0.999)*(Gd12**2) +1e-10
                veloP23 = 0.999*veloP23 + (1-0.999)*(Gd23**2) +1e-10

                aux1= 1-(0.9**Tempo)
                aux2 = 1 - (0.999**Tempo)
    
                P12 = P12 + self.rate*( (massaP12/aux1) / np.sqrt(veloP12/aux2) )
                P23 = P23 + self.rate*( (massaP23/aux1) / np.sqrt(veloP23/aux2) )
       
                Gd2 = - e2 
                Gd3 = - e3 

                massaB2 = 0.9*massaB2 + (1-0.9)*Gd2
                massaB3 = 0.9*massaB3 + (1-0.9)*Gd3

                veloB2 = 0.999*veloB2 + (1-0.999)*(Gd2**2) +1e-10
                veloB3 = 0.999*veloB3 + (1-0.999)*(Gd3**2) +1e-10
    
                B2 = B2 + self.rate*( (massaB2/aux1) / np.sqrt(veloB2/aux2) )
                B3 = B3 + self.rate*( (massaB3/aux1) / np.sqrt(veloB3/aux2) )
 

        print('100%')

        if (self.sbw==1):            
            P12 = P12m*1
            P23 = P23m*1
            B2 = B2m*1
            B3 = B3m*1


        #Salva os pesos e bias em arquivos txt----------------------------------------------------------
        np.save(nomepasta + "net.npy", self.nn1c + self.nn2c*1e3 + self.nn3c*1e6)
        np.save(nomepasta + "netati.npy", self.fa2c + self.fa3c*1e3)
        np.save(nomepasta + "norm.npy", self.norma + self.normout*1e3)

        np.save(nomepasta + "P12.npy", P12)
        np.save(nomepasta + "P23.npy", P23)
        np.save(nomepasta + "B2.npy", B2)
        np.save(nomepasta + "B3.npy", B3)

        if (self.sbw==1):
            VetorErro[0] = itememo
            np.save(nomepasta + "Convergencia.npy", VetorErro)

        #Salva os pesos para checagem humana
        np.savetxt(nomepasta + "P12.txt", P12)
        np.savetxt(nomepasta + "P23.txt", P23)
        np.savetxt(nomepasta + "B2.txt", B2)
        np.savetxt(nomepasta + "B3.txt", B3)    

        tfim = time.time()
        print('runtime(s) = ' , tfim-tinicio)




###############################################################
###############################################################
################ Aplication of NN   ###########################
###############################################################
###############################################################




    #make prediction----------------------------------------------------------
    def Predict(self, matX):
        
        #pesos
        P12 = np.zeros((self.nn1c,self.nn2c))
        P23 = np.zeros((self.nn2c,self.nn3c))
        #bias
        B2= np.zeros((self.nn2c))
        B3= np.zeros((self.nn3c))
        #camadas
        c1= np.zeros((self.nn1c))
        c2= np.zeros((self.nn2c))
        c3= np.zeros((self.nn3c))

        #ajuste do local de salvamento, se especificado
        if (self.namenet==''):
            nomepasta=''
        else:
            nomepasta = self.namenet + '/'
            

        try: #Inicializa com pesos ja salvos, se existir esses arquivos-------------------------------------

            net02 = np.load(nomepasta + "net.npy")            
            net01 = self.nn1c + self.nn2c*1e3 + self.nn3c*1e6
            if (net01 != net02):
                input('Neural network saves this different from configured network')
                exit()

            net03 = np.load(nomepasta + "netati.npy")            
            net04 = self.fa2c + self.fa3c*1e3
            if (net03 != net04):
                input('Activation functions saves this different from configured network')
                exit()

            net05 = np.load(nomepasta + "norm.npy")            
            net06 = self.norma + self.normout*1e3
            if (net05 != net06):
                input('Normalization saves this different from configured network')
                exit()

            P12 = np.load(nomepasta + "P12.npy")
            P23 = np.load(nomepasta + "P23.npy")                      
            B2 = np.load(nomepasta + "B2.npy")
            B3 = np.load(nomepasta + "B3.npy")  
                
        except: #se nao tem pesos salvos encerra o programa-------------------------------

           input('No saved weight files')
           exit()

        #Normaliza a entrada de data----------------------
        matX = self.Normalize2(matX,nomepasta + "vmax_in.npy",nomepasta + "vmin_in.npy",nomepasta + "media_in.npy",nomepasta + "desvio_in.npy") 

        
        #Predição----------------------------
        numdata = len(matX)
        Calculated = np.zeros((numdata, self.nn3c)) #inicializa a matriz dos resultados Calculated
        
        for caso in range (0, numdata):

            #Camada 1, data de entrada
            c1 = matX[caso,:self.nn1c]                     
                
            #propagacao sinal
            c2 = np.dot(c1,P12)- B2     
            c2 = self.Activation(self.fa2c,c2)

            c3 = np.dot(c2,P23)- B3
            c3 = self.Activation(self.fa3c,c3)       

            # saida----------------------------
            Calculated[caso][:] = c3[:]

        Calculated = self.DesNormalizeout(Calculated, nomepasta + "vmax_out.npy", nomepasta + "vmin_out.npy",nomepasta + "media_out.npy",nomepasta + "desvio_out.npy") 

        if (self.txt!=0): #print txt out data
             np.savetxt(nomepasta + "out.txt", Calculated)

        return Calculated




###############################################################
###############################################################
################ Auxliliar plot   #############################
###############################################################
###############################################################




    #Plota a convergencia ----------------------------------------------------------
    def Plotconv(self):

        if (self.sbw==1):
            
            #ajuste do local de salvamento, se especificado
            if (self.namenet==''):
                nomepasta=''
            else:
                nomepasta = self.namenet + '/'

            
            #grafico da convergencia
            Conve = np.load(nomepasta + "Convergencia.npy")
            tamanho = len(Conve)
        
            MenorErro = np.min(Conve)
            itemenorerro = Conve[0]

            eixoX = np.zeros((tamanho-1)) 
            eixoY = np.zeros((tamanho-1))

            eixoX = np.arange(0, tamanho-1, dtype=int)
            eixoY = Conve[1:tamanho]
    
            plt.figure(figsize=(12, 5))
            plt.title('Mean squared error = ' + str(MenorErro) + ', iteration number = ' + str(itemenorerro))
            plt.xlabel('Study data')
            plt.ylabel('Error, mse')
            plt.plot(eixoX, eixoY, marker = '', color = 'darkblue')  
            plt.show()





###############################################################
###############################################################
################ Auxliliar calculation   ######################
###############################################################
###############################################################


    #Mean squared error  ----------------------------------------------------------
    def MSE(self):

        if (self.sbw==1):
            
            #ajuste do local de salvamento, se especificado
            if (self.namenet==''):
                nomepasta=''
            else:
                nomepasta = self.namenet + '/'

            
            #grafico da convergencia
            Conve = np.load(nomepasta + "Convergencia.npy")
            tamanho = len(Conve)
        
            MenorErro = np.min(Conve)
            itemenorerro = Conve[0]

            return MenorErro


