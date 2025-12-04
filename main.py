import cv2 as cv
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

capture = cv.VideoCapture(0)

sum_conf = 0
count = 0
current_avg = 0


while True:
    isTrue, frame = capture.read()

    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    boxes = pytesseract.image_to_data(rgb)

    for i,line in enumerate(boxes.splitlines()):
        if i != 0: # skip header row

            part = line.split()

            if len(part) == 12:

                # update running average confidence
                conf = float(part[10])
                count += 1
                sum_conf += conf
                current_avg = sum_conf / count

                # choose color based on confidence threshold
                color = (82, 168, 50) if (current_avg > 80) else (13,0,161)


                x, y, w, h = int(part[6]), int(part[7]), int(part[8]), int(part[9])
                cv.rectangle(frame, (x - 10, y - 5), (x + w + 10, y + h + 10), color, 3)
                cv.putText(frame, part[11], (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    cv.putText(frame, f'conf = {current_avg}', (40, 40), cv.FONT_HERSHEY_SIMPLEX, 0.9, (207,122,4), 2)

    cv.imshow("video", frame)
    if cv.waitKey(20) & 0xFF == ord('q'):
        break

capture.release()
cv.destroyAllWindows()
cv.waitKey(0)





















