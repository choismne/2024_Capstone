import cv2
from pyzbar import pyzbar
# import webbrowser

def decode_qr_code(frame):
    # 프레임에서 QR 코드를 인식하고 디코드
    decoded_objects = pyzbar.decode(frame)
    for obj in decoded_objects:
        # QR 코드 데이터가 URL인지 확인하고, 맞다면 웹브라우저를 통해 열기
        if obj.data.startswith(b"http"):
            print(obj.data.decode())
            # webbrowser.open(obj.data.decode())
            return True
    return False


# 카메라 캡처 객체 생성
cap = cv2.VideoCapture(0)

while True:
    # 프레임 별로 캡처
    ret, frame = cap.read()
    if not ret:
        continue

    # QR 코드 인식 시도
    if decode_qr_code(frame):
        break

    # 결과 프레임을 화면에 표시
    cv2.imshow('QR Code Scanner', frame)

    # 'q'를 누르면 루프에서 벗어납니다.
    # 이거해야 ui나옴
    if cv2.waitKey(1) == ord('q'):
        break

# 작업 완료 후 해제
cap.release()
cv2.destroyAllWindows()
