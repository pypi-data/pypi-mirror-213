import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms, datasets
import torchvision.transforms.functional as TF
import os
import torch.optim as optim
import torch.nn.init as init
from loguru import logger

__all__ = ['Classifier']

MODELS = {
    'resetnet18': models.resnet18,
    'squeezenet1_0': models.squeezenet1_0,
    'swin_t': models.swin_t,
    'swin_s': models.swin_s,
    'swin_b': models.swin_b
}

WEIGHTS = {
    'resetnet18': models.ResNet18_Weights.DEFAULT,
    'squeezenet1_0': models.SqueezeNet1_0_Weights.DEFAULT,
    'swin_t': models.Swin_T_Weights.DEFAULT,
    'swin_s': models.Swin_S_Weights.DEFAULT,
    'swin_b': models.Swin_B_Weights.DEFAULT
}

OPTIMIZER = {
    'Adadelta': optim.Adadelta,
    'Adagrad': optim.Adagrad,
    'Adam': optim.Adam,
    'AdamW': optim.AdamW,
    'Adamax': optim.Adamax,
    'ASGD': optim.ASGD,
    'NAdam': optim.NAdam,
    'RAdam': optim.RAdam,
    'RMSprop': optim.RMSprop,
    'Rprop': optim.Rprop,
    'SGD': optim.SGD
}


def set_parameter_requires_grad(model, feature_extracting):
    if feature_extracting:
        for param in model.parameters():
            param.requires_grad = False


class Classifier():

    def __init__(self) -> None:
        self._mean = np.array([0.485, 0.456, 0.406])
        self._std = np.array([0.229, 0.224, 0.225])
        self._resize = (224, 224)
        self._device = torch.device(
            "cuda:0" if torch.cuda.is_available() else "cpu")

        # 训练相关
        self.feature_extract = True

    def _preprocess(self, bgr):
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        rgb = cv2.resize(rgb, self._resize)
        tensor = TF.to_tensor(rgb)
        tensor = TF.normalize(tensor, self._mean, self._std)
        tensor = torch.unsqueeze(tensor, 0)
        return tensor

    def get_avaliable_model_name(self):
        """获取当前支持的模型名称列表。

        Returns:
            list[str]: 模型名称列表
        """
        return list(MODELS.keys())

    def get_base_model(self, model_name='resetnet18', weights='pretrained'):
        """获取基础模型

        Args:
            model_name (str, optional): 模型名称。可用 `get_avaliable_model_name` 查看支持的模型。 Defaults to 'resetnet18'.
            weights (any, optional): 当为 'pretrained' 时，会载入训练好的参数，
            当为 None 时，会随机初始化参数，当为其它值时，会当作权重文件路径并载入相应的权重。 Defaults to 'pretrained'.

        Returns:
            torch.nn.Module: torch 模型
        """
        _model = MODELS[model_name]
        if weights == 'pretrained':
            w = WEIGHTS[model_name]
            model = _model(weights=w)
        else:
            model = _model(weights=None)
            if weights is not None:
                model.load_state_dict(weights)
        model = model.to(self._device)
        model.eval()
        self.model = model
        self.categories = models.SqueezeNet1_0_Weights.DEFAULT.meta[
            'categories']
        return model

    def create_model(self, base_model_name, num_classes, feature_extract=True):
        """创建分类模型

        Args:
            base_model_name (str): 基础模型名称，创建模型时会以此模型作为骨干网络。
            可用 `get_avaliable_model_name` 查看支持的模型。
            num_classes (int): 分类数量
            feature_extract (bool, optional): 为 True 时，进行特征提取，为 False 时，进行微调. Defaults to True.

        Returns:
            torch.nn.Module: torch 模型
        """
        _model = MODELS[base_model_name]
        w = WEIGHTS[base_model_name]
        model_ft = _model(weights=w)
        set_parameter_requires_grad(model_ft, feature_extract)
        if base_model_name == 'resetnet18':
            num_ftrs = model_ft.fc.in_features
            model_ft.fc = nn.Linear(num_ftrs, num_classes)
        elif base_model_name == 'squeezenet1_0':
            final_conv = nn.Conv2d(512,
                                   num_classes,
                                   kernel_size=(1, 1),
                                   stride=(1, 1))
            # see https://github.com/pytorch/vision/blob/v0.13.1/torchvision/models/squeezenet.py#L88
            init.normal_(final_conv.weight, mean=0, std=0.01)
            if final_conv.bias is not None:
                init.constant_(final_conv.bias, 0)
            model_ft.classifier[1] = final_conv
            model_ft.num_classes = num_classes
        elif base_model_name == 'swin_t' or base_model_name == 'swin_s' or base_model_name == 'swin_b':
            num_ftrs = model_ft.head.in_features
            model_ft.head = nn.Linear(num_ftrs, num_classes)
            # see https://github.com/pytorch/vision/blob/v0.13.1/torchvision/models/swin_transformer.py#L399
            init.trunc_normal_(model_ft.head.weight, std=0.02)
            if model_ft.head.bias is not None:
                init.zeros_(model_ft.head.bias)
        model_ft = model_ft.to(self._device)
        self.model = model_ft
        self.feature_extract = feature_extract
        return model_ft

    def load_model(self, path):
        """载入模型

        Args:
            path (str): 模型文件路径，文件类型一般是 pth 
        """
        self.model = torch.load(path).to(self._device)

    def load_label(self, label_path):
        """载入标签，该标签会在解析预测结果时用到

        Args:
            label_path (str): 标签文件路径，一般来说，使用 `create_dataloaders` 方法
            生成的标签文件
        """
        labels = []
        with open(label_path, 'r', encoding='utf-8') as f:
            for line in f:
                labels.append(line.strip())

        self.categories = labels

    def save_model(self, file_path='MyModel.pth'):
        """保存模型

        Args:
            file_path (str, optional): 模型文件保存路径. Defaults to 'MyModel.pth'.
        """
        torch.save(self.model, file_path)
        logger.debug(f'模型已保存到 {file_path}')

    def load_weights(self, weight_path):
        """载入权重

        Args:
            weight_path (str): 权重文件路径
        """
        self.model.load_state_dict(torch.load(weight_path))

    def predict(self, img):
        """运行推理，返回 softmax 后的结果

        Args:
            img (numpy.ndarray): BGR格式的图片
        
        Returns:
            numpy.ndarray: 返回 N 维的向量，N是分类数量。每一项对应相应分类的置信度。
        """
        self.model.eval()
        tensor = self._preprocess(img)
        with torch.no_grad():
            tensor = tensor.to(self._device)
            output = self.model(tensor)
            return nn.functional.softmax(output, dim=1).cpu().numpy()[0]

    def parse_prediction(self, predictions, top_k=1):
        """解析模型的推理结果。在使用前，请确保你已载入相应的标签文件。
           如果你直接使用基础模型（ImageNet 1000分类），则无需载入标签文件。

        Args:
            predictions (numpy.ndarray): `predict` 方法返回的结果
            top_k (int, optional): 解析可能性最高的 k 个结果. Defaults to 1.
        """
        idx_score_pairs = self.get_top_k(predictions, top_k)
        print('该图片')
        for t in idx_score_pairs:
            print(f"有{t[1]*100:.1f}%的可能是'{self.categories[t[0]]}'")

    def get_top_k(self, predictions, top_k=1):
        """获取分数最高的 `top_k` 个结果

        Args:
            predictions (numpy.ndarray): `predict` 方法返回的结果
            top_k (int, optional): 该数值决定返回的结果个数. Defaults to 1.

        Returns:
            list(tuple): 每个元组都是一个“索引-分数”对，元组内的“分数”就是 `predictions` 中
            成绩最高的 `top_k` 个之一，而“索引”就是该“分数”在 `predictions` 的索引号。
        """
        if top_k > len(predictions):
            top_k = len(predictions)
        top_k_idx = np.argpartition(predictions, -top_k)[-top_k:]
        scores = [predictions[i] for i in top_k_idx]
        return list(zip(list(top_k_idx), scores))

    def create_dataloaders(self,
                           dir,
                           label_save_path='labels.txt',
                           batch_size=4,
                           random_hflips=True,
                           color_jitter=(0.2, 0.2, 0.1, 0.1),
                           random_rotation=10,
                           random_crop=(0.8, 1.0)):
        """创建数据载入器

        Args:
            dir (str): 存放数据集的文件夹路径，该目录下应包含 train 和 val 两个文件夹
            label_save_path (str, optional): 标签文件保存路径. Defaults to 'labels.txt'.
            batch_size (int, optional): 批大小，根据自身电脑的内存或显存大小而设，数字越大，训练时占用的内存或显存就越大. Defaults to 4.
            random_hflips (bool, optional): 是否随机水平镜像图片. Defaults to True.
            color_jitter (tuple, optional): 随机改变图片的亮度、对比度、饱和度、色相，详细说明见 
                https://pytorch.org/vision/0.13/generated/torchvision.transforms.ColorJitter.html#torchvision.transforms.ColorJitter.
                Defaults to (0.2, 0.2, 0.1, 0.1).
            random_rotation (int, optional): 随机改变图片的角度. Defaults to 10.
            random_crop (tuple, optional): 随机剪裁图片的范围. Defaults to (0.8, 1.0).

        Returns:
            dict: 含有训练集与验证集的数据载入器
        """

        train_tf = [
            transforms.ColorJitter(*color_jitter),
            transforms.RandomRotation(random_rotation),
            transforms.RandomResizedCrop(224, scale=random_crop),
        ]
        if random_hflips:
            train_tf.append(transforms.RandomHorizontalFlip())

        train_tf.append(transforms.ToTensor())
        train_tf.append(
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]))
        data_transforms = {
            'train':
            transforms.Compose(train_tf),
            'val':
            transforms.Compose([
                transforms.Resize(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406],
                                     [0.229, 0.224, 0.225])
            ]),
        }

        image_datasets = {
            x: datasets.ImageFolder(os.path.join(dir, x), data_transforms[x])
            for x in ['train', 'val']
        }
        dataloaders = {
            x: torch.utils.data.DataLoader(image_datasets[x],
                                           batch_size=batch_size,
                                           shuffle=True,
                                           num_workers=0)
            for x in ['train', 'val']
        }
        class_names = image_datasets['train'].classes

        with open(label_save_path, 'w', encoding='utf-8') as f:
            for c in class_names:
                f.write(f'{c}\r\n')

        logger.debug(f'分类标签已保存到 {os.path.abspath(label_save_path)} 文件')
        return dataloaders

    def create_optimizer(self, optim_name, lr=0.001):
        params_to_update = self.model.parameters()
        print("需要训练的参数:")
        if self.feature_extract:
            params_to_update = []
            for name, param in self.model.named_parameters():
                if param.requires_grad == True:
                    params_to_update.append(param)
                    print("\t", name)
        else:
            for name, param in self.model.named_parameters():
                if param.requires_grad == True:
                    print("\t", name)
        optimizer = OPTIMIZER[optim_name](params_to_update, lr=lr)

        return optimizer

    def get_avaliable_optimizer_name(self):
        """获取可用的优化器名称

        Returns:
            list[str]: 优化器名称列表
        """
        return list(OPTIMIZER.keys())

    def train(self,
              dataloaders,
              optimizer='Adam',
              lr=0.001,
              save_path='.',
              num_epochs=10):
        """训练模型

        Args:
            dataloaders (dict): 由 `create_dataloaders` 方法创建的数据载入器
            optimizer (str, optional): 优化器名称，可用 `get_avaliable_optimizer_name` 查看支持的优化器。 Defaults to 'Adam'.
            lr (float, optional): 学习率. Defaults to 0.001.
            save_path (str, optional): 权重保存目录. Defaults to '.'.
            num_epochs (int, optional): 训练次数. Defaults to 10.
        """

        model = self.model.to(self._device)
        device = self._device
        optimizer = self.create_optimizer(optimizer, lr)

        train_loader = dataloaders['train']
        val_loader = dataloaders['val']

        best_acc = 0.

        for ep in range(num_epochs):
            model.train()
            train_loss = 0.0
            train_acc = 0.
            for images, labels in iter(train_loader):
                images = images.to(device)
                labels = labels.to(device)
                optimizer.zero_grad()
                outputs = model(images)

                loss = F.cross_entropy(outputs, labels)
                _, preds = torch.max(outputs, 1)
                train_acc += torch.sum(preds == labels.data)
                train_loss += loss.item()
                loss.backward()
                optimizer.step()
            train_loss /= len(train_loader)
            train_acc /= len(train_loader.dataset)

            model.eval()
            test_loss = 0.0
            test_acc = 0.
            for items in iter(val_loader):
                images, labels = items[:2]
                images = images.to(device)
                labels = labels.to(device)
                outputs = model(images)

                loss = F.cross_entropy(outputs, labels)
                _, preds = torch.max(outputs, 1)
                test_acc += torch.sum(preds == labels.data)
                test_loss += loss.item()

            test_loss /= len(val_loader)
            test_acc /= len(val_loader.dataset)
            logger.debug(
                f"epoch {ep} - train loss: {train_loss}, val loss: {test_loss}"
            )

            logger.debug(f"train acc: {train_acc}, val acc: {test_acc}")

            if test_acc > best_acc:
                torch.save(model.state_dict(),
                           os.path.join(save_path, 'best_ckpt.pth'))
                logger.debug(
                    f"权重已保存到 {os.path.join(save_path,'best_ckpt.pth')}")
                best_acc = test_acc
