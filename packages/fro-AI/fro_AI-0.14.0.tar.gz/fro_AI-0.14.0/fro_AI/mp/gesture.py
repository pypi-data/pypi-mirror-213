import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2
from fro_AI.utils.data_utils import get_file, get_hash_prefix_from_file_name
import time
import cv2

model_url = 'http://gz.chuangfeigu.com:8087/fro_AI/models/gesture_recognizer/gesture_recognizer-97952348.task'

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


def get_file_name(url):
    return url.split('/')[-1]


class GestureRecognizer:

    def __init__(self, model_path=None, mode='image', num_hands=1) -> None:
        """ 手势识别

        默认模型可识别 7 种手势：👍, 👎, ✌️, ☝️, ✊, 👋, 🤟('Thumb Up', 'Thumb Down', 'Vcitory', 'Pointing Up', 'Closed Fist', 'Open Palm', 'I Love You')

        Args:
            model_path(str): 模型路径，为 None 时，会自动从网络下载默认模型参数
            mode(str): 'image' or 'video'
            num_hands(int): 识别手的数量
        """
        if model_path is None:
            hash_prefix = get_hash_prefix_from_file_name(
                get_file_name(model_url))
            model_path = get_file(get_file_name(model_url),
                                  model_url,
                                  hash_prefix=hash_prefix,
                                  cache_subdir='models/gesture_recognizer')
        base_options = python.BaseOptions(model_asset_path=model_path)
        running_mode = vision.RunningMode.IMAGE if mode == 'image' else vision.RunningMode.VIDEO
        options = vision.GestureRecognizerOptions(base_options=base_options,
                                                  running_mode=running_mode,
                                                  num_hands=num_hands)
        self.recognizer = vision.GestureRecognizer.create_from_options(options)
        self.mode = mode

    def process(self, image):
        """ 处理图片或视频帧

        Args:
            image: 图片或视频帧

        Returns:
            gestures: 手势识别结果
            hand_landmarks: 手部关键点坐标
        """
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        if self.mode == 'image':
            recognition_result = self.recognizer.recognize(mp_image)
        else:
            frame_timestamp_ms = int(time.time() * 1000)
            recognition_result = self.recognizer.recognize_for_video(
                mp_image, frame_timestamp_ms)
        gestures = recognition_result.gestures
        hand_landmarks = recognition_result.hand_landmarks
        return gestures, hand_landmarks

    def infer(self, image):
        """ 预测

        Args:
            image: 图片或视频帧

        Returns:
            gestures (List[str,float]): 手势识别结果，由手势名称和置信度组成的列表，如 [('Thumb Up', 0.9)]
            hand_landmarks (List[List[Tuple(float,float,float)]]): 手部关键点坐标，如 [[(0.1, 0.2, 0.3), (0.2, 0.3, 0.4), ...]]
        """
        gestures, hand_landmarks = self.process(image)
        if len(gestures) == 0:
            return [], []
        gestures = [(g.category_name, g.score) for g in gestures[0]]
        hand_landmarks = [[(lm.x, lm.y, lm.z) for lm in hand]
                          for hand in hand_landmarks]
        return gestures, hand_landmarks

    def visualize(self, image, gestures, hand_landmarks):
        """ 可视化手势识别结果

        Args:
            image: 图片或视频帧
            gestures: 手势识别结果
            hand_landmarks: 手部关键点坐标

        Returns:
            image: 可视化后的图片或视频帧
        """
        if len(gestures) == 0:
            return image
        top_gesture = gestures[0]
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=lm[0], y=lm[1], z=lm[2])
            for lm in hand_landmarks[0]
        ])
        mp_drawing.draw_landmarks(
            image, hand_landmarks_proto, mp.solutions.hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
        title = f"{top_gesture[0]} ({top_gesture[1]:.2f})"
        dynamic_text_size = int(max(image.shape[0], image.shape[1]) / 40 * 0.1)
        cv2.putText(image, title, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    dynamic_text_size, (0, 0, 255), 2)
        return image


if __name__ == '__main__':
    cap = cv2.VideoCapture(1)
    recognizer = GestureRecognizer(mode='video')
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        results = recognizer.process(frame)
        frame = recognizer.visualize(frame, *results)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
