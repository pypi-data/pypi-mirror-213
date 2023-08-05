import hyperlpr3 as lpr3
import cv2
import numpy as np
from PIL import Image
from PIL import ImageDraw


def draw_plate_on_image(img, box, text, font=None):
    x1, y1, x2, y2 = box
    cv2.rectangle(img, (x1, y1), (x2, y2), (139, 139, 102), 2, cv2.LINE_AA)
    cv2.rectangle(img, (x1, y1 - 20), (x2, y1), (139, 139, 102), -1)
    if font is not None:
        data = Image.fromarray(img)
        draw = ImageDraw.Draw(data)
        draw.text((x1 + 5, y1 - 20), text, (255, 255, 255), font=font)
        res = np.asarray(data)
        return res
    else:
        return img


class LPR:

    def __init__(self) -> None:
        self.model = lpr3.LicensePlateCatcher()

    def infer(self, image):
        """ 识别车牌

        Args:
            image (np.ndarray): 图片

        Returns:
            List[Tuple[str, float, int, Tuple[int, int, int, int]]]: 识别结果，每个车牌对应一个元组，元组包含以下字段：
                code: 车牌号
                confidence: 置信度
                type: 车牌类型
                position: 车牌位置，(x1, y1, x2, y2)
        """
        return self.model(image)

    def visualize(self, image, result, font=None):
        """ 可视化识别结果

        Args:
            image (np.ndarray): 图片
            result (List[Tuple[str, float, int, Tuple[int, int, int, int]]]): 识别结果
            font (ImageFont): 字体

        Returns:
            np.ndarray: 可视化结果
        """
        for code, confidence, _, box in result:
            text = f"{code} {confidence:.2f}"
            image = draw_plate_on_image(image, box, text, font)
        return image
