from http import client
import socket
from threading import Thread
import time
from datetime import datetime

#시각입력
timer=time.ctime()

#포트,ip 직접입력
PORT=int(input("포트번호를 입력하세요 : "))
IPNUM=(input("IP번호를 입력하세요 : "))

#실험용 코드
#IPNUM = '%s'%socket.gethostbyname(socket.gethostname())   # ip주소
#PORT = 9099               # 서버의 포트 번호 

f=open('client_%s.txt'%datetime.today().strftime('%Y-%m-%d'),'a')
f.write("======"+time.ctime()+"======") #정확한 시각 입력
f.close()

# /***********************
#    * 작성자: 김선민
#    * 작성일: 2022-01-14
#    *
#    * Param: 소켓
#    * Description: 메세지 수신하고 화면에 출력후 파일 쓰기 함수
#    * Return: 
#    ************************/


def rcvMessage(sock):
    while True:
        try:
            data = sock.recv(1024) #메세지 수신 
            if not data:    
                break
            print(data.decode())    #수신받은 메세지 출력
            f=open('client_%s.txt'%datetime.today().strftime('%Y-%m-%d'),'a')   #파일 열기
            f.write("\n")
            f.write(data.decode())  #파일쓰기
            f.write("\n")
            f.close() #파일닫기
            
        except:
            pass


# /***********************
#    * 작성자: 김선민
#    * 작성일: 2022-01-14
#    *
#    * Param: 
#    * Description: 소켓 객체를 생성해서 서버와 연결하는 함수
#    * Return: 
#    ************************/
def runChat():
    #with=구문 실행후 자동으로 close하게해줌
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            #소켓 객체를 생성
            #AF_INET=주소체계중 IPv4인터넷 프로토콜
            #SOCK_STREAM 소켓 계속 연결상태 유지
        sock.connect((IPNUM, PORT))  #서버로 연결시도
        t = Thread(target=rcvMessage, args=(sock,)) #메세지를 보낼 쓰레드
        t.daemon = True #데몬 쓰레드
        #데몬쓰레드=백그라운드에서 실행되는 쓰레드로 메인 쓰레드가 종료되면 즉시 종료되는 쓰레드
        
        t.start() #쓰레드 시작!

        while True:
            message = input() #메세지 입력
            if message == '/quit':  #/quit할때까지 반복
                sock.send(message.encode())
                break
                
            sock.send(message.encode()) #메세지 송신
            
runChat()
