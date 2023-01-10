# Cornerstone Chatbot Log

# 2023-01-10 작성
 * 의문점
    1. ChatbotDB의 con은 왜 생성자에서 connection을 호출하지 않는가?
        - 현재는 PEx 클래스 생성자에서 ChatbotDB 객체 생성 후 connection()을 호출하는 데 의도가 무엇인지

    2. create_insert_table()은 왜 Simulation에서 호출 되는가? 이것 역시 ChatbotDB의 생성자에서 하는 게 옳지 않은가?

    3. PEx 클래스의 self.db_langs와 같은 DB table을 생성하기 위한 리스트는 왜 PEx 클래스의 멤버 변수인가?
        - DB의 table을 생성하기 위한 데이터이므로 ChatbotDB의 멤버 변수로 선언하면 create_insert_table()을 호출할 때
          매개변수로 사용하지 않아도 되는데, 왜 굳이 PEx 클래스의 멤버 변수로 사용한 의도가 무엇인지

    4. CornerstoneChatbot(이하 Chatbot) 클래스의 멤버 면수 post_num 역시 DB와 더 관련 깊은 변수인데, 왜 Chatbot 클래스
       멤버 변수로 선언했는가?

 * 문제점
    1. PEx, Chatbot, ChatbotDB 클래스 사이에 연관 관계가 필요 이상으로 복잡하게 설계되어 있음
        - Chatbot 클래스 내부에서 멤버 변수로 ChatbotDB 객체를 생성하고 있음에도 PEx 객체에서도 생성하고 있음
        - DB와 관련 깊은 데이터(변수)들이 PEx의 멤버 변수로 선언되어 있음

 * 해결 방안
    1. PEx 클래스는 Chatbot 객체만 생성하고, DB와 데이터 전달이 필요할 경우, Chatbot 객체의 멤버 변수로 선언된
       ChatbotDB 객체를 참조해서 사용하는 방식으로 변경

 * 추가적으로..
    1. Chatbot의 멤버 변수 self.user_id, self.language, self.location을 DB의 멤버 변수로 변경
        - 위 세 개의 멤벼 변수 모두 DB와 깊은 연관이 있는 변수이므로 DB에 있는 게 맞다고 판단 됨
        - self.chatbot_db.user_id와 같은 방식으로 접근하도록 하여, DB의 함수 호출 시 인자 전달을 생략하도록 함