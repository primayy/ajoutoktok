# ajoutoktok
## 소개
아주똑똑은 강의자와 학습자 사이의 소통을 증진시키기 위해 강의 중 실시간으로 질문을 할 수 있는 데스크탑 채팅 어플리케이션입니다.
기존에 강의자와 학습자들이 강의, 질문, 소통에 대해 느꼈던 문제점과 불편함을 알기 위하여 강의자와 학습자를 대상으로 인터뷰와 설문을 진행했고, 이를 통해 실제 사용자들이 원하는 서비스를 제공하고자 했습니다. 
<h3><br>본 프로젝트 결과물은 아주대학교 계정을 사용해 이용할 수 있습니다.</h3>

## 특징
1. 학습자는 누가 질문했는지 알 수 없으나 강의자는 질문자가 누구인지 알 수 있다.
2. 강의자는 학습자가 질문한 목록을 등록한 이메일 계정으로 전송받을 수 있다.
3. 학습자의 자발적 질문 유도를 위한 Gamification 요소(랭킹) 추가
4. 강의자는 질문 카테고리를 생성해 학습자의 질문을 일차적으로 분류할 수 있다.


## 서비스 화면
### 1. 로그인 화면
![image](https://user-images.githubusercontent.com/37567802/91816537-0013a080-ec70-11ea-8798-9c05ed032d0e.png)
![image](https://user-images.githubusercontent.com/37567802/91818104-6f899000-ec70-11ea-8bf1-69cc015a4561.png)<br>
- 로그인 화면은 간단하게 계정과 비밀번호를 입력하는 부분으로 구성됩니다. 
- 로그인은 BlackBoard의 계정과 연동되어 별도의 회원가입 절차 없이 간편하게 로그인할 수 있습니다.
- BlackBoard로 이동하기를 체크할 경우에는 로그인 된 상태로 BlackBoard 홈페이지를 함께 열 수 있습니다.

### 2. 서비스 메인 화면
![image](https://user-images.githubusercontent.com/37567802/91821675-ab712500-ec71-11ea-9dd5-82ef998c482b.png)
- 강의 목록은 학생이 수강하고 있는 강의들의 채팅방 목록입니다. 
- Black Board의 학생 정보를 크롤링 하여 자동으로 연동합니다. 그렇기 때문에 같은 강의를 수강하는 학생들은 기본적으로 같은
채팅방에 접속하여 질문을 공유하게 됩니다.

### 3. 질문 및 질문 위젯
![image](https://user-images.githubusercontent.com/37567802/91821859-f12ded80-ec71-11ea-86a5-3871b08b757b.png)
![image](https://user-images.githubusercontent.com/37567802/91821788-d6f40f80-ec71-11ea-97bd-7b0f1428b284.png)
![image](https://user-images.githubusercontent.com/37567802/91821914-0571ea80-ec72-11ea-8673-5fb63f63b8bf.png)
-  강의 목록 오른쪽 하단의 말풍선 아이콘을 클릭할 시 채팅방의 새로 온 메시지 개수를 알려주는 알림 팝업을
띄울 수 있습니다. 팝업은 화면의 항상 모든 창 위에 고정되며 더블 클릭 시 해당 강의 채팅방으로 이동할 수 있고 우클릭 시 팝업을 화면에서 제거할 수 있습니다.

### 4. 질문 답변
![image](https://user-images.githubusercontent.com/37567802/91822172-571a7500-ec72-11ea-8870-fd1104c1ec0f.png)
- 질문을 선택하면 본 화면으로 이동 가능합니다.
- 이 화면에서는 질문에 달린 답변들의 목록을 확인하거나 직접 답변을 작성할 수 있습니다. 

### 5. 답변 채택
<img src="https://user-images.githubusercontent.com/37567802/91822428-c1cbb080-ec72-11ea-8925-cb2d8790a38e.png" width="300">
<img src="https://user-images.githubusercontent.com/37567802/91822481-d6a84400-ec72-11ea-8bb9-82b9d22847a7.png" width="300">
<img src="https://user-images.githubusercontent.com/37567802/91822244-6f8a8f80-ec72-11ea-93cc-0591594a4f9d.png">

- 질문에 작성된 답변 중 어떤 답변이 가장 도움이 되는 답변인지 모른다 라는 의견을 통해 답변채택기능을 추가했습니다.
- 채팅 작성자는 답변들 중 가장 우수하거나 도움이 된 답변을 우클릭을 통해 채택할 수 있습니다.

### 6. 알림
![image](https://user-images.githubusercontent.com/37567802/91822363-a9f42c80-ec72-11ea-8929-933899752053.png)

- 사용자의 질문에 댓글이 달리거나 사용자의 댓글이 채택될 경우 이를 알림으로 확인할 수 있습니다. 
- 화살표 버튼을 누르면 해당 댓글의 질문 목록으로 이동합니다.

### 7. 질문 목록 이메일 전송 & 전송 결과
<img src="https://user-images.githubusercontent.com/37567802/91822011-25a1a980-ec72-11ea-983d-d162661c30b0.png" width="300">
<img src="https://user-images.githubusercontent.com/37567802/91822058-33572f00-ec72-11ea-974d-a17dad1d22e1.png">

- 채팅방 우측 상단의 다운로드 아이콘 클릭 시 지정 기간 내의 질문 목록을 접속된 아이디의 아주대학교 Gmail 로 전송할 수 있습니다. 
- 질문 목록은 학번, 날짜, 질문, 공감수가 기록되어 있고 해당 채팅방의 카테고리 별로 분류되어 있습니다.

### 8. 리더보드
![image](https://user-images.githubusercontent.com/37567802/91823935-f0e32180-ec74-11ea-8568-12c713db12f9.png)

- 학습자의 자발적인 참여를 위해 질의응답시 포인트를 부여하는 게임요소를 추가했습니다.
- 리더보드 메뉴에서는 학습자가 얻은 포인트를 바탕으로 학습자들의 순위를 측정합니다.

## 실행 방법
### Client
1. cd client
2. run main.py

### Database
1. cd client
2. db7.sql을 mysql에서 실행하여 필수 테이블 생성
3. run mysql

### Server
1. cd server
2. pip install pymysql
3. server.py의 19라인을 mysql 서버 설정으로 변경
4. mysql database 실행
5. run server.py
