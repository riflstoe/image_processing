"""**Thumbnail Maker**

This module makes a thumbnail from a video, or makes thumnails for each video in directory.
Users can designate the size of the image to be written and which frame to be written.
These can also be set using a template.

Example:
    test = Thumbnailer() \n
    Users can choose whether to use presets or custom values.
    If the user does not enter a value, thumbnails are created with default settings. \n
    The default setting for size is the video's original size. \n
    The default setting for frame is the video's first frame. \n
    custom values example:
        test.size = 1280, 720 \n
        test.frame = 30 \n
        or test.frame_float = 0.2 \n
    presets example:
        test.size_preset = 'quarter' \n
        test.frame_preset = 'two_third'
    Both Path must be set.\n
    path example:
        test.path = '/input/the/path/to/video.mov' \n
        or test.path = '/input/the/path/that/have/videos' \n
        test.output = '/input/the/path/to/write/thumbnails'\n
    test.execute()\n
    Output image will be like:
        '/input/the/path/to/write/thumbnails/videoname_thumbnail_{frame}.jpg'
"""
import os
import cv2
from math import floor


class Thumbnailer:
    """This class declares an auto-thumbnail-generating operation.
    When the class is called, the default size and frame are set.

    Attributes:
        _size: Exact size of thumbnail to write.
        _frame: Exact frame to write thumbnail image
        _size_preset: Preset to Set the size of thumbnail
        _frame_preset: Preset to write thumbnail image.
        _frame_float: Position of the frame to write the thumbnail as a float number
        _path: Local path to video file or a directory
        _output: Local path to write output image(thumbnail)
        is_path_dir: Check whether _path leads to file or directory
        size_change: Check whether image resize is needed
        inside_vids: List of files under _path if _path leads to directory
    """
    _size = 1
    _frame = 1
    _size_preset = None
    _frame_preset = None
    _frame_float = None
    _path = None
    _output = None

    def __init__(self):
        """
        Attributes are created automatically when declaring a class.
        """
        self.is_path_dir = False
        self.size_change = False
        self.inside_vids = []

    @property
    def path(self):
        """Set the path to a video or a directory. \n
        path(str): Local path of a video file, or a directory that contains several videos.

        Returns:
            self.path

        Raises:
            ValueError: If path is not an existing video file path, or a directory that contains video.
        """
        return self._path

    @path.setter
    def path(self, path):
        """Set the path to a video or a directory. \n

        Args:
            path(str): Local path of a video file, or a directory that contains several videos.

        Returns:
            Set path of video or directory for cv2.VideoCapture.

        Raises:
            ValueError: If path is not an existing video file path, or a directory that contains video.
        """
        self._path = path
        if os.path.isdir(path):
            self.is_path_dir = True
            temp_list = os.listdir(path)
            self.check_dir_files(temp_list)
            return
        if os.path.isfile(path):
            return
        self.error(1)

    def check_dir_files(self, temp_list):
        """Find files in entered directory and make a list of those files. \n
        temp_list(list): Entering a directory in path setter automatically creates a list of subfiles.

        Args:
            temp_list(list): Entering a directory in path setter automatically creates a list of subfiles.

        Returns:
            self.inside_vid contains every local path for each files in temp_list.

        Raises:
            ValueError: If there are no files in directory.
        """
        for files in temp_list:
            full_path = os.path.join(self.path, files)
            if os.path.isfile(full_path) is True:
                self.inside_vids.append(full_path)
            else:
                pass
        if not self.inside_vids:
            self.error(2)

    @property
    def output(self):
        """Set the path for writing images. \n
        outdir(str): Local path to write thumbnail images.

        Returns:
            self.output

        Raises:
            ValueError: If path does not exist.
        """
        return self._output

    @output.setter
    def output(self, outdir):
        """Set the path for writing images.

        Args:
            outdir(str): Local path to write thumbnail images.

        Returns:
            Set path for imwrite.

        Raises:
            ValueError: If path does not exist.
        """
        if not os.path.exists(outdir):
            self.error(3)
            return
        if os.path.isdir(outdir):
            self._output = outdir
            return
        self.error(3)

    @property
    def frame(self):
        """Set the frame to write thumbnail image. \n
        frame_num(int): Exact frame to write. If the input value is negative, It is caclulated from the last frame.

        Returns:
            self.frame

        Raises:
            ValueError: If input number is not integer.
        """
        return self._frame

    @frame.setter
    def frame(self, frame_num):
        """Set the frame to write thumbnail image.

        Args:
            frame_num(int): Exact frame to write. If the input value is negative, It is caclulated from the last frame.

        Returns:
            Set the exact frame to write.

        Raises:
            ValueError: If input number is not integer.
        """
        if type(frame_num) is int:
            self._frame = frame_num
            return
        self.error(4)

    @property
    def frame_preset(self):
        """Set the frame to write thumbnail image with preset. \n
        If 'first', thumbnail is first frame of the video. \n
        If 'last', thumbnail is last frame of the video. \n
        If 'middle', thumbnail is half frame of full frame of the video. \n
        If 'one_third', thumbnail is one third frame of full frame of the video. \n
        If 'two_third', thumbnail is two third frame of full frame of the video.

        Returns:
            self.frame_preset

        Raises:
            ValueError: If input string does not match with any preset.
        """
        return self._frame_preset

    @frame_preset.setter
    def frame_preset(self, preset):
        """Set the frame to write thumbnail image with preset.

        Args:
            preset(str): If 'first', thumbnail is written with first frame of the video.\n
                If 'last', thumbnail is written with last frame of the video. \n
                If 'middle', thumbnail is written with half of full frame of the video. \n
                If 'one_third', thumbnail is written with one third of full frame of the video. \n
                If 'two_third', thumbnail is written with two third of full frame of the video.

        Returns:
            self.frame_preset

        Raises:
            ValueError: If input string does not match with any preset.
        """
        if type(preset) is not str:
            self.error(5)
            return
        if preset in ['first', 'last', 'middle', 'one_third', 'two_third']:
            self._frame_preset = preset
            return
        self.error(5)

    @property
    def frame_float(self):
        """Set the position of the frame to write the thumbnail as a float number. \n
        floatnum(float): Any number between 0 and 1 is accepted. It is converted to a percentage and used.
                0.1 corresponds to 10% position in the video.

        Returns:
            self.frame_float

        Raises:
            ValueError: If input number is not between 0 and 1
        """
        return self._frame_float

    @frame_float.setter
    def frame_float(self, floatnum):
        """Set the position of the frame to write the thumbnail as a float number.

        Args:
            floatnum(float): Any number between 0 and 1 is accepted. It is converted to a percentage and used.
                0.1 corresponds to 10% position in the video.

        Returns:
            self.frame_float

        Raises:
            ValueError: If input number is not between 0 and 1
        """
        if type(floatnum) is float and 0 < floatnum < 1:
            self._frame_float = floatnum
            return
        self.error(6)

    @property
    def size(self):
        """Set exact size of thumbnail to write. \n
        If only one of the horizontal and vertical input is entered,
        the other value will be calculated from resolution of the video. \n
        res(tuple): Input must look like (horizontal value, vertical value).
            If one value is 0, that value will be calculated from resolution of the video according to the other value.

        Returns:
            self.size

        Raises:
            ValueError: If there are not two inputs.
        """
        return self._size

    @size.setter
    def size(self, res):
        """Set exact size of thumbnail to write. \n
        If only one of the horizontal and vertical input is entered,
        the other value will be calculated from resolution of the video.

        Args:
            res(tuple): Input must look like (horizontal value, vertical value). If one value is 0,
                that value will be calculated from resolution of the video according to the other value.

        Returns:
            self.size

        Raises:
            ValueError: If there are not two inputs.
        """
        if type(res) is not tuple:
            self.error(7)
            return
        if len(res) != 2:
            self.error(7)
            return
        hor = res[1]
        ver = res[0]
        if type(hor) is not int or type(ver) is not int:
            self.error(7)
            return
        if hor == 0:
            self._size = ['ver', ver]
            return
        if ver == 0:
            self._size = ['hor', hor]
            return
        self._size = res

    @property
    def size_preset(self):
        """Set the size of thumbnail to write with preset. \n
        If "full", thumbnail is written as full scale of the video. \n
        If "half", thumbnail is written as half scale of the video.  \n
        If "quarter", thumbnail is written as quarter scale of the video. \n
        preset(str): Only "full", "half", "quarter" can be used.

        Returns:
            self.size_preset

        Raises:
            ValueError: If input string does not match with any preset.
        """
        return self._size_preset

    @size_preset.setter
    def size_preset(self, preset):
        """Set the size of thumbnail to write with preset.  \n
        If "full", thumbnail is written as full scale of the video. \n
        If "half", thumbnail is written as half scale of the video.  \n
        If "quarter", thumbnail is written as quarter scale of the video.

        Args:
            preset(str): Only "full", "half", "quarter" can be used.

        Returns:
            self.size_preset

        Raises:
            ValueError: If input string does not match with any preset.
        """
        if type(preset) is not str:
            self.error(8)
            return
        if preset in ['full', 'half', 'quarter']:
            self._size_preset = preset
            return
        self.error(8)

    def frame_size(self):
        """Make a tuple for resize. \n
        If First two arguments are both 0, the resolution will be resized by selected preset. \n
        If there are only two arguments in tuple, self.size_calculate will be executed before resize method. \n
        If there isn't any return, the resize method won't be executed.

        Returns:
            Tuple for cv2.resize
            (absolute horizontal value, absolute vertical value, relative horizontal value, relative vertical value)
        """
        if self.size_preset == 'full' or self.size == 1:
            return 0, 0, 1, 1
        self.size_change = True
        if self.size_preset == 'half':
            return 0, 0, 0.5, 0.5
        if self.size_preset == 'quarter':
            return 0, 0, 0.25, 0.25
        hor_val = self.size[0]
        ver_val = self.size[1]
        if type(hor_val) is str:
            return hor_val, ver_val
        return hor_val, ver_val, 1, 1

    @staticmethod
    def size_calculate(video, frame):
        """This method is executed when one of the value in size is 0. \n
        The other value will be calculated from resolution of the video.

        Args:
            video: Arguments that put the path into cv2.VideoCapture
            frame(tuple): The first value determines the second value is horizontal or vertical.
                Second value is fixed value. The remaining value is determined according to the resolution ratio.

        Returns:
            Tuple for cv2.resize. First two arguments will be the resolution of thumbnail.
        """
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        resolution = width / height
        if frame[0] == 'hor':
            return round(frame[1] * resolution), frame[1], 1, 1
        elif frame[0] == 'ver':
            return frame[1], round(frame[1] / resolution), 1, 1

    def execute(self):
        """Check whether multiple video thumbnails are created or a single thumbnail is created.

        Returns:
            Run self.exporting_frame(path)

        Raises:
            ValueError: If file in the path is not a video.
        """
        if (self.path is None) or (self.output is None):
            self.error(9)
            return
        if self.is_path_dir is True:
            for vids in self.inside_vids:
                self.exporting_frame(vids)
        else:
            self.exporting_frame(self.path)

    def exporting_frame(self, path):
        """Make thumbnail(s) from path.

        Args:
            path: Path to execute.

        Returns:
            Output thumbnail image(s)
        """
        video_file = cv2.VideoCapture(path)
        frame_num = self.get_output_framenum(video_file)
        size = self.frame_size()
        name = os.path.basename(path)[:-4]
        video_file.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = video_file.read()
        if ret is False:
            self.error(10)
            return
        if len(size) == 2:
            size = self.size_calculate(video_file, size)
        if self.size_change is True:
            frame = cv2.resize(frame, dsize=(size[0], size[1]), fx=size[2], fy=size[3], interpolation=cv2.INTER_AREA)
        cv2.imwrite(os.path.join(self.output, f'{name}_thumbnail.jpg'), frame)

    def get_output_framenum(self, vid_file):
        """Calculate the exact frame number to write.

        Args:
            vid_file: Video file to check its total number of frames.

        Returns:
            Exact frame number to write thumbnail.
        """
        length = int(vid_file.get(cv2.CAP_PROP_FRAME_COUNT))
        if self.frame_preset == 'first':
            return 1
        if self.frame_preset == 'last':
            return length
        if self.frame_preset == 'middle':
            return length // 2
        if self.frame_preset == 'one_third':
            return length // 3
        if self.frame_preset == 'two_third':
            return (length // 3) * 2
        if type(self.frame) is float:
            return self.float_framenum(length)
        if type(self.frame) is int:
            return self.int_framenum(length)

    def float_framenum(self, length):
        """This method is executed when calculating exact frame number from the frame position is needed.

        Args:
            length: Total number of frames in video

        Returns:
            Exact frame number to write thumbnail.
        """
        ex_num = self.frame * length
        if ex_num < 1:
            return 1
        else:
            return int(floor(ex_num))

    def int_framenum(self, length):
        """This method is executed when the user inputs an exact frame number.
        If the number is larger than total number of frames, the last frame will be the frame number to write.

        Args:
            length: Total number of frames

        Returns:
            Exact frame number to write thumbnail.
        """
        if self.frame < 0:
            return length + self.frame
        if self.frame <= length:
            return self.frame
        if self.is_path_dir > length:
            return length

    @staticmethod
    def error(err_num):
        """This method is executed when invalid values are entered into the input methods.

        Args:
            err_num: Error type

        Returns:
            This method will raise ValueError for each error type.
        """
        if err_num == 1:
            raise ValueError("Path Setting Error : Path must be an existing video file path,"
                             "or a directory that contains video.")
        if err_num == 2:
            raise ValueError("Path Setting Error : This path does not contain video. "
                             "You must set video file or directory as path.")
        if err_num == 3:
            raise ValueError("Path Setting Error : Output must be an existing directory.")
        if err_num == 4:
            raise ValueError("Input Error : Frame must be an integer.")
        if err_num == 5:
            raise ValueError("Input Error : Presets for frame are first, last, middle, one_third, two_third. "
                             "Other strings aren't supported.")
        if err_num == 6:
            raise ValueError("Input Error : Calculating the frame position requires float number between 0 and 1")
        if err_num == 7:
            raise ValueError("Input Error : Size must be two integer.  Parentheses are not necessary")
        if err_num == 8:
            raise ValueError("Input Error : Presets for size are full, half, quarter. "
                             "Other strings aren't supported.")
        if err_num == 9:
            raise ValueError("Path setting Error : Input path or output path not yet defined")
        if err_num == 10:
            raise ValueError("Path Setting Error : This path is not a video file path. "
                             "You must set video file path as path.")


# def main():
    # test = Thumbnailer()
    # test.size = 1000, 0
    # test.size_preset = 'quarter'
    # test.frame = -4
    # test.frame_preset = 'two_third'
    # test.frame_float = 0.2
    # test.path = '/home/rapa/test/colored/scene01/s1_03.mov'
    # test.output = '/home/rapa/test/colored'
    # test.execute()


# if __name__ == "__main__":
#     main()
