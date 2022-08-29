import cv2
import sys
import numpy as np

cap1 = cv2.VideoCapture('128863.mp4')
cap2 = cv2.VideoCapture('129011.mp4')

if not cap1.isOpened() or not cap2.isOpened():
    print('x')
    sys.exit()

# 각 영상 프레임 수
frames_cnt1 = round(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
frames_cnt2 = round(cap2.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap1.get(cv2.CAP_PROP_FPS)
effect_frames = int(fps * 2)

delay = int(1000 / fps)

# 영상 가로 세로 설정
w = round(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 비디오 코덱 설정
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output.avi', fourcc, fps, (w, h))

# 1번 영상 열기
for i in range(frames_cnt1 - effect_frames):
    ret1, frame1 = cap1.read()

    if not ret1:
        break

    out.write(frame1)
    cv2.imshow('frame', frame1)
    cv2.waitKey(delay)

# 합성하기
for i in range(effect_frames):
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        print('frame read error!')
        sys.exit()

    # 합성, 짤라내기 위한 변수, w 넓이를 48로 나눔
    dx = int((w / effect_frames) * i)

    # 프레임을 하나 생성
    frame = np.zeros((h, w, 3), dtype=np.uint8)
    frame[:, 0:dx, :] = frame2[:, 0:dx, :]  # 0부터 dx까지는 영상2
    frame[:, dx:w-2] = frame1[:, dx:w-2]  # dx부터 끝까지는 영상1

    # 프레임 저장
    out.write(frame)
    print('.', end='')

    cv2.imshow('output', frame)  # 영상 출력
    cv2.waitKey(delay)

# 2번 동영상 저장
for i in range(effect_frames, frames_cnt2):
    ret2, frame2 = cap2.read()

    if not ret2:
        print('video read error!')
        sys.exit()

    out.write(frame2)
    print('.', end='')

    cv2.imshow('output', frame2)
    cv2.waitKey(delay)

# 프레임을 받아온 후 꼭 release를 써야 한다. 사용한 자원 해제
cap1.release()
cap2.release()
out.release()
cv2.destroyAllWindows()