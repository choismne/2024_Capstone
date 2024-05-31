# reading_dynamodb_stream.py Lambda함수 코드 설명

사용자가 QR코드 촬영을 통해 네컷사진을 앱에 업로드하면, 일련의 과정을 거치고 DynamoDB에 해당 사진의 메타데이터가 적재되게 됩니다.

이때 새로운 DynamoDB 새로운 항목이 생성되면, DynamoDB Stream을 활용하여 해당 이벤트를 트리거로 Lambda 함수가 실행되어 처리 과정을 거치고, RDS의 통계 테이블의 값을 업데이트 합니다.

allowed_moods_columns, allowed_poses_columns라는 딕셔너리를 작성하여 DynamoDB stream 이벤트로부터 추출된 값들을 검증하는 절차를 거친 후 쿼리 문자열에 포함시킬 수 있도록 구현하였습니다.

RDS와 해당 Lambda함수를 동일한 VPC에 배치시켜 사용하면, Lambda함수에서 VPC밖에있는 DynamoDB를 사용할 수 없는 Issue가 있었습니다. 이를 해결하기 위해 VPC Endpoint를 생성하여 DynamoDB에 접근할 수 있도록 구현하였습니다.
