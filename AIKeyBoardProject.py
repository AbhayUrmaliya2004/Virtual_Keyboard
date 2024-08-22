import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# length and breadth setup
cap.set(3, 1280)
cap.set(4, 640)

detector = HandDetector(detectionCon=0.8)

# drawing keyboard on the image

def draw_keyboard(img, buttonList):
    
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        # Draw a custom filled rectangle and text on the frame
        cv2.rectangle(img, button.pos, (x+h, y+w), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x+15, y+60),
                     cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
        
    return img

# Creating Button Class 

class Button:
    def __init__(self, pos, text, size=(85, 85)):
        self.pos = pos 
        self.text = text 
        self.size= size


buttonList = []
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

# Add buttons to list 
for i in range(len(keys)):
    for j,key in enumerate(keys[i]):
        buttonList.append(Button([100*j+50, 100*i+50], key))

finalText = ""

while True :
    succes, img = cap.read()
    # Find hands and get their landmarks and bounding box info
    hands, img = detector.findHands(img, flipType=False, draw=False)
    
    img = draw_keyboard(img, buttonList)

    # Check if any hands are detected
    if hands:
        for hand in hands:
            lmList = hand['lmList']  # List of 21 landmark points
            bbox = hand['bbox']  # Bounding box info x, y, w, h
            
            for button in buttonList:
                x, y = button.pos
                w, h = button.size
    
                if x < lmList[8][0] < x+w and y < lmList[8][1] < y+h :
                    # Draw a custom filled rectangle and text on the frame
                    cv2.rectangle(img, button.pos, (x+h, y+w), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x+15, y+60),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    
                    # find dis to see the features
                    if len(lmList) > 12:
                        p1 = (lmList[8][0],lmList[8][1])
                        p2 = (lmList[12][0],lmList[12][1])

                        distance, _, _ = detector.findDistance(p1, p2, img, color=(255, 0, 0))
                        print(f"Distance: {distance}")
                    
                    if distance < 35 :
                        # Draw a custom filled rectangle and text on the frame
                        cv2.rectangle(img, button.pos, (x+h, y+w), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x+15, y+60),
                        cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4) 

                        if button.text == '/': # backspace button
                            finalText = finalText[:-1]
                        else :
                            finalText += button.text

                        sleep(0.5)
                
    # Draw a custom filled rectangle and text on the frame
    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 425),
    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    cv2.imshow("Image", img)
    
    cv2.waitKey(1)