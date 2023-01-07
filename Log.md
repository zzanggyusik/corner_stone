# Cornerstone Chatbot Log


# 2023-01-07 01:46 작성
-         if(self.isAlready == False):
            if(self.chatbot_db.visited_user(self.chatbot_db.con, self.user_id)):
                self.isAlready = True

                ... (feature/JunHyuk의 CornerstoneChatbot.py, line 128 ~ 130)

- 의문 사항
    1. 위 조건의 필요성은?
        * self.isAlready가 True일 때만 sendMessageWithSim() 함수가 제대로 동작하기는 함.
            그리고, self.chatbot_db.visited_user()를 통해 이미 DB에 user_id가 있으면 이미 데이터가 
            있으므로 바로 message를 보낼 수 있게 하는 것 까지는 OK
            But, 만약에 이미 DB에 user_id가 저장된 사용자가 /start를 하지 않고 있게 된다면?
            self.isAlready == False가 맞음.
            하지만, /start를 입력하지 않았기 때문에 self.user_id는 None 일거임
            그렇다면, self.chatbot_db.visited_user() 인자로 넘어가는 self.user_id에서 에러가 발생할 것으로 예상됨
            sendMessageWithSim()은 Cornerstone 객체가 만들어진 후 /start, /option 등과 같이 
            ConversationHandler가 돌아가지 않아도 시뮬에서 호출 할 수 있음,
            /start를 통해 ConversationHandler가 작동해야 self.user_id에 값이 들어가는데,
            아무것도 입력하지 않았을 경우에도 sendMessageWithSim()은 호출될 수 있어서 
            챗봇을 실행하고 가만히 있는 상태면 self.user_id가 없어서 문제가 될것으로 예상


* PEx 클래스 생성자에 bot.chatbot_db.con, bot.post_num등 외부에 선언 된 bot을 사용하는 게 맞는지,
 맞다면 인자로 받아서 하는 게 더 안전할 거 같은데 어떻게 생각하는지

* DB 파일이 message_db와 userID_db가 합쳐진게 Corner_db 인지,
  맞다면 Line 48, 80에 bot.chatbot_db.message_con은 무엇을 의미하는지(message_con 변수를 생성하는 거?)
  왜 생성자에서는 chatbot_db.con을 쓰는데 위는 message_con을 쓰는지,

* 