import cv2

# เปิดวิดีโอ
cap = cv2.VideoCapture('openCV/testfall.mp4')
#cap = cv2.VideoCapture(0)

# ตรวจสอบว่าสามารถเปิดวิดีโอได้หรือไม่
if not cap.isOpened():
    print("Error: ไม่สามารถเปิดวิดีโอได้")
    exit()

# กำหนดตัวแปรเพื่อนับเฟรม
frame_count = 0
init_frame = None
fusion1 = None
fusion2 = None


while True:


    # อ่านเฟรมปัจจุบัน
    ret, frame = cap.read()

    # ตรวจสอบว่าอ่านเฟรมได้สำเร็จหรือไม่
    if not ret:
        break
    #reset framecount
    if frame_count == 10:
        frame_count = 0

    # รวมเฟรมทุกๆ 4 เฟรม
    if frame_count % 4 == 0: #initial frame 0
        init_frame = frame

    
    if frame_count % 4 == 1:
        fusion1 = cv2.addWeighted(init_frame, 0.5, frame, 0.5, 0)

    if frame_count % 4 == 2:
        fusion2 = cv2.addWeighted(fusion1, 0.5, frame, 0.5, 0)

    if frame_count % 4 == 3:
        fusion_full = cv2.addWeighted(fusion2, 0.5, fusion1, 0.5, 0)
        #cv2.imwrite(str(frame_count)+'.png', fusion_full)
        cv2.imshow('fusion image',fusion_full)
        print('count '+str(frame_count))
    
    # เพิ่มค่า frame_count ขึ้นทีละ 1
    frame_count += 1
    # หน่วงเวลา
    cv2.waitKey(17)
        

# ปิดวิดีโอ
cap.release()
cv2.destroyAllWindows()
