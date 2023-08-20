import ffmpeg
import os
import subprocess
import cv2


class Framebreaker:
    def __init__(self):
        self._path = None
        self.iframes = None
        self.bframes = None
        self.pframes = None

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, video_path=None):
        if video_path:
            self._path = video_path

    def iframes(self):
        command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1'.split()
        out = subprocess.check_output(command + [self.path]).decode()
        f_types = out.replace('pict_type=', '').split()
        frame_types = zip(range(len(f_types)), f_types)
        i_frames = [x[0] for x in frame_types if x[1] == 'I']
        if i_frames:
            cap = cv2.VideoCapture(self.path)
            for frame_no in i_frames:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
                ret, frame = cap.read()
                outname = self.path + 'i_frame_' + str(frame_no) + '.jpg'
                cv2.imwrite(outname, frame)
            cap.release()
            print("I-Frame selection Done!!")

    def get_ipb_frmaes(self):
        pass

    def make_video_dict(self):
        pass

    def rgb_to_ycbcr(self):
        pass

    def compare_frames(self, previous_frame, current_frame):
        pass

    def make_cut_image(self):
        pass

    def save_image(self):
        pass

    def get_video(self):
        pass

    def logic(self):
        pass

    def get_ipb_frames_2(self):
        video = ffmpeg.probe(self.path)
        time = float(video['streams'][0]['duration']) // 2
        width = video['streams'][0]['width']
        parts = 7

        intervals = time // parts
        intervals = int(intervals)
        interval_list = [(i * intervals, (i + 1) * intervals) for i in range(parts)]
        i = 0

        for item in interval_list:
            (
                ffmpeg
                .input(self.path, ss=item[1])
                .filter('scale', width, -1)
                .output('Image' + str(i) + 'jpg', vframes=1)
                .run()
            )
            i += 1

    # def get_frame_types(self, video_fn):
    #     command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1'.split()
    #     out = subprocess.(command + [video_fn]).decode()
    #     frame_types = out.replace('pict_type=', '').split()
    #     return zip(range(len(frame_types)), frame_types)

    def save_i_keyframes(self, video_fn):
        frame_types = self.get_frame_types(video_fn)
        i_frames = [x[0] for x in frame_types if x[1] == 'I']
        if i_frames:
            basename = os.path.splitext(os.path.basename(video_fn))[0]
            cap = cv2.VideoCapture(video_fn)
            for frame_no in i_frames:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
                ret, frame = cap.read()
                outname = basename + '_i_frame_' + str(frame_no) + '.jpg'
                cv2.imwrite(outname, frame)
                print('Saved: ' + outname)
            cap.release()
        else:
            print('No I-frames in ' + video_fn)


def main():
    f = Framebreaker()
    f.path = 'D:\4_School_Works\playon.mp4'
    f.iframes()

if __name__ == '__main__':
    main()
