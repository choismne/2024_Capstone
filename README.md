# 🧀 Choose Cheese

**2024-1학기 Capstone Design 에서 진행한 프로젝트입니다.** 

**ChooseCheese는 사용자의 네컷사진 관리 및 포즈 분석/추천, 미소기부 서비스 입니다. 기존 네컷사진 관리의 어려움을 개선하고자 하는 아이디어에서 시작되었습니다.**  

- 기존 네컷 사진 관리의 어려움을 해결하기 위해, 네컷 사진에 포함된 QR 코드를 촬영하는 것만으로 사진을 저장하고 관리할 수 있도록 단순화하였습니다. 또한, 사진에 등장한 얼굴을 통해 사진을 클러스터링하는 기능으로 사용성을 개선하였습니다.
- 사용자가 업로드한 네컷 사진의 포즈와 분위기를 분석하여, 사용자가 경험해보지 못한 새로운 사진 포즈와 분위기를 추천하는 기능을 제공합니다.
- 네컷 사진에 등장한 인물의 미소 점수를 측정하여, 미소 점수에 따른 기부를 진행하는 기능도 포함하고 있어,사용자 참여를 높이고 사회적 기여를 장려합니다.


## 📚 담당 분야
- 백엔드, AWS
  
## 🛠️ 사용 기술 및 라이브러리

- Python, MySQL, Docker
- FastAPI, SQLAlchemy, python-jose[cryptography]
- AWS(EC2, RDS, API Gateway, Lambda, DynamoDB), boto3, PyMySQL

## 👨‍💻 전체 프로젝트 아키텍처
<img width="1565" alt="image" src="https://github.com/choismne/2024_Capstone/assets/97864850/3cdda1e9-7fe3-4fb9-95d5-361310e49bdc">

**본 리포지토리에서는 백엔드 파트 코드만 포함하고 있습니다. (녹색 점선 안쪽 부분)** 



