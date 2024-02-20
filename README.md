# 🤖 프로젝트를 더 슬기롭게! 노션 회의 일정 슬랙 봇 프로젝트
## 🌟 소개
<img src="https://github.com/leehjhjhj/nothon-calander-slackbot-project/assets/102458609/5ba340fc-6bd2-4754-9751-f7f7953312d6" width="10%" height="10%"><br>
### 더욱 효율적인 협업을 위해 노션 캘린더와 슬랙을 연동시키는 프로젝트입니다.
**노션 캘린더 데이터베이스 화면**<br>
<img src="https://github.com/leehjhjhj/nothon-calander-slackbot-project/assets/102458609/d9c8eb0e-ce67-417b-87cd-699e9d72cd1b" width="40%" height="40%"><br><br>
**슬랙 메시지 화면**<br>
<img src="https://github.com/leehjhjhj/nothon-calander-slackbot-project/assets/102458609/0a2e5158-8775-49f6-a22a-be47d73452bf" width="40%" height="40%">
- 노션 데이터베이스 API를 통해서, 캘린더에 존재하는 회의를 일정 텀을 두고 불러와 서버 DB에 저장하고, 회의 시작 하루 전, 한 시간 전 슬랙으로 메시지를 전달해줍니다.
- `Celery beat` 를 사용해서 read_notion 함수를 스케줄링하고, worker를 통해서 알림 시간을 스케줄링 합니다.

## 🛠️ 기술 스택
- 사용 스택:
  - Fastapi, Celery, Notion api, Slack sdk
  - Aws ec2, rds, codedeploy, lambda, eventbridge, github actions, nginx, docker

## 🤹‍♂️ 개발 내용 및 경험
https://velog.io/@leehjhjhj/효율적인-프로젝트를-위한-노션-슬랙-봇1-원리와-설계 <br>
https://velog.io/@leehjhjhj/효율적인-프로젝트를-위한-노션-슬랙-봇2-고도화-페이지-자동-생성




