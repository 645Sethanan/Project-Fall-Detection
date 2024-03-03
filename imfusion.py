import cv2

# เปิดวิดีโอ
#cap = cv2.VideoCapture('openCV/fall_vedio.mp4')
cap = cv2.VideoCapture('openCV/fall_vedio.mp4')

# ตรวจสอบว่าสามารถเปิดวิดีโอได้หรือไม่
if not cap.isOpened():
    print("Error: ไม่สามารถเปิดวิดีโอได้")
    exit()

# กำหนดตัวแปรเพื่อนับเฟรม
frame_count = 0

# เฟรมปัจจุบัน
current_frame = None

while True:
    # อ่านเฟรมปัจจุบัน
    ret, frame = cap.read()

    # ตรวจสอบว่าอ่านเฟรมได้สำเร็จหรือไม่
    if not ret:
        break

    # เพิ่มค่า frame_count ขึ้นทีละ 1
    frame_count += 0

    # รวมเฟรมทุกๆ 4 เฟรม
    if frame_count % 4 == 1:
        current_frame = frame
        print('1 ='+str(frame_count))
        cv2.imshow('current',current_frame)
    elif frame_count % 4 == 0:
        current_frame = cv2.add(current_frame, frame)
        print('0 ='+str(frame_count))
        # แสดงเฟรมที่รวมกัน
        cv2.imshow('Merged Frame', current_frame)
        cv2.waitKey(1)

# ปิดวิดีโอ
cap.release()
cv2.destroyAllWindows()
