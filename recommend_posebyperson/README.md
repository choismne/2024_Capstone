# recommend_posebyperson.py 함수 코드 설명

### GET /recommend/posebyperson/{number}

해당 함수는 사진에 검출된 인원수 별로 사용자에게 사진을 제공해주는 엔드포인트입니다.

API Gateway의 Path Parameter를 활용하여 구현하였습니다.

DynamoDB에 저장된 항목들을 스캔하여, Path Parameter로 받은 값에 맞는 이미지들을 사용자에게 반환합니다.

클라이언트에서 HTTP header에 JWT토큰을 담아서 요청을 보내면, 이를 검증하고 로직을 수행하는 함수입니다.
