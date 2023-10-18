# 🤖 프로젝트를 더 슬기롭게! 노션 회의 일정 슬랙 봇 프로젝트
## 🌟 소개
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
  - Aws ec2, rds, codedeploy, github actions, nginx, docker

## 개발 내용 및 경험
### Celery를 이용한 스케줄링
celery beat와 worker를 사용하여 주기적으로 데이터베이스를 읽고, celery task 함수의 `appy_async`의 `eta`인자를 활용해서 알림 시간을 스케줄링 하였습니다.
### 책임 분리
최대한 function을 분리해서 코드가 너무 길어지지 않도록 노력했고, service, persistance, celery beat, worker을 분리해서 각 영억의 책임만 지도록 개발하였습니다.
### 효율적인 개발을 위한 CICD 구축
서비스를 위해 한번에 띄어야 될 컨테이너 수가 많은 만큼, docker compose를 사용하였으며, 쉬운 배포를 위해서 github acition을 이용한 CI를 구축하였습니다. CD에서 기존에 appleboy를 이용한 ssh를 이용한 ec2 인스턴스에 접속하는 방식이 아닌, Codedeploy를 사용해서 안정적인 배포가 이루어지도록 하였습니다.
### 성장경험
프로젝트 팀장을 맡으면서 '어떻게 하면 효율적으로 팀을 이끌어 나갈 수 있을까?' 를 고민하고 있었습니다. 여러번 프로젝트를 경험하면서, 소통에 있어서 '회의'를 효과적으로 이끌어 내는 것이 중요하다고 느꼈습니다. 하지만 일정을 빈번하게 잊어버리는 일도 잦고, 그렇게 되면 회의 주제나 미리 준비해야 하는 부분들을 팀원들이 놓치기 쉽상이었습니다. 따라서 원할한 프로젝트 진행을 위해서, 모든 알림은 slack에 집중시키고, 회의 알림을 slack 메시지로 보내서 팀원들로 하여금 프로젝트에 쉽게 집중할 수 있는 환경을 만들어주려고 노력하고 있습니다.





