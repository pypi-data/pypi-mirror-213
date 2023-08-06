from face_recognition import face_locations, face_landmarks
from math import ceil
import base64
import cv2
import ffmpeg
import logging

logger = logging.getLogger("Misc")
logger.setLevel(logging.DEBUG)


class Misc:
    def __init__(self):
        # BBX
        self.locations = None
        self.process_this_frame = None
        self.scale = None
        self.scale_back = None
        self.offset = 0
        # Blink
        self.landmarks = None
        self.eye_left = None
        self.eye_right = None
        self.eye_left_bbx = None
        self.eye_right_bbx = None
        # Mouth
        self.th_area = 0.45
        self.bbx_b_lip = None
        self.bbx_t_lip = None
        self.area = 0
        # Resize
        self.aspect_ratio_4_3 = float(4 / 3)
        self.aspect_ratio_16_9 = float(16 / 9)

        self.process_this_frame = True
        self.scale = 0.25
        self.scale_back = ceil(1 / self.scale)
        self.offset = 20

    def __del__(self):
        pass

    def encodeFrame64(self, frame):
        """Encode frame to base 64.
        @frame: frame CV2_64 to be encoded"""
        if frame is not None:
            ret, buffer = cv2.imencode(".jpg", frame)
            if ret:
                return base64.b64encode(buffer).decode("utf-8")
            return None
        else:
            return None

    def resize_to_VGA(self, frame):
        """Resize a given frame to VGA in 16:9 (854x480) or 4:3 (640X480)
        @frame: Frame to be resized."""
        (h, w) = frame.shape[:2]
        if w / h == self.aspect_ratio_16_9 and (w != 854 or h != 480):
            return cv2.resize(frame, (480, 854), interpolation=cv2.INTER_CUBIC)
        elif w / h == self.aspect_ratio_4_3 and (w != 640 or h != 480):
            return cv2.resize(frame, (480, 640), interpolation=cv2.INTER_CUBIC)
        else:
            return frame

    def resize_to_QVGA(self, frame):
        """Resize a given frame to QVGA in 16:9 (854x480) or 4:3 (640X480)
        @frame: Frame to be resized."""
        (h, w) = frame.shape[:2]
        if float(h / w) == self.aspect_ratio_16_9 and (w != 427 or h != 240):
            return cv2.resize(frame, (240, 426), interpolation=cv2.INTER_CUBIC)
        elif float(h / w) == self.aspect_ratio_4_3 and (w != 320 or h != 240):
            return cv2.resize(frame, (240, 320), interpolation=cv2.INTER_CUBIC)
        else:
            return frame

    def get_BBX(self, frame=None, method=None):
        """Get a face Bounding Box from the videostream frame.
        @frame: frame from the videostream."""
        if frame is not None:
            small_frame = self.resize_to_QVGA(frame)
            # Only process every other frame of video to save time
            if self.process_this_frame:
                rgb_small_frame = small_frame[:, :, ::-1]
                # Find all the faces and face encodings
                # in the current frame of video
                if method is None or method != "multiple_faces":
                    self.locations = face_locations(
                        rgb_small_frame, model="hog")
                else:
                    self.locations = face_locations(
                        rgb_small_frame, model="cnn")

            self.process_this_frame = not self.process_this_frame
            # Initialize face matrix and BBx components that will be returned
            face = []  # np.zeros_like(frame)
            bbx = []
            top, right, bottom, left = (0, 0, 0, 0)

            for (top, right, bottom, left) in self.locations:
                # Scale back up face locations since the frame we
                # detected in was scaled to 1/4 size
                # top *= self.scale_back
                # right *= self.scale_back
                # bottom *= self.scale_back
                # left *= self.scale_back

                # face.append(frame[top:bottom, left:right])
                face.append(small_frame[top:bottom, left:right])
                bbx.append((top, bottom, left, right))
            return face, bbx
        else:
            return None, None

    # FaceLandmarks
    def get_face_landmarks(self, face):
        """Find face landmarks and store given a face frame.
        @face: face frame."""

        self.landmarks = face_landmarks(
            face, face_locations=None, model="large")
        ret_lendmarks = False
        if len(self.landmarks):
            # Left eye
            start = (
                self.landmarks[0]["right_eye"][0][0] - self.offset,
                self.landmarks[0]["right_eye"][0][1] - self.offset,
            )
            end = (
                self.landmarks[0]["right_eye"][3][0] + self.offset,
                self.landmarks[0]["right_eye"][3][1] + self.offset,
            )
            self.eye_left_bbx = (start, end)
            self.eye_right = face[start[1]: end[1], start[0]: end[0]]
            # Right eye
            start = (
                self.landmarks[0]["left_eye"][0][0] - self.offset,
                self.landmarks[0]["left_eye"][0][1] - self.offset,
            )
            end = (
                self.landmarks[0]["left_eye"][3][0] + self.offset,
                self.landmarks[0]["left_eye"][3][1] + self.offset,
            )
            self.eye_right_bbx = (start, end)
            self.eye_left = face[start[1]: end[1], start[0]: end[0]]
            # Mouth
            self.bbx_b_lip = self.landmarks[0]["bottom_lip"]
            self.bbx_t_lip = self.landmarks[0]["top_lip"]
            ret_lendmarks = True
        else:
            self.eye_left = None
            self.eye_right = None
            self.eye_left_bbx = None
            self.eye_right_bbx = None
            self.bbx_b_lip = None
            self.bbx_t_lip = None
        return ret_lendmarks

    # Blink
    def get_eye_left(self):
        """ Returns the left eye matrix frame"""
        return self.eye_left

    def get_eye_right(self):
        """ Returns the right eye matrix frame"""
        return self.eye_right

    def get_eyes_bbx(self):
        """ Returns the right and left eyes bbxs"""
        return (self.eye_right_bbx, self.eye_left_bbx)

    # Mouth
    def get_lips_bbx(self):
        return (self.bbx_t_lip, self.bbx_b_lip)

    def check_face_area(self):
        """ Returns if face area is greather than the minimum required."""
        return self.area > self.th_area

    def compute_face_area(self, bbx, shape):
        """Compute face area given the bbx of a face.
        @bbx: bbx of a detected face.
        @shape: face shape."""
        if len(bbx):
            (y, w, h, x) = bbx
            self.area = (w * h) / (shape[0] * shape[1])

    # https://github.com/melvinkokxw/face_emotion_detection/commit/68febcc3c2e47f723d9fb275be3c0357cf68b31c
    def check_rotation(self, video_file):
        """Checks if given video file has rotation metadata
        Used as workaround for OpenCV bug
        https://github.com/opencv/opencv/issues/15499,
        where the rotation metadata in a video is not used
         by cv2.VideoCapture. May have to be removed/tweaked
        when bug is fixed in a new opencv-python release.
        Parameters
        ----------
        video_file : str
            Path to video file to be checked
        Returns
        -------
        rotate_code : enum or None
            Flag fror cv2.rotate to decide how much to rotate the image.
            None if no rotation is required
        """

        try:
            meta_dict = ffmpeg.probe(video_file)
            rotation_angle = int(meta_dict["streams"][0]["tags"]["rotate"])
        except Exception as ex:
            print(f'Failed to get rotate tag in check_rotation: {video_file}')
            return None

        rotate_code = None
        if rotation_angle == 90:
            rotate_code = cv2.ROTATE_90_CLOCKWISE
        elif rotation_angle == 180:
            rotate_code = cv2.ROTATE_180
        elif rotation_angle == 270:
            rotate_code = cv2.ROTATE_90_COUNTERCLOCKWISE

        return rotate_code
