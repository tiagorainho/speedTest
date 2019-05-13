import socket
import sys
import psutil
import csv
import json  
import random
import time
import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import MD5

def NumValidoArg(arr):
    if (len(arr) <= 3):
        print("python3 client.py interval num [country or id]")
        sys.exit(0)

def TratArgumentos(arr):
    arg=""
    #receber todos os argumentos numa string
    for x in range(3, len(arr)):
        if x==len(arr)-1:
            arg = arg + arr[x]
        else:
            arg = arg + arr[x] + " "   
    return arg

def ArgNumerico(arr):
    if arr[1].isnumeric() and arr[2].isnumeric():
        
        #nao permitir que intervalo seja negativo
        if (int)(arr[1])<0:

            #mostrar mensagem de aviso
            print("Intervalo invalido: %d"%arr[1])

            #terminar programa
            sys.exit(0)
        
        #nao permitir que numero de etstes seja negativo
        if (int)(arr[2])<0:

            #mostrar mensagem de aviso
            print("Numero de testes invalido: %d"%arr[2])

            #terminar programa
            sys.exit(0)

    #caso ou o intervalo ou o numero de testes não sejam numericos
    else:

        #mostrar mensagem de aviso
        print("Primeiros 2 argumentos necessitam de ser numeros positivos")

        #terminar o programa
        sys.exit(0)
    
def tratArg3(arr, arg):
    try:
        ficheiro="servers.json"
        with open(ficheiro) as ficheiro:
        #atribuicao de dados dentro do ficheiro a variaveis em python
            servers=json.load(ficheiro)
    
    #apanhar exceçao caso o ficheiro não exista
    except IOError:
        print("Ficheiro "+ ficheiro + " não existe.")
        sys.exit(0) 

    count=0
    countServers=0
    dados = [ 0,0 ]
    #caso o 3º argumento seja numerico
    if arr[3].isnumeric():

        #varrer os servidores
        for server in servers['servers']:

            #caso o id seja encontrado
            if server['id'] == int(arg):
                count=count+1
                id=int(arg)
                print(server['name'])
                host= server['host']
                break
        else:
            print("O servidor nao existe")
            sys.exit(0)
    else: #quando é inserido nome de país
        #print("country : %s"%arg)
        for server in servers['servers']:
            countServers=countServers+1
            if server['country'] == arg:
                count=count+1
                #print(server['name'])
        if count==0:

            #ligamo-nos a um server qualquer se não houvver nenhum server no país inserido 
            a= random.randint(0, countServers-1)
            count=0
            for i in servers['servers']:
                if count == a:
                    print(i['name'])
                    host= i['host']
                    id=i['id']
                    break
                count=count+1
            print(a)
        else:

            #cria um valor entre 0 e o numero de servers do pais
            a=random.randint(0, count-1)
            count=0

            #correr os servidores
            for i in servers['servers']:

                #caso o pais seja igual ao argumento passado
                if i['country'] == arg:
                    if count == a:
                        print(i['name'])
                        host= i['host']
                        id=i['id']
                        break
                    count=count+1
    dados[0]=host
    dados[1]=id
    return dados

def Ping(site,porta,numTestes):
    
    #criar socket
    tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #definir valor de timeout
    tcp_s.settimeout(10)

    print("Connecting to " + site + " : " + porta + " ...")

    try:
        #ligaçao aos servidor
        tcp_s.connect( (site, int(porta)))

        #enviar mensagem ao servidor
        tcp_s.send(b"HI\n")

        #receber mensagem do servidor
        inf=tcp_s.recv(4096) ## caso off, systemOut

    #Apanhar exceçoes
    except socket.timeout:
        print("Tempo maximo de ligaçao expirado")
        return -1
    except socket.error:
        print("Erro com o socket")
        return -1

    #definir valores default
    mediaPing=0
    reps=numTestes
    pingTotal=0

    #loop
    for i in range(reps+2):

        try:

            #mensagem para enviar ao servidor
            str_data = "PING <timespamp>\n".encode("utf-8")

            #enviar mensagem ao servidor
            tcp_s.send(str_data)

            #receber mensagem do servidor
            str_data = tcp_s.recv(4096).decode("utf-8")

        #Apanhar exceçoes
        except socket.timeout:
            print("Tempo maximo de ligaçao expirado")
            return -1
        except socket.error:
            print("Erro com o socket")
            return -1

        #dividir a mensagem recebida pelo servidor sempre que encontre uma espaço
        data_to_split=str_data.split(" ")

        #guardar o valor do pong
        server_pong=data_to_split[1]
        
        #eliminar o primeiro resultado
        if i>1:

            #incrementar constantemente o ping
            pingTotal=pingTotal+(int(server_pong)-int(pongAnterior))

        #guardar o ping anterior para o proximo calculo de Ping
        pongAnterior=server_pong

    #calcular a média das latências
    mediaPing=pingTotal/reps 

    #returnar a media dos Pings para diminuir erros
    return mediaPing

def Download(host,porta):

    #criar socket
    tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #definir valor de timeout
    tcp_s.settimeout(10)

    #print("Connecting to " + site + " : " + porta + " ...")

    try:
        #ligaçao aos servidor
        tcp_s.connect( (site, int(porta)))

        #enviar mensagem ao servidor
        tcp_s.send(b"HI\n")

        #receber mensagem do servidor
        inf=tcp_s.recv(4096) ## caso off, systemOut
    
    #Apanhar exceçoes
    except socket.timeout:
        print("Tempo maximo de ligaçao expirado")
        return 0
    except socket.error:
        print("Erro com o socket")
        return 0

    #criar numero aleatorito para fazer download entre 10 e 100
    downloadMbs = random.randint(10,100)

    #quantidade de bytes de 1 Mb
    Mb=1024

    #valor de download a fazer
    valor=downloadMbs

    #começar a contar tempo
    tempoStartDownload=time.time()

    #valor inicial do download feito
    DownloadTotal=0

    #indicar começo do teste de velocidade
    print("> Teste de velocidade de internet iniciado! <")

    while 1:
        try:
            #comando para executar
            str_data = ("DOWNLOAD <" + str(1024) + ">\n").encode("utf-8")

            #enviar o pacote
            tcp_s.send(str_data)

            #contar tempo para depois saber se passaram 10 segundos ou n
            tempoAnterior=time.time()
            
            #receber o pacote
            resp = tcp_s.recv(1024)
        
        #Apanhar exceçoes
        except socket.timeout:
            print("Tempo maximo de ligaçao expirado")
            return 0

        except socket.error:
            print("Erro com o socket")
            return 0

        #incrementar o valor dos mbs recebidos
        #DownloadTotal+=len(resp)
        DownloadTotal+=1

        #começar a contar o tempo apartir do 1 Mb
        if DownloadTotal==Mb:
            tempoStartDownload=time.time()

        #terminar download quando chega ao valor pretendido
        if DownloadTotal >= valor:
            tempoFinalDownload=time.time()
            
            #comando para avisar o servidor que vai terminar a operacao
            str_data = "QUIT\n".encode("utf-8")
            tcp_s.send(str_data)

            #fechar a ligaçao ao servidor
            tcp_s.close()

            #terminar o while
            break

        tempoDepois = int(time.time())

        #calcular o tempo entre o tempo inicial dentro do while e final
        deltaTime = int(tempoDepois - tempoAnterior)

        #caso a variaçao do tempo seja superior a 10 segundos ou não haja resposta 
        if deltaTime >= 10 or not resp:
            
            #averiguar tempo de download
            tempoFinalDownload = time.time()

            #calcular a quantidade de mbs realmente recebidos
            DownloadTotal = round(DownloadTotal / Mb)

            #fechar ligacao ao servidor
            tcp_s.close()

            #terminar o while
            break

    #calcular valor da diferença entre o tempo inicial e final do download
    downloadTime = (tempoFinalDownload - tempoStartDownload)

    #calculo da velocidade
    velocidade = round(float((DownloadTotal-1)/downloadTime),2)

    #mostrar os valores da velocidade
    #print("Descarregados " + str(DownloadTotal-1) +" Mbs em " + str(round(downloadTime,2)) + " segundos")

    #returnar a velocidade em Mbs
    return velocidade

#contador, id do server, data em iso, latencia, largura de banda e tudo junto sem espaços(check)
def storingData(ficheiro,x,id,data,ping,download):

    #abrir ficheiro
    file = open(ficheiro, "a")

    #frase a gravar no ficheiro
    frase = str(x) + ", " + str(id) + ", " + str(data) + ", " + str(ping) + ", " + str(download) + ", "

    #produzir o check
    check = str(x) + str(id) + str(data) + str(ping) + str(download)

    #escrever a frase no ficheiro
    file.write(frase + check + "\n")

    #fechar o ficheiro e dessa forma grava-lo
    file.close()

    #libertar memória
    #file.flush()

def encryptFile(ficheiroComKey, ficheiroParaEscrever, ficheiro):

    #abrir ficheiro com a chavePingPingPingPing
    fkey=open(ficheiroComKey, "rb")

    #ler ficheiro com a chave
    fkeyRead = fkey.read()

    #fechar ficheiro com a chave
    fkey.close()

    #importar a chave
    keyPair=RSA.importKey(fkeyRead, "senha")

    #guardar par de chaves
    cipher=PKCS1_OAEP.new(keyPair)

    #abrir ficheiro csv
    fich = open(ficheiro, "r")

    #abrir ficheiro para escrever
    file = open(ficheiroParaEscrever,"w")

    #receber o valor hash do ficheiro
    hash = hashMD(ficheiro)

    #cifrar o hash
    strCifrada=cipher.encrypt(hash.encode("utf-8"))

    #escrever no ficheiro sig o conteudo do ficheiro csv em hash, cifrado
    file.write(str(strCifrada))

    #fechar ficheiro sig
    file.close()

    #fechar ficheiro csv
    fich.close()

def hashMD(ficheiro):

    #abrir ficheiro
    ficheiro = open(ficheiro,"r")

    #ler ficheiro
    fichContent = ficheiro.read()

    #iniciar variavel para adicionar String para fazer hash
    h = MD5.new()

    #atualizar a variavel para fazer hash
    h.update( fichContent.encode('utf-8') )

    #returnar o valor hash
    return h.hexdigest()

def generateRSAkey(ficheiro,senha):

    #criar RSA key
    key=RSA.generate(1024)

    #criar ficheiro com key
    file = open(ficheiro, "wb")

    #preparar para exportar
    export=key.exportKey("PEM",senha)

    #escrever a key no ficheiro
    file.write(export)

    #fechar o ficheiro
    file.close()

def deleteFile(ficheiro):

    #abrir o ficheiro em wb para apagar os dados nele contido
    file = open(ficheiro, "wb")

    #fechar o ficheiro
    file.close()

#/////////////////// MAIN ///////////////////////////////////////////////////////

#verificar se os valores dados sao legitimos
NumValidoArg(sys.argv)

#juntar os argumentos
arg = TratArgumentos(sys.argv)

#averiguar se os argumentos sao validos e numericos
ArgNumerico(sys.argv)

#receber o servidor a comunicar
dados= tratArg3(sys.argv, arg)

#guardar host do servidor
host=dados[0]

#guardar id do servidor
id=dados[1]

#guardar o valor de numero de testes
numTestes=sys.argv[2]

#guardar o valor de intervalo em segundos
intervalo=sys.argv[1]

#dividir String
x=str(host).split(":")

#receber parte relativa ao site
site=x[0]

#receber parte relativa a porta
porta=x[1]

#nome do ficheiro
ficheiro = "report.csv"

#atribuir nome ao ficheiro para onde vamos escrever o conteudo do ficheiro csv mas cifrado
ficheiroParaEscrever = "report.sig"

#atribuir nome ao ficheiro com key
ficheiroComKey="key.priv"

#eliminar dados no ficheiro csv
deleteFile(ficheiro)

#eliminar dados no ficheiro sig
deleteFile(ficheiroParaEscrever)

#eliminar dados no ficheiro priv (que possui a chave)
deleteFile(ficheiroComKey)

#gerar RSA key
generateRSAkey(ficheiroComKey, "senha")

#definir numero de testes para calcular o ping
numTestesPing=10

#não permitir que se façam menos que 3 testes de Ping 
if numTestesPing<3:
    print("Erro com o numero de testes para calcular o Ping, mude o valor de maneira a ser superior a 2")
    sys.exit(0)

for x in range(int(numTestes)):

    #terminar o programa quando não houver mais testes a fazer
    if x==numTestes:
        sys.exit(0)

    #calcular Ping
    ping = Ping(site,porta,numTestesPing)

    #calcular teste de velocidade de download
    download = Download(host,porta)

    #caso o ping seja -1 e o download 0, entao houve erro com o servidor
    if ping==-1 and download==0:
        
        #mostrar mensagem de erro
        print("Ocorreu um erro com a comunicação com o servidor")

    else:

        #mostrar Ping
        print("Ping: %d"%ping)

        #mostrar velocidade de download
        print("Velocidade de download: %.1f mbs"%download)

        #mostrar testes concluidos
        print("Teste %d concluido!"%(x+1))
        
    #dar uma linha de intervalo entre cada teste
    print()

    #data em iso
    data = datetime.datetime.now().isoformat()    

    #guardar a informacao num ficheiro csv
    storingData(ficheiro,x+1,id,data,ping,download)

    #esperar que passe o tempo necessário para o proximo teste
    time.sleep(int(intervalo))

#guardar ficheiro cifrado
encryptFile(ficheiroComKey, ficheiroParaEscrever, ficheiro)

