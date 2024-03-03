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
fusion1 = None
fusion2 = None

while True:
    # อ่านเฟรมปัจจุบัน
    ret, frame = cap.read()

    # ตรวจสอบว่าอ่านเฟรมได้สำเร็จหรือไม่
    if not ret:
        break

    # รวมเฟรมทุกๆ 4 เฟรม
    if frame_count % 4 == 0: #initial frame 0
        current_frame = frame
        print('init '+str(frame_count))

    elif frame_count <= 10:

        if frame_count % 4 < 2: #mod 1 & 2
            fusion1 = cv2.add(current_frame,frame)
            current_frame = fusion1
            print(f"fusion1 {frame_count}")
            print('end1')

        elif frame_count % 4 >= 2: #mod 2 & 3
            fusion2 = cv2.add(fusion1,frame)
            print(f"fusion2 {frame_count}")

            # แสดงเฟรมที่รวมกัน
            cv2.imwrite(str(frame_count)+'.png', fusion2)
            cv2.imshow('fusion',fusion2)
            cv2.waitKey(1)
            print('end2')
    # เพิ่มค่า frame_count ขึ้นทีละ 1
    frame_count += 1
    #reset



# ปิดวิดีโอ
cap.release()
cv2.destroyAllWindows()
