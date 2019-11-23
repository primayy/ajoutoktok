# -*- coding:utf-8 -*-
from threading import *
from socket import *
import pymysql as mdb
import requests
import os
import datetime
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
                    #여기서 가끔 문제발생
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
                        cur.execute("SELECT lecture_name,lecture_code FROM lecture WHERE no =" + str(side[i]) + "")
                        allSQLRows = cur.fetchall()
                        print(allSQLRows)
                        lecture_info += allSQLRows[0][0] + ","
                        lecture_info += allSQLRows[0][1] + "/"

                    print('클라이언트로 lecture 정보 전송')
                    client.send(lecture_info.encode('utf-8'))

                elif commend == 'groupSearch':
                    print('그룹 조회 왔다')
                    print(side)
                    cur = self.databasent.cursor()
                    group_info = ""

                    cur.execute("SELECT no,lecture_name,lecture_code FROM lecture WHERE lecture_code ='" + str(side[0]) + "'")
                    allSQLRows = cur.fetchall()

                    if len(allSQLRows) == 0:
                        group_info += 'x'

                    else:
                        group_info += str(allSQLRows[0][0]) + ","
                        group_info += str(allSQLRows[0][1]) + ","
                        group_info += str(allSQLRows[0][2])

                    client.send(group_info.encode('utf-8'))

                elif commend == 'exitLecture':
                    print('그룹 나가기 들어옴')
                    print(side)

                    cur = self.databasent.cursor()
                    cur.execute("SELECT lecture_id FROM student_course WHERE student_id ='" + str(side[0]) + "' AND lecture_code ='"+str(side[1])+"'")
                    del_lecId = cur.fetchall()
                    del_lecId = str(del_lecId[0][0])
                    print(del_lecId)

                    cur.execute("delete FROM student_course WHERE student_id ='" + str(side[0]) + "' AND lecture_code ='"+str(side[1])+"'")
                    self.databasent.commit()

                    client.send(del_lecId.encode('utf-8'))


                elif commend == 'groupInsert':
                    # print('그룹 생성 왔다')
                    cur = self.databasent.cursor()
                    group_info = ""
                    cur.execute("SELECT no,lecture_name FROM lecture WHERE professor_id ='" + str(side[1]) + "' AND lecture_name ='"+str(side[0])+"'")
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

                elif commend == 'group_add':
                    print(side)

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
                    
                    #강의코드 가져오기
                    cur.execute("SELECT lecture_code FROM category WHERE chatroom_name ='" + str(category_name) + "'"+ "AND lecture_id = '"+ str(lecid)+"'")
                    lecture_code = cur.fetchall()
                    #점수 +
                    cur.execute("UPDATE points SET points = points + 5 WHERE Student_id='"+str(stuid)+"' AND Lec_id = '" + str(lecture_code[0][0]) + "'")
                    self.databasent.commit()

                    client.send('o'.encode('utf-8'))
                    print('sendmsg끝')

                elif commend == 'sendReplyMsg':
                    cur = self.databasent.cursor()

                    #답글 디비에 저장
                    query = 'INSERT INTO reply (chat_id,student_id,reply_comment) Values (%s,%s,%s)'

                    chat_id = str(side[0])
                    stuid = str(side[1])
                    msg = str(" ".join(side[2:]))
                    print(msg)

                    cur.execute(query, (chat_id, stuid, msg))
                    self.databasent.commit()
                    #방금 넣은 reply_id 찾기
                    cur.execute("SELECT count(*) FROM reply")
                    reply = cur.fetchall()
                    reply_id = reply[0][0]-1
                    #게시글 학생 학번,카테고리 id 찾기
                    cur.execute("SELECT student_id,category_id FROM chatting WHERE no ="+str(chat_id) )
                    chatResult = cur.fetchall()
                    chat_stuId = chatResult[0][0]
                    category_id = chatResult[0][1]

                    #카테고리 아이디로 강의코드 얻어오기
                    cur.execute("SELECT lecture_code FROM category WHERE no ="+str(category_id) )
                    lecCode = cur.fetchall()
                    lec_code = lecCode[0][0]

                    #알림 테이블에 입력
                    cur.execute("INSERT INTO alarm(chat_id,chat_student_id,reply_id,reply_student_id,reply_selected) Values ("+str(chat_id)+",'"+chat_stuId+"',"+str(reply_id)+",'"+stuid+"',0)")
                    self.databasent.commit()

                    #답글 달았을 때 포인트 정리 (5점 증가)
                    cur.execute("UPDATE points SET points = points + 5 WHERE Student_id='"+str(stuid)+"' AND Lec_id = '" + str(lec_code) + "'")
                    self.databasent.commit()

                    client.send('o'.encode('utf-8'))

                    print('답글 저장완료')


                elif commend == 'Alarm': #알림용
                    print(side)
                    ChatAlarmText = ""
                    ReplyAlarmText = ""
                    cur = self.databasent.cursor()
                    #내가 쓴 게시글의 댓글 개수(count(*))와 게시글 id
                    cur.execute("SELECT count(*),chat_id FROM alarm WHERE chat_student_id ='" + str(side[0]) + "' GROUP BY chat_id")
                    chatAlarm = cur.fetchall()
                    #내가 쓴 댓글의 게시글 id
                    cur.execute("SELECT chat_id FROM alarm WHERE reply_student_id ='" + str(side[0]) + "' AND reply_selected = 1")
                    replyAlarm = cur.fetchall()

                    if len(chatAlarm) > 0:
                        for i in range(len(chatAlarm)):
                            #게시글id로 카테고리id 얻기
                            cur.execute("SELECT category_id FROM chatting WHERE no =" + str(chatAlarm[i][1]) + "")
                            cat_id = cur.fetchall()
                            #카테고리id로 강의코드 얻기
                            cur.execute("SELECT lecture_code FROM category WHERE no =" + str(cat_id[0][0]) + "")
                            lec_co = cur.fetchall()
                            #강의코드로 강의이름 얻기
                            cur.execute("SELECT lecture_name FROM lecture WHERE lecture_code ='" + str(lec_co[0][0]) + "'")
                            lecture_name = cur.fetchall()
                            ChatAlarmText += lecture_name[0][0] + "," + str(chatAlarm[i][0]) +"." # "강의이름,댓글 수" 
                        ChatAlarmText = ChatAlarmText.rstrip()


                    if len(replyAlarm) > 0:
                        for i in range(len(chatAlarm)):
                            #위와 동일
                            cur.execute("SELECT category_id FROM chatting WHERE no =" + str(replyAlarm[i][0]) + "")
                            cat_id = cur.fetchall()
                            cur.execute("SELECT lecture_code FROM category WHERE no =" + str(cat_id[0][0]) + "")
                            lec_co = cur.fetchall()
                            cur.execute("SELECT lecture_name FROM lecture WHERE lecture_code ='" + str(lec_co[0][0]) + "'")
                            lecture_name = cur.fetchall()
                            ReplyAlarmText += lecture_name[0][0] + "." #강의 이름
                        ReplyAlarmText = ReplyAlarmText.rstrip()
                    AlarmText = ChatAlarmText + "/" + ReplyAlarmText
                    client.send(AlarmText.encode('utf-8'))
                
                
                elif commend == 'chat_history':
                    print(side)
                    cur = self.databasent.cursor()
                    cur.execute("SELECT no FROM category WHERE lecture_id ='" + str(side[0]) + "'AND chatroom_name = '"+str(side[1])+"'")
                    category_id = cur.fetchall()
                    print(category_id)
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
                                result += str(chat_log[i][5]) + "," #time
                                result += str(chat_log[i][0]) + "/" #chatting_id

                            client.sendall(result.encode('utf-8'))
                            print('chat_history 끝')
                    else:
                        print('history읽기 오류')
                        result = 'x'
                        client.send(result.encode('utf-8'))

                elif commend == 'replyHistory':
                    print(side)
                    cur = self.databasent.cursor()
                    cur.execute("SELECT * FROM reply WHERE chat_id ='" + str(side[0]) + "'")
                    reply = cur.fetchall()
                    # print(reply[0][4].strftime('%Y,%m,%d,%H,%M'))
                    if len(reply) != 0:
                        result = ""
                        for i in range(len(reply)):
                            print(reply[i][2])
                            result += str(reply[i][2]) +"," #msg
                            result += str(reply[i][3]) +"," #stuId
                            result += str(reply[i][4].strftime('%Y.%m.%d.%H.%M')) +"/" #time

                        client.sendall(result.encode('utf-8'))
                        print('reply 끝')
                    else:
                        client.send('x'.encode('utf-8'))
                        print('답글 없음')


                elif commend == 'get_lecture_id':
                    print(side)
                    cur = self.databasent.cursor()
                    cur.execute("SELECT no FROM lecture WHERE lecture_code ='" + str(side[0]) + "'")
                    allSQLRows = cur.fetchall()

                    lecid = allSQLRows[0][0]
                    lecid = str(lecid)
                    client.send(lecid.encode('utf-8'))

                #아이디 중복 확인
                elif commend == 'OvelapCheck':
                    print(str(side[0]))
                    Answer = ""

                    #특수문자 ㄴㄴ해
                    for i in range(len(str(side[0]))):
                        print("ord(str(side[0])[i])" + str(ord(str(side[0])[i])))
                        if 122 < ord(str(side[0])[i]):
                            Answer = "noMark"
                            print(Answer+"4")
                            client.send(Answer.encode('utf-8'))
                            
                        elif 90 < ord(str(side[0])[i]):
                            if 97 > ord(str(side[0])[i]):
                                Answer = "noMark"
                                print(Answer+"3")
                                client.send(Answer.encode('utf-8'))

                        elif 57 < ord(str(side[0])[i]):
                            if 65 > ord(str(side[0])[i]):
                                Answer = "noMark"
                                print(Answer+"2")
                                client.send(Answer.encode('utf-8'))

                        elif 48 > ord(str(side[0])[i]):
                            Answer = "noMark"
                            print(Answer+"1")
                            client.send(Answer.encode('utf-8'))

                    print(len(str(side[0])))
                    if len(Answer)==0:
                        if (len(str(side[0]))<4 or len(str(side[0]))>8):
                            Answer = "length" #짧은거 ㄴㄴ해 긴 것도 ㄴㄴ해
                            print(Answer)
                            client.send(Answer.encode('utf-8'))
                    # elif len(str(side[0]))>8:
                    #     Answer = "long" #긴 것도 ㄴㄴ해
                    #     client.send(Answer.encode('utf-8'))

                    cur = self.databasent.cursor()
                    cur.execute("SELECT nickname FROM user WHERE student_id ='" + str(side[0]) + "'")
                    allSQLRows = cur.fetchall()
                    if len(Answer)==0:
                        if len(allSQLRows) > 0:
                            Answer = "overlap" #있는 것도 ㄴㄴ해
                            client.send(Answer.encode('utf-8'))
                        else:
                            Answer = "newone" #없으면 괜찮음
                            client.send(Answer.encode('utf-8'))
                        print(Answer)

                elif commend == 'getRank': #LeaderBoard 순위 가져오기
                    print(side)
                    cur = self.databasent.cursor()
                    
                    cur.execute("SELECT department FROM user WHERE student_id ='" + str(side[1]) + "'")  #해당 유저의 학과 ==> '학과내'에 사용
                    allSQLRows = cur.fetchall()
                    Department = ""
                    if len(allSQLRows) > 0 :
                        Department = str(allSQLRows[0][0])

                    #for i in range(len(allSQLRows)):
                        #Lecture_Id += str(allSQLRows[i][2]) +" "
                        #points += allSQLRows[i][1]
                    #wholepoint = str(points)
                    if side[0] == '1':
                        UnivRank = ""
                        #학번으로 묶어서 포인트의 합과 학번을 얻는다(내림차순)
                        cur.execute("SELECT sum(points),Student_id FROM points GROUP BY Student_id ORDER BY sum(points) DESC")
                        #cur.execute("SELECT sum(point),student_id FROM user GROUP BY student_id ORDER BY sum(point) DESC")
                        allSQLRows = cur.fetchall()
                        #전체 랭킹 서치
                        if len(allSQLRows) > 0 :
                            for i in range(len(allSQLRows)):
                                cur.execute("SELECT nickname FROM user WHERE student_id ='" + str(allSQLRows[i][1]) + "'") #해당 학번의 닉네임 호출
                                allSQLRows2 = cur.fetchall()
                                print(">>>>>ID: " + str(allSQLRows2))
                                UnivRank += str(allSQLRows[i][0]) + "," + str(allSQLRows2[0][0]) + " " # "포인트,닉네임"
                        UnivRank.rstrip()
                        print(UnivRank)
                        client.send(str(UnivRank).encode('utf-8'))
                    elif side[0] == '2': #학과내
                        print(Department)
                        inDeptRank = ""
                        #학번으로 묶어서 포인트의 합과 학번을 얻는다(조건[같은학과], 내림차순)
                        cur.execute("SELECT sum(points),Student_id FROM points WHERE Depart = '"+Department+"' GROUP BY Student_id ORDER BY sum(points) DESC")
                        #cur.execute("SELECT sum(point) FROM user WHERE department = '"+Department+"' GROUP BY student_id ORDER BY sum(point) DESC") 리더보드는 유저 테이블로도 가능하지만 일단 points 테이블로 사용하였다.
                        allSQLRows = cur.fetchall()
                        #과내 랭킹 서치
                        if len(allSQLRows) > 0 :
                            for i in range(len(allSQLRows)):
                                cur.execute("SELECT nickname FROM user WHERE student_id ='" + str(allSQLRows[i][1]) + "'") #해당 학번의 닉네임 호출
                                allSQLRows2 = cur.fetchall()
                                print(">>>>>ID: " + str(allSQLRows2))
                                inDeptRank += str(allSQLRows[i][0]) + "," + str(allSQLRows2[0][0]) + " "  # "포인트,닉네임"
                        inDeptRank.rstrip()
                        print(inDeptRank)
                        client.send(str(inDeptRank).encode('utf-8'))
                    elif side[0] == '3':
                        DeptRank = ""
                        #학과로 묶어서 포인트의 합과 학과을 얻는다(내림차순)
                        cur.execute("SELECT sum(points),Depart FROM points GROUP BY Depart ORDER BY sum(points) DESC")
                        #cur.execute("SELECT sum(point) FROM user GROUP BY department ORDER BY sum(point) DESC") 리더보드는 유저 테이블로도 가능하지만 일단 points 테이블로 사용하였다.
                        allSQLRows = cur.fetchall()
                        #과별 랭킹 서치
                        if len(allSQLRows) > 0 :
                            for i in range(len(allSQLRows)):
                                DeptRank += str(allSQLRows[i][0]) + "," + str(allSQLRows[i][1]) + " " # "포인트,학과"
                        DeptRank.rstrip()
                        print(DeptRank)
                        client.send(str(DeptRank).encode('utf-8'))

                    #elif side[0] == '4': 강의실 내 포인트 비교... 적용여부미정, 보류
                    #    cur.execute("SELECT Depart,Lec_id,points FROM lecture WHERE Student_id ='" + str(side[1]) + "' AND Lec_id =") 리더보드는 유저 테이블로도 가능하지만 일단 points 테이블로 사용하였다.
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
                    cur.execute("SELECT no FROM lecture WHERE lecture_code ='" + str(side[0]) +"'")
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

                elif commend == 'courses_create':
                    cur = self.databasent.cursor()
                    print(side)
                    stuid = str(side[0])

                    # 강의 있는지 조회
                    cur.execute("SELECT department FROM user WHERE student_id ='" + str(stuid) + "'")
                    depart = cur.fetchall()
                    depart = depart[0][0]

                    tmp = ' '.join(side[1:])
                    print(tmp)
                    tmp = tmp.split('/')
                    print(tmp)
                    tmp.pop()
                    for t in tmp:
                        course_name = t.split(',')[0]
                        course_code = t.split(',')[1]
                        print(course_name)
                        print(course_code)

                        #강의 있는지 조회
                        cur.execute("SELECT no FROM lecture WHERE lecture_code ='" + str(course_code) + "'")
                        lec_id = cur.fetchall()

                        #있으면
                        if len(lec_id) != 0:
                            print('a')
                            #바로추가
                            query = 'INSERT INTO student_course (student_id,lecture_code,lecture_id) Values (%s,%s,%s)'
                            cur.execute(query, (stuid, str(course_code),str(lec_id[0][0])))
                            self.databasent.commit()

                            # 학생, 강의 정보를 포인트 테이블에 추가
                            query = 'INSERT INTO points (Student_id,Depart,Lec_id,points) Values (%s,%s,%s,%s)'
                            cur.execute(query, (stuid, str(depart), str(course_code), str(0)))
                            self.databasent.commit()


                        #없으면
                        else:
                            print('b')
                            #강의를 디비에 추가
                            query = 'INSERT INTO lecture (lecture_name,lecture_code) Values (%s,%s)'
                            cur.execute(query, (str(course_name), str(course_code)))
                            self.databasent.commit()

                            print('c')
                            #추가한 강의의 lecid를 가져옴
                            cur.execute("SELECT no FROM lecture WHERE lecture_code ='" + str(course_code) + "'")
                            lec_id = cur.fetchall()
                            lec_id = str(lec_id[0][0])

                            query = 'INSERT INTO category (lecture_code,lecture_id,chatroom_name) Values (%s,%s,%s)'
                            cur.execute(query, (str(course_code), lec_id, str('강의')))
                            self.databasent.commit()

                            print('d')
                            print(str(lec_id))
                            #학생 정보에 강의 추가
                            query = 'INSERT INTO student_course (student_id,lecture_code,lecture_id) Values (%s,%s,%s)'
                            cur.execute(query, (stuid, str(course_code), str(lec_id)))
                            self.databasent.commit()

                            # 학생, 강의 정보를 포인트 테이블에 추가
                            query = 'INSERT INTO points (Student_id,Depart,Lec_id,points) Values (%s,%s,%s,%s)'
                            cur.execute(query, (stuid, str(depart),str(course_code), str(0)))
                            self.databasent.commit()


                    print('3333: 추가완료')
                    client.send('complete'.encode('utf-8'))

                elif commend == 'like_update':
                    chat_id = str(side[0])
                    print("side:")
                    print(side)
                    print("<><><><>")
                    cur = self.databasent.cursor()
                    #왜 하는지 모르지만 안전상 유지시킴
                    cur.execute("SELECT no FROM chatting WHERE no = " + str(chat_id) + "")
                    allSQLRows = cur.fetchall()
                    chat_id = allSQLRows[0][0]
                    #포인트 조절용>>>
                    cur.execute("SELECT category_id FROM chatting WHERE no = " + str(chat_id) + "")
                    allSQLRows1 = cur.fetchall()
                    cat_id = allSQLRows1[0][0]
                    cur.execute("SELECT lecture_code FROM category WHERE no = " + str(cat_id) + "")
                    allSQLRows1 = cur.fetchall()
                    lec_id = allSQLRows1[0][0]
                    print(lec_id)
                    #<<<포인트 조절용
                    cur.execute("SELECT likes_num FROM likes WHERE student_id = '"+str(side[1])+"' AND chat_id = " + str(chat_id) + "")
                    allSQLRows = cur.fetchall()
                    print(allSQLRows)
                    if len(allSQLRows)>0:
                        likes_num = allSQLRows[0][0]
                        if likes_num == 0:
                            #좋아요를 할때
                            cur.execute("UPDATE chatting SET likes = likes+1 WHERE no =" + str(chat_id) + "")
                            self.databasent.commit()
                            cur.execute("UPDATE likes SET likes_num = 1 WHERE student_id='"+str(side[1])+"' AND chat_id = " + str(chat_id) + "")
                            self.databasent.commit()
                            #점수 +
                            cur.execute("UPDATE points SET points = points + 1 WHERE Student_id='"+str(side[1])+"' AND Lec_id = '" + str(lec_id) + "'")
                            self.databasent.commit()
                            
                            
                            
                        elif likes_num == 1:
                            #이미 좋아요를 했을때
                            cur.execute("UPDATE chatting SET likes = likes-1  WHERE no = " + str(chat_id) + "")
                            self.databasent.commit()
                            cur.execute("UPDATE likes SET likes_num = 0 WHERE student_id='"+str(side[1])+"' AND chat_id = " + str(chat_id) + "")
                            self.databasent.commit()
                            #점수 -
                            cur.execute("UPDATE points SET points = points - 1 WHERE Student_id='"+str(side[1])+"' AND Lec_id = '" + str(lec_id) + "'")
                            self.databasent.commit()
                    
                    else:
                        #likes가 생성되지 않았을때
                        cur.execute("INSERT INTO likes(chat_id,student_id,likes_num) VALUES ("+str(chat_id)+",'"+str(side[1])+"',1)")
                        self.databasent.commit()
                        cur.execute("UPDATE chatting SET likes = likes+1 WHERE no =" + str(chat_id) + "")
                        self.databasent.commit()
                        #점수+
                        cur.execute("UPDATE points SET points = points + 1 WHERE Student_id='"+str(side[1])+"' AND Lec_id = '" + str(lec_id) + "'")
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
