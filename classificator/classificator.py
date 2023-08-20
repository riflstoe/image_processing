import cv2
import time
from multiprocessing import Process, Queue
from skimage.metrics import structural_similarity as compare_ssim


# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("original")
#     parser.add_argument("modified")
#     return parser.parse_args()
#
#
# imageA = cv2.imread("/home/rapa/test/colored/s1_01_thumbnail.jpg")
# imageB = cv2.imread("/home/rapa/test/colored/s1_02_thumbnail.jpg")
# grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
# grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
# score, diff = compare_ssim(grayA, grayB, full=True)
#
# diff = (diff * 255).astype('uint8')
# print(f'SSIM: {score:.6f}')
# print(diff)

# vid = "/home/rapa/test/ASC_StEM2_178_2K_24_100nits_Rec709_Stereo.mp4"
# convert = ffmpeg.input(vid)
# convert = convert.filter('scale', w=192, h=108)
# convert2 = ffmpeg.output(convert, "/home/rapa/test/test.mp4")
# ffmpeg.run(convert2)

def video_process(total_threads, thread_num, result_frm):
    cap = cv2.VideoCapture("D:\\4_School_Works\\playon.mp4")
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    division = length / total_threads
    start_num = division * (thread_num - 1) + 1
    end_num = division * thread_num
    current_frame = 0
    stack = 0
    cut = 1
    old_frame = None
    total_frames = []
    current_frame += start_num - 1
    cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width * 0.1)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height * 0.1)
    while True:
        ret, frame = cap.read()
        if ret is True:
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            if old_frame is not None:
                score, _ = compare_ssim(old_frame, gray, full=True)
                ssim = score * 100
                if ssim < 50:
                    stack += 1
                    temp = ssim
                else:
                    if stack == 1:
                        frm = f'cut : {cut}, frame : {current_frame - 1}, SSIM: {temp:.1f}%'
                        print(frm)
                        total_frames.append(frm)
                        stack = 0
                        cut += 1
                if stack == 2:
                    stack = 0
                # print(f'frame : {current_frame}, SSIM: {ssim:.1f}%')
                # cv2.imshow('diff_frame', gray)
            old_frame = gray
            current_frame += 1
            if current_frame == end_num:
                break
        else:
            print('ERROR!')
            break
    cap.release()
    cv2.destroyAllWindows()
    result_frm.put(total_frames)
    return


if __name__ == "__main__":
    start_time = time.time()
    result = Queue()
    th1 = Process(target=video_process, args=(30, 1, result))
    th2 = Process(target=video_process, args=(30, 2, result))
    th3 = Process(target=video_process, args=(30, 3, result))
    th4 = Process(target=video_process, args=(30, 4, result))
    th5 = Process(target=video_process, args=(30, 5, result))
    th6 = Process(target=video_process, args=(30, 6, result))
    th7 = Process(target=video_process, args=(30, 7, result))
    th8 = Process(target=video_process, args=(30, 8, result))
    th9 = Process(target=video_process, args=(30, 9, result))
    th10 = Process(target=video_process, args=(30, 10, result))
    th11 = Process(target=video_process, args=(30, 11, result))
    th12 = Process(target=video_process, args=(30, 12, result))
    th13 = Process(target=video_process, args=(30, 13, result))
    th14 = Process(target=video_process, args=(30, 14, result))
    th15 = Process(target=video_process, args=(30, 15, result))
    th16 = Process(target=video_process, args=(30, 16, result))
    th17 = Process(target=video_process, args=(30, 17, result))
    th18 = Process(target=video_process, args=(30, 18, result))
    th19 = Process(target=video_process, args=(30, 19, result))
    th20 = Process(target=video_process, args=(30, 20, result))
    th21 = Process(target=video_process, args=(30, 21, result))
    th22 = Process(target=video_process, args=(30, 22, result))
    th23 = Process(target=video_process, args=(30, 23, result))
    th24 = Process(target=video_process, args=(30, 24, result))
    th25 = Process(target=video_process, args=(30, 25, result))
    th26 = Process(target=video_process, args=(30, 26, result))
    th27 = Process(target=video_process, args=(30, 27, result))
    th28 = Process(target=video_process, args=(30, 28, result))
    th29 = Process(target=video_process, args=(30, 29, result))
    th30 = Process(target=video_process, args=(30, 30, result))

    th1.start()
    th2.start()
    th3.start()
    th4.start()
    th5.start()
    th6.start()
    th7.start()
    th8.start()
    th9.start()
    th10.start()
    th11.start()
    th12.start()
    th13.start()
    th14.start()
    th15.start()
    th16.start()
    th17.start()
    th18.start()
    th19.start()
    th20.start()
    th21.start()
    th22.start()
    th23.start()
    th24.start()
    th25.start()
    th26.start()
    th27.start()
    th28.start()
    th29.start()
    th30.start()

    th1.join()
    th2.join()
    th3.join()
    th4.join()
    th5.join()
    th6.join()
    th7.join()
    th8.join()
    th9.join()
    th10.join()
    th11.join()
    th12.join()
    th13.join()
    th14.join()
    th15.join()
    th16.join()
    th17.join()
    th18.join()
    th19.join()
    th20.join()
    th21.join()
    th22.join()
    th23.join()
    th24.join()
    th25.join()
    th26.join()
    th27.join()
    th28.join()
    th29.join()
    th30.join()

    result.put('STOP')
    total = []
    while True:
        tmp = result.get()
        if tmp == 'STOP':
            break
        else:
            total.append(tmp)
    print(f"Result: {total}")
    print("--- %s seconds ---" % (time.time() - start_time))
