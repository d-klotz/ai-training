import cv2
# tracker = cv2.TrackerKCF.create()
# tracker = cv2.TrackerCSRT.create()
tracker = cv2.TrackerMIL.create()

video = cv2.VideoCapture('data/video.mp4')

ok, frame = video.read()

bbox = cv2.selectROI(frame)

ok = tracker.init(frame, bbox)

while True:
    ok, frame = video.read()
    if not ok:
        break

    ok, bbox = tracker.update(frame)
    print(bbox)

    if ok:
        (x, y, w, h) = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2, 1)

    else:
        cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow('Tracking', frame)
    if cv2.waitKey(1) & 0xFF == 27: #esc key
        break

