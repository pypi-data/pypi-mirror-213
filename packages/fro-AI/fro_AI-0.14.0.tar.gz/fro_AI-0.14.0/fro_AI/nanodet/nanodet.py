import cv2
import numpy as np
import math
from fro_AI.utils.data_utils import get_file, get_hash_prefix_from_file_name

model_url = 'http://gz.chuangfeigu.com:8087/fro_AI/models/nanodet/nanodet-plus-m_320-569490b4.onnx'
label_url = 'http://gz.chuangfeigu.com:8087/fro_AI/models/nanodet/coco-634a1132.names'


def get_file_name(url):
    return url.split('/')[-1]


class NanoDet:

    def __init__(self,
                 model_path=None,
                 label_path=None,
                 prob_threshold=0.5,
                 iou_threshold=0.4) -> None:
        """ 只支持 NanoDet-plus-m_320 模型

        onnx 模型使用官方的脚本转换

        自己训练时，注意 keep-ratio 参数要设置为 false，目前的代码不支持 keep-ratio

        Args:
            model_path (str, optional): 模型地址. Defaults to None.
            label_path (str, optional): 标签地址. Defaults to None.
            prob_threshold (float, optional): 置信度阈值. Defaults to 0.5.
            iou_threshold (float, optional): iou阈值. Defaults to 0.4.
        """
        if model_path is None:
            hash_prefix = get_hash_prefix_from_file_name(
                get_file_name(model_url))
            model_path = get_file(get_file_name(model_url),
                                  model_url,
                                  hash_prefix=hash_prefix,
                                  cache_subdir='models/nanodet')
        if label_path is None:
            hash_prefix = get_hash_prefix_from_file_name(
                get_file_name(label_url))
            label_path = get_file(get_file_name(label_url),
                                  label_url,
                                  hash_prefix=hash_prefix,
                                  cache_subdir='models/nanodet')
        self.net = cv2.dnn.readNet(model_path)
        # Load labels
        self.class_names = list(
            map(lambda x: x.strip(),
                open(label_path, 'r').readlines()))
        self.num_classes = len(self.class_names)
        self.prob_threshold = prob_threshold
        self.iou_threshold = iou_threshold
        self.mean = np.array([103.53, 116.28, 123.675],
                             dtype=np.float32).reshape(1, 1, 3)
        self.std = np.array([57.375, 57.12, 58.395],
                            dtype=np.float32).reshape(1, 1, 3)
        self.input_shape = (320, 320)
        self.reg_max = 7
        self.project = np.arange(self.reg_max + 1)
        self.strides = (8, 16, 32, 64)
        self.mlvl_anchors = []
        for i in range(len(self.strides)):
            anchors = self._make_grid(
                (math.ceil(self.input_shape[0] / self.strides[i]),
                 math.ceil(self.input_shape[1] / self.strides[i])),
                self.strides[i])
            self.mlvl_anchors.append(anchors)

    def get_class_names(self):
        return self.class_names

    def _make_grid(self, featmap_size, stride):
        feat_h, feat_w = featmap_size
        shift_x = np.arange(0, feat_w) * stride
        shift_y = np.arange(0, feat_h) * stride
        xv, yv = np.meshgrid(shift_x, shift_y)
        xv = xv.flatten()
        yv = yv.flatten()
        return np.stack((xv, yv), axis=-1)

    def softmax(self, x, axis=1):
        x_exp = np.exp(x)
        # 如果是列向量，则axis=0
        x_sum = np.sum(x_exp, axis=axis, keepdims=True)
        s = x_exp / x_sum
        return s

    def _normalize(self, img):
        img = img.astype(np.float32)
        img = (img - self.mean) / (self.std)
        return img

    def preprocess(self, img):
        img = cv2.resize(img, self.input_shape)
        img = self._normalize(img)
        return img

    def postprocess(self, preds):
        # preds = preds.reshape(-1, self.num_classes + (self.reg_max + 1) * 4)
        mlvl_bboxes = []
        mlvl_scores = []
        ind = 0
        for stride, anchors in zip(self.strides, self.mlvl_anchors):
            cls_score, bbox_pred = preds[ind:(
                ind + anchors.shape[0]), :self.num_classes], preds[ind:(
                    ind + anchors.shape[0]), self.num_classes:]
            ind += anchors.shape[0]
            bbox_pred = self.softmax(bbox_pred.reshape(-1, self.reg_max + 1),
                                     axis=1)
            bbox_pred = np.dot(bbox_pred, self.project).reshape(-1, 4)
            bbox_pred *= stride

            nms_pre = 1000
            if nms_pre > 0 and cls_score.shape[0] > nms_pre:
                max_scores = cls_score.max(axis=1)
                topk_inds = max_scores.argsort()[::-1][0:nms_pre]
                anchors = anchors[topk_inds, :]
                bbox_pred = bbox_pred[topk_inds, :]
                cls_score = cls_score[topk_inds, :]

            bboxes = self.distance2bbox(anchors,
                                        bbox_pred,
                                        max_shape=self.input_shape)
            mlvl_bboxes.append(bboxes)
            mlvl_scores.append(cls_score)

        mlvl_bboxes = np.concatenate(mlvl_bboxes, axis=0)
        mlvl_scores = np.concatenate(mlvl_scores, axis=0)

        bboxes_wh = mlvl_bboxes.copy()
        bboxes_wh[:, 2:4] = bboxes_wh[:, 2:4] - bboxes_wh[:, 0:2]  ####xywh
        classIds = np.argmax(mlvl_scores, axis=1)
        confidences = np.max(mlvl_scores, axis=1)  ####max_class_confidence

        indices = cv2.dnn.NMSBoxes(bboxes_wh.tolist(), confidences.tolist(),
                                   self.prob_threshold, self.iou_threshold)
        if len(indices) > 0:
            mlvl_bboxes = mlvl_bboxes[indices]
            confidences = confidences[indices]
            classIds = classIds[indices]
            return mlvl_bboxes, confidences, classIds
        else:
            return np.array([]), np.array([]), np.array([])

    def distance2bbox(self, points, distance, max_shape=None):
        x1 = points[:, 0] - distance[:, 0]
        y1 = points[:, 1] - distance[:, 1]
        x2 = points[:, 0] + distance[:, 2]
        y2 = points[:, 1] + distance[:, 3]
        if max_shape is not None:
            x1 = np.clip(x1, 0, max_shape[1]) / max_shape[1]
            y1 = np.clip(y1, 0, max_shape[0]) / max_shape[0]
            x2 = np.clip(x2, 0, max_shape[1]) / max_shape[1]
            y2 = np.clip(y2, 0, max_shape[0]) / max_shape[0]
        return np.stack([x1, y1, x2, y2], axis=-1)

    def infer(self, img):
        """ 推理

        Args:
            img (np.ndarray): 输入图像

        Returns:
            bboxes (np.ndarray): 检测框
            confidences (np.ndarray): 置信度
            classIds (np.ndarray): 类别ID
        """
        img = self.preprocess(img)
        blob = cv2.dnn.blobFromImage(img)
        self.net.setInput(blob)
        preds = self.net.forward(
            self.net.getUnconnectedOutLayersNames())[0].squeeze(axis=0)
        bboxes, confidences, classIds = self.postprocess(preds)
        return bboxes, confidences, classIds

    def visualize(self, img, bboxes, confidences, classIds):
        """ 可视化

        Args:
            img (np.ndarray): 输入图像
            bboxes (np.ndarray): 检测框
            confidences (np.ndarray): 置信度
            classIds (np.ndarray): 类别ID

        Returns:
            img (np.ndarray): 可视化后的图像
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        for i, bbox in enumerate(bboxes):
            label = int(classIds[i])
            color = (_COLORS[label] * 255).astype(np.uint8).tolist()
            text = f"{self.class_names[label]}:{confidences[i]*100:.1f}%"
            txt_color = (0, 0,
                         0) if np.mean(_COLORS[label]) > 0.5 else (255, 255,
                                                                   255)
            txt_size = cv2.getTextSize(text, font, 0.5, 2)[0]
            x1, y1, x2, y2 = bbox
            x1 *= img.shape[1]
            y1 *= img.shape[0]
            x2 *= img.shape[1]
            y2 *= img.shape[0]
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color,
                          2)
            # 自动调整文本位置，使其在图像内
            if y1 - txt_size[1] - 2 < 0:
                y1 = txt_size[1] + 2
            if x1 + txt_size[0] + 2 > img.shape[1]:
                x1 = img.shape[1] - txt_size[0] - 2
            cv2.rectangle(img, (int(x1), int(y1 - txt_size[1] - 2)),
                          (int(x1 + txt_size[0]), int(y1)), color, -1)
            cv2.putText(img,
                        text, (int(x1), int(y1 - 2)),
                        font,
                        0.5,
                        txt_color,
                        thickness=1,
                        lineType=cv2.LINE_AA)
        return img


_COLORS = (np.array([
    0.000,
    0.447,
    0.741,
    0.850,
    0.325,
    0.098,
    0.929,
    0.694,
    0.125,
    0.494,
    0.184,
    0.556,
    0.466,
    0.674,
    0.188,
    0.301,
    0.745,
    0.933,
    0.635,
    0.078,
    0.184,
    0.300,
    0.300,
    0.300,
    0.600,
    0.600,
    0.600,
    1.000,
    0.000,
    0.000,
    1.000,
    0.500,
    0.000,
    0.749,
    0.749,
    0.000,
    0.000,
    1.000,
    0.000,
    0.000,
    0.000,
    1.000,
    0.667,
    0.000,
    1.000,
    0.333,
    0.333,
    0.000,
    0.333,
    0.667,
    0.000,
    0.333,
    1.000,
    0.000,
    0.667,
    0.333,
    0.000,
    0.667,
    0.667,
    0.000,
    0.667,
    1.000,
    0.000,
    1.000,
    0.333,
    0.000,
    1.000,
    0.667,
    0.000,
    1.000,
    1.000,
    0.000,
    0.000,
    0.333,
    0.500,
    0.000,
    0.667,
    0.500,
    0.000,
    1.000,
    0.500,
    0.333,
    0.000,
    0.500,
    0.333,
    0.333,
    0.500,
    0.333,
    0.667,
    0.500,
    0.333,
    1.000,
    0.500,
    0.667,
    0.000,
    0.500,
    0.667,
    0.333,
    0.500,
    0.667,
    0.667,
    0.500,
    0.667,
    1.000,
    0.500,
    1.000,
    0.000,
    0.500,
    1.000,
    0.333,
    0.500,
    1.000,
    0.667,
    0.500,
    1.000,
    1.000,
    0.500,
    0.000,
    0.333,
    1.000,
    0.000,
    0.667,
    1.000,
    0.000,
    1.000,
    1.000,
    0.333,
    0.000,
    1.000,
    0.333,
    0.333,
    1.000,
    0.333,
    0.667,
    1.000,
    0.333,
    1.000,
    1.000,
    0.667,
    0.000,
    1.000,
    0.667,
    0.333,
    1.000,
    0.667,
    0.667,
    1.000,
    0.667,
    1.000,
    1.000,
    1.000,
    0.000,
    1.000,
    1.000,
    0.333,
    1.000,
    1.000,
    0.667,
    1.000,
    0.333,
    0.000,
    0.000,
    0.500,
    0.000,
    0.000,
    0.667,
    0.000,
    0.000,
    0.833,
    0.000,
    0.000,
    1.000,
    0.000,
    0.000,
    0.000,
    0.167,
    0.000,
    0.000,
    0.333,
    0.000,
    0.000,
    0.500,
    0.000,
    0.000,
    0.667,
    0.000,
    0.000,
    0.833,
    0.000,
    0.000,
    1.000,
    0.000,
    0.000,
    0.000,
    0.167,
    0.000,
    0.000,
    0.333,
    0.000,
    0.000,
    0.500,
    0.000,
    0.000,
    0.667,
    0.000,
    0.000,
    0.833,
    0.000,
    0.000,
    1.000,
    0.000,
    0.000,
    0.000,
    0.143,
    0.143,
    0.143,
    0.286,
    0.286,
    0.286,
    0.429,
    0.429,
    0.429,
    0.571,
    0.571,
    0.571,
    0.714,
    0.714,
    0.714,
    0.857,
    0.857,
    0.857,
    0.000,
    0.447,
    0.741,
    0.314,
    0.717,
    0.741,
    0.50,
    0.5,
    0,
]).astype(np.float32).reshape(-1, 3))
