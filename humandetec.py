import cv2
import numpy as np
# Load YOLOv3 model and configuration
net = cv2.dnn.readNetFromDarknet('openCV/yolov3.cfg','openCV/yolov3.weights')
classes = []
with open('openCV/coco.names', 'r') as f:
    classes = f.read().splitlines()
# Set input video
cap = cv2.VideoCapture('openCV/testfall.mp4')
count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width, _ = frame.shape

    # Create blob from input frame and perform forward pass
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layer_outputs = net.forward(output_layers_names)

    # Process detections
    boxes = []
    confidences = []
    class_ids = []

    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 0:  # class_id 0 represents "person" in COCO dataset
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply non-maximum suppression to remove redundant overlapping boxes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    # Draw boxes and labels on the frame
    #first frame
    r,first_frame = cap.read()
    
    for i in indices:
        box = boxes[0]
        x0,y0,w0,h0 = box
        #cv2.rectangle(first_frame, (x0, y0), (x0 + w0, y0 + h0), (0, 255, 0), 2)
        print('firstbox',x0,y0,w0,h0)
        box_next = boxes[i]
        x, y, w, h = box_next
        print('secondebox',x,y,w,h)
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        #cv2.putText(frame, 'Person', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # สร้าง mask ขนาดเท่ากับ frame และให้ทุกส่วนเป็นสีขาว (255) ในแผ่นขนาดนั้น
        mask1 = np.ones_like(frame) * 255
        mask2 = np.ones_like(frame) * 255

        # ให้พื้นที่นอกกรอบที่ต้องการทำเป็นสีดำ
        mask1[y0:y0+h0, x0:x0+w0] = 0
        mask2[y:y+h, x:x+w] = 0

        # เปลี่ยนสีดำใน mask เป็นสีดำใน frame
        first_frame[np.where((mask2 != [0,0,0]).all(axis=2))] = [0,0,0]
        frame[np.where((mask2 != [0,0,0]).all(axis=2))] = [0,0,0]

        #optical flow

        #convert to gray scale
        prvs = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
        next = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate optical flow using Farneback method
        flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        # Visualize optical flow
        hsv = np.zeros_like(frame)
        hsv[..., 1] = 255

        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])

        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        cv2.imshow('optical flow',rgb)
        cv2.imwrite('openCV/img'+str(count)+'.png',rgb)
        count = count+1
    #display first frame
    #cv2.imshow('first', first_frame)
    # Display the output frame
    #cv2.imshow('second', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
