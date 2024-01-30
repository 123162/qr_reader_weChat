import cv2
import sys
import time

def displayBbox(im, bbox):
    if bbox is not None:
        bbox = [bbox[0].astype(int)]
        n = len(bbox[0])
        for i in range(n):
            cv2.line(im, tuple(bbox[0][i]), tuple(bbox[0][(i+1) % n]), (0,255,0), 3)
            

detector=cv2.wechat_qrcode_WeChatQRCode("detect.prototxt",
                                        "detect.caffemodel",
                                        "sr.prototxt",
                                        "sr.caffemodel")        

if __name__ == '__main__':
    # Initialize video capture from the default camera (index 0).
    cap = cv2.VideoCapture("b.mp4")
    new_width = 650
    new_height = 800
    while True:
        ret, frame = cap.read()#frame:okunan kare,ret:karenin başarı ile okunup okunmadığını temsil eder
        resized_frame = cv2.resize(frame, (new_width, new_height))
        corrected_frame = cv2.flip(resized_frame, flipCode=0)
        if not ret:
            print("Failed bro!!!")#kare okunmazsa
            break

        t1 = time.time()
        # Detect and decode.
        res, points = detector.detectAndDecode(corrected_frame)
        t2 = time.time()

        # Detected outputs.
        if len(res) > 0:
            print('Time Taken : ', round(1000*(t2 - t1), 1), ' ms')
            print('Output : ', res[0])
            displayBbox(corrected_frame, points)
        else:
            print('QRCode not detected')

        # Display the resulting frame
        cv2.imshow("Frame", corrected_frame)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()