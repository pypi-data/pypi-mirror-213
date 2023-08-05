import cv2
import numpy as np
import qrcode
import pyzbar.pyzbar as pyzbar


class QRCode:

    def generate(self, data):
        """ 生成二维码

        Args:
            data (Any): 二维码数据，一般输入字符串

        Returns:
            img: 二维码图片
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        return img

    def detect(self, image: np.ndarray):
        """ 检测二维码

        Args:
            image (np.ndarray): 输入图片

        Returns:
            List[Dict]: 二维码检测结果，每个二维码对应一个字典，字典包含以下字段：
                data: 二维码数据，数据会自动按utf-8解码
                type: 二维码类型
                position: 二维码位置，(left, top, width, height)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        codes = pyzbar.decode(gray)
        results = []
        for code in codes:
            result = {
                'data': code.data.decode('utf-8'),
                'type': code.type,
                'position': code.rect
            }
            results.append(result)
        return results


if __name__ == '__main__':
    qr = QRCode()
    img = qr.generate('hello world')
    img.save('hello_world.png')
