# -*- coding:utf-8 -*-
from threading import *
from socket import *
import pymysql as mdb
import requests
import os

class ServerSocket:
    def __init__(self):
        self.numnum = 0
        try:
            self.databasent = mdb.connect('localhost', 'root', '789521', 'db_testin')
            print("Successfully Connected To DB")
        except mdb.Error as e:
            print('Not Connected Succefully To DB')

        self.bListen = False
        self.clients = []
        self.chat_clients = []
        self.ip = []
        self.chat_ip = []
        self.threads = []

        self.serverThreads = []

        self.t = Thread(target=self.start, args=('',int(3333),))#main server
        self.t.start()
        self.serverThreads.append(self.t)

        self.t = Thread(target=self.start, args=('',int(3334),))#chat server
        self.t.start()
        self.serverThreads.append(self.t)


    def __del__(self):
        self.stop()

    def start(self, ip, port):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        try:
            self.server.bind((ip, port))
        except Exception as e:
            print('Bind Error : ', e)
            return False
        else:
            self.bListen = True
            self.t = Thread(target=self.listen, args=(self.server,port,))
            self.t.start()
            print('Server Listening...')
            self.resourceInfo()
        return True

    def stop(self):
        self.bListen = False
        if hasattr(self, 'server'):
            self.server.close()
            print('Server Stop')

    def listen(self, server, port):
        while self.bListen:
            server.listen(5)
            try:
                client, addr = server.accept()
            except Exception as e:
                print('Accept() Error : ', e)
                break
            else:


                print(str(port)+"(server): "+str(client)+' 클라이언트 접속')

                if port == int(3333): #main server receive
                    self.clients.append(client)
                    self.ip.append(addr)

                    t = Thread(target=self.receive, args=(addr, client))
                    self.threads.append(t)
                    t.start()
                else:# chat server receive
                    self.chat_clients.append(client)
                    self.chat_ip.append(addr)

                    t = Thread(target=self.chat_receive, args=(addr, client))
                    self.threads.append(t)
                    t.start()

        self.removeAllClients()
        self.server.close()

    def chat_receive(self, addr, client):
        while True:
            try:
                recv = client.recv(1024)
            except Exception as e:
                print('Recv() Error :', e)
                break
            else:
                com = str(recv, encoding='utf-8')

                print('3334 msg:'+ com)
                com = com.split(' ')

                if len(com) != 1:
                    commend = com[0]
                    side = []
                    for i in range(1,len(com)):
                        side.append(com[i])
                else:
                    commend = com[0]

                print('3334: '+ commend)

                if commend == 'exit':
                    self.chat_ip.remove(addr)
                    self.chat_clients.remove(client)

                    client.send('stop'.encode('utf-8'))
                    break

                elif commend == 'chat_update':
                    data = 'update'
                    #채팅방에 들어와 있는 애들만 어떻게 선정?
                    # print(self.clients)
                    for c in self.chat_clients:
                        print(c)
                        print(data)
                        c.send(data.encode('utf-8'))


    def receive(self, addr, client):
        while True:
            try:
                recv = client.recv(1024)
                print('recv:'+str(len(recv)))
            except Exception as e:
                print('Recv() Error :', e)
                break
            else:
                msg = str(recv, encoding='utf-8')

                print('3333 msg: '+msg)

                msg = msg.split(' ')

                if len(msg) != 1:
                    commend = msg[0]
                    side = []
                    for i in range(1,len(msg)):
                        side.append(msg[i])
                else:
                    commend = msg[0]

                print('3333: '+ commend)

                if commend == 'login':
                    cur = self.databasent.cursor()
                    #cur.execute("SELECT student_id FROM student_id WHERE student_id =" + str(side[0]) + "")
                    cur.execute("SELECT * FROM student_id ")
                    allSQLRows = cur.fetchall()

                    #첫 로그인하는 사람인 경우
                    if len(allSQLRows) == 0:
                        print('aa')
                    else:
                        cur = self.databasent.cursor()
                        cur.execute("SELECT lecture_id FROM student_course WHERE student_id =" + str(side[0]) + "")
                        # cur.execute("SELECT no,professor_name FROM lecture WHERE professor_id ='" + str(side[0]) + "'")
                        allSQLRows = cur.fetchall()

                        lectures = allSQLRows
                        print("강의수: "+ str(len(allSQLRows)))
                        # print(lectures)

                        if len(lectures) != 0:
                            lectureId = ""

                            for i in range(len(lectures)):
                                lectureId += str(lectures[i][0]) + " "
                            if len(lectures[0])>1:
                                lectureId += str(lectures[0][1]) + " "
                            lectureId = lectureId.rstrip()
                            # print(lectureId)
                            client.send(lectureId.encode('utf-8'))
                        else:
                            print('lecture 없다')
                            lectureId = "x"
                            # print(lectureId)
                            client.send(lectureId.encode('utf-8'))

                elif commend == 'lecture':
                    cur = self.databasent.cursor()
                    lecture_info = ""
                    print(side)
                    for i in range(len(side)):
                        cur.execute("SELECT lecture_name,professor_name,lecture_code FROM lecture WHERE no =" + str(side[i]) + "")
                        allSQLRows = cur.fetchall()
                        print(allSQLRows)
                        lecture_info += allSQLRows[0][0] + ","
                        lecture_info += allSQLRows[0][1] + ","
                        lecture_info += allSQLRows[0][2] + "/"

                    print('클라이언트로 lecture 정보 전송')
                    client.send(lecture_info.encode('utf-8'))

                elif commend == 'groupSearch':
                    print('그룹 조회 왔다')
                    cur = self.databasent.cursor()
                    group_info = ""
                    for i in range(len(side)):
                        cur.execute("SELECT no,lecture_name,professor_name FROM lecture WHERE lecture_code ='" + str(side[i]) + "'")
                        allSQLRows = cur.fetchall()

                        if len(allSQLRows) == 0:
                            group_info += 'x'

                        else:
                            group_info += str(allSQLRows[0][0]) + ","
                            group_info += str(allSQLRows[0][1]) + ","
                            group_info += str(allSQLRows[0][2]) + ","
                    client.send(group_info.encode('utf-8'))

                
                elif commend == 'groupInsert':
                    print('그룹 생성 왔다')
                    cur = self.databasent.cursor()
                    group_info = ""
                    cur.execute("SELECT no,lecture_name,professor_name FROM lecture WHERE professor_id ='" + str(side[1]) + "' AND lecture_name ='"+str(side[0])+"'")
                    allSQLRows = cur.fetchall()
                    print(allSQLRows)
                    print(len(allSQLRows))
                    
                    
                    
                    result= ""
                    if len(allSQLRows) == 0:
                        cur.execute("SELECT professor_name FROM lecture WHERE professor_id ='" + str(side[1]) + "'")
                        allSQLRows = cur.fetchall()
                        print(allSQLRows)
                        cur.execute("INSERT INTO lecture(lecture_name,lecture_code,professor_name,professor_id,student_num) VALUES('"+str(side[0])+"','A"+str(self.numnum%10)+"B"+str(self.numnum%10)+"','"+str(allSQLRows[0][0])+"','"+str(side[1])+"',0)")
                        self.databasent.commit()
                        self.numnum += 1
                        result += "add_success"
                    else:
                        result += "already" 
                    client.send(result.encode('utf-8'))

                elif commend == 'group_insert':
                    cur = self.databasent.cursor()
                    result_to_client = False

                    #학번으로 어떤 그룹에 속해있는지 검색 -> 그룹id로 나옴
                    cur.execute("SELECT lecture_id FROM student_course WHERE student_id ='" + str(side[1]) + "'")
                    allSQLRows = cur.fetchall()

                    if len(allSQLRows) == 0: #그룹 0개
                        print('asd')
                        cur = self.databasent.cursor()
                        cur.execute("SELECT lecture_code FROM lecture WHERE no ='" + str(side[0]) + "'")
                        lec_code = cur.fetchall()
                        lec_code = lec_code[0][0]
                        cur = self.databasent.cursor()
                        query = 'INSERT INTO student_course (student_id,lecture_id,lecture_code) Values (%s,%s,%s)'
                        cur.execute(query, (side[1], side[0], lec_code))

                        self.databasent.commit()
                        # print(str(side[1]+", "+str(side[0])))
                        print('저장 완료')
                        client.send('add_success'.encode('utf-8'))

                    else: #속해있는 그룹이 있음
                        # 이미 이 그룹에 속해있는지 확인
                        for i in range(len(allSQLRows)):
                            if str(allSQLRows[i][0]) == str(side[0]):
                                print('이미 이 그룹에 있음')
                                result_to_client = True
                                client.send('already'.encode('utf-8'))
                                break
                        #이 그룹에 속해 있지 않음
                        if result_to_client == False:
                            #DB에 이 정보 추가
                            cur = self.databasent.cursor()
                            cur.execute("SELECT lecture_code FROM lecture WHERE no ='" + str(side[0]) + "'")
                            lec_code = cur.fetchall()
                            lec_code = lec_code[0][0]
                            cur = self.databasent.cursor()
                            query = 'INSERT INTO student_course (student_id,lecture_id,lecture_code) Values (%s,%s,%s)'
                            cur.execute(query, (side[1],side[0],lec_code))

                            self.databasent.commit()
                            # print(str(side[1]+", "+str(side[0])))
                            print('저장 완료')
                            client.send('add_success'.encode('utf-8'))

                    # client.send(group_info.encode('utf-8'))

                elif commend == 'sendMsg':
                    # print(side)
                    cur = self.databasent.cursor()
                    query = 'INSERT INTO chatting (category_id,comment,nickname,student_id) Values (%s,%s,%s,%s)'
                    category_name = str(side[0])
                    lecid = str(side[1])
                    msg = str(" ".join(side[2:-1]))
                    stuid = str(side[-1])

                    cur.execute("SELECT nickname FROM user WHERE student_id ='" + str(stuid) + "'")
                    nick = cur.fetchall()
                    nick = nick[0][0]

                    #카테고리 정보 가져오기
                    cur.execute("SELECT no FROM category WHERE chatroom_name ='" + str(category_name) + "'"+ "AND lecture_id = '"+ str(lecid)+"'")
                    category_id = cur.fetchall()
                    # print(category_id)
                    cur.execute(query, (category_id, msg, nick,stuid))
                    self.databasent.commit()

                    client.send('o'.encode('utf-8'))
                    print('sendmsg끝')

                elif commend == 'chat_history':
                    print(side)
                    cur = self.databasent.cursor()
                    cur.execute("SELECT no FROM category WHERE lecture_id ='" + str(side[0]) + "'AND chatroom_name = '"+str(side[1])+"'")
                    category_id = cur.fetchall()

                    if len(category_id) != 0:
                        cur = self.databasent.cursor()
                        cur.execute("SELECT * FROM chatting WHERE category_id ='" + str(category_id[0][0]) + "'")
                        chat_log = cur.fetchall()

                        if len(chat_log) == 0:
                            result = 'x'
                            client.send(result.encode('utf-8'))
                        else:
                            result = ""
                            for i in range(len(chat_log)):
                                result += str(chat_log[i][4]) + "," #stuid
                                result += str(chat_log[i][3]) + "," #nickname
                                result += str(chat_log[i][2]) + "," #comment
                                result += str(chat_log[i][6]) + "," #likes
                                result += str(chat_log[i][1]) + "," #category_id
                                result += str(chat_log[i][5]) + "/" #time

                            client.sendall(result.encode('utf-8'))
                            print('chat_history 끝')
                    else:
                        print('history읽기 오류')
                        result = 'x'
                        client.send(result.encode('utf-8'))

                elif commend == 'get_lecture_id':
                    # print(side)
                    cur = self.databasent.cursor()
                    cur.execute("SELECT no FROM lecture WHERE lecture_code ='" + str(side[0]) + "'")
                    allSQLRows = cur.fetchall()

                    lecid = allSQLRows[0][0]
                    lecid = str(lecid)
                    client.send(lecid.encode('utf-8'))

                elif commend == 'getRank': #LeaderBoard 순위 가져오기
                    print(side)
                    cur = self.databasent.cursor()
                    #cur.execute("SELECT Depart,points FROM points WHERE Student_id ='" + str(side[1]) + "'")
                    cur.execute("SELECT department,point FROM user WHERE student_id ='" + str(side[1]) + "'")
                    allSQLRows = cur.fetchall()
                    Department = ""                    
                    if len(allSQLRows) > 0 :
                        Department += str(allSQLRows[0][0])
                    #Lecture_Id = ""
                    points = 0



                    for i in range(len(allSQLRows)):
                        #Lecture_Id += str(allSQLRows[i][2]) +" "
                        points += allSQLRows[i][1]
                    wholepoint = str(points)
                    if side[0] == '1':
                        UnivRank = ""
                        #cur.execute("SELECT sum(points) FROM points GROUP BY Student_id ORDER BY sum(points) DESC")
                        cur.execute("SELECT sum(point) FROM user GROUP BY student_id ORDER BY sum(point) DESC")
                        allSQLRows = cur.fetchall()
                        #전체 랭킹 서치
                        if len(allSQLRows) > 0 :
                            for i in range(len(allSQLRows)):
                                UnivRank += str(allSQLRows[0][0]) +" "
                    
                        print('asd')
                        print(str(UnivRank)+ "a")
                        client.send(str(UnivRank).encode('utf-8'))
                    elif side[0] == '2':
                        inDeptRank = ""
                        #cur.execute("SELECT sum(points) FROM points WHERE Depart = '"+Department+"' GROUP BY Student_id ORDER BY sum(points) DESC")
                        cur.execute("SELECT sum(point) FROM user WHERE department = '"+Department+"' GROUP BY student_id ORDER BY sum(point) DESC")
                        allSQLRows = cur.fetchall()
                        #과내 랭킹 서치
                        if len(allSQLRows) > 0 :
                            for i in range(len(allSQLRows)):
                                inDeptRank += str(allSQLRows[0][0]) +" "
                    
                        print('bcd')
                        print(str(inDeptRank) + "a")
                        client.send(str(inDeptRank).encode('utf-8'))
                    elif side[0] == '3':
                        DeptRank = ""
                        #cur.execute("SELECT sum(points) FROM points GROUP BY Depart ORDER BY sum(points) DESC")
                        cur.execute("SELECT sum(point) FROM user GROUP BY department ORDER BY sum(point) DESC")
                        allSQLRows = cur.fetchall()
                        #과별 랭킹 서치
                        if len(allSQLRows) > 0 :
                            for i in range(len(allSQLRows)):
                                DeptRank += str(allSQLRows[0][0]) +" "
                    
                        print('efg')
                        print(str(DeptRank)+ "a")
                        client.send(str(DeptRank).encode('utf-8'))

                    #elif side[0] == '4':
                    #    cur.execute("SELECT Depart,Lec_id,points FROM lecture WHERE Student_id ='" + str(side[1]) + "' AND Lec_id =")
                    #    allSQLRows = cur.fetchall()
                    #    #강의별 랭킹 서치
                    #    print('efg')
                    #    client.send('4'.encode('utf-8'))
                  
                
                elif commend == 'getCategory':
                    cur = self.databasent.cursor()
                    cur.execute("SELECT chatroom_name FROM category WHERE lecture_id ='" + str(side[0]) + "'")
                    category = cur.fetchall()
                    result = ""

                    for i in range(len(category)):
                        result += str(category[i][0]) +","

                    client.send(result.encode('utf-8'))

                elif commend == 'category_create':
                    print(side)
                    cur = self.databasent.cursor()
                    cur.execute("SELECT lecture_code FROM lecture WHERE no ='" + str(side[0]) + "'")
                    lecture_code = cur.fetchall()[0][0]
                    print(lecture_code)

                    query = 'INSERT INTO category (lecture_code,lecture_id,chatroom_name) Values (%s,%s,%s)'
                    cur.execute(query, (lecture_code, side[0], side[1]))
                    self.databasent.commit()
                    print('굿?')

                elif commend == 'HowManyChat':
                    cur = self.databasent.cursor()
                    print(msg)
                    print("Finding lecno...")
                    cur.execute("SELECT no FROM lecture WHERE lecture_name ='" + str(side[0]) + "' AND professor_name = '" + str(side[1]) + "'")
                    allSQLRows = cur.fetchall()
                    lecno = allSQLRows[0][0]
                    # print(lecno)
                    cur.execute("SELECT no FROM category WHERE lecture_id =" + str(lecno) + "")
                    allSQLRows = cur.fetchall()
                    catno = allSQLRows[0][0]
                    # print(catno)
                    cur.execute("SELECT count(*) FROM chatting WHERE category_id =" + str(catno) + "")
                    allSQLRows = cur.fetchall()
                    count = allSQLRows[0][0]
                    # print(str(count))
                    print('클라이언트로 chatCount 전송')
                    client.send(str(count).encode('utf-8'))

                elif commend == 'firstLogin':
                    print(side)
                    cur = self.databasent.cursor()
                    cur.execute("SELECT * FROM student_id WHERE student_id =" + str(side[0]) + "")
                    result = cur.fetchall()
                    if len(result) != 1:
                        client.send('first'.encode('utf-8'))
                    else:
                        client.send('already_registerd'.encode('utf-8'))

                elif commend == 'register':
                    print(side)
                    cur = self.databasent.cursor()
                    query = 'INSERT INTO user (student_id,name,nickname,department) Values (%s,%s,%s,%s)'
                    cur.execute(query, (str(side[3]), str(side[2]), str(side[0]), str(side[1])))
                    self.databasent.commit()

                    query = 'INSERT INTO student_id (student_id) Values (%s)'
                    cur.execute(query, str(side[3]))
                    self.databasent.commit()

                    print(str(side[3])+'등록 완료')
                    client.send('registered'.encode('utf-8'))

                elif commend == 'like_update':
                    studid = str(side[0])
                    msg = str(" ".join(side[1:]))

                    cur = self.databasent.cursor()
                    cur.execute("UPDATE chatting SET likes = likes+1 WHERE student_id ='" + studid + "' AND comment = '" + msg + "'")
                    self.databasent.commit()
                    print('좋아요 업데이트')
                    client.send('like_updated'.encode('utf-8'))

                elif commend == 'exit':
                    self.removeClient(addr, client)
                    break


    def send(self, msg):
        try:
            for c in self.clients:
                c.send(msg.encode())
        except Exception as e:
            print('Send() Error : ', e)

    def removeClient(self, addr, client):
        client.close()
        self.ip.remove(addr)
        self.clients.remove(client)

        i = 0
        for t in self.threads[:]:
            if not t.isAlive():
                del (self.threads[i])
            i += 1

        self.resourceInfo()

    def removeAllClients(self):
        for c in self.clients:
            c.close()

        self.ip.clear()
        self.clients.clear()
        self.threads.clear()

        self.resourceInfo()

    def resourceInfo(self):
        print('Number of Client ip\t: ', len(self.ip))
        print('Number of Client socket\t: ', len(self.clients))
        print('Number of Client thread\t: ', len(self.threads))

if __name__ == '__main__':
    server = ServerSocket()
