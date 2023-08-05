import pathlib
import random
import os

__all__ = ['make_image_cl_dataset']


def get_categories(path):
    root = pathlib.Path(path)
    categories = []
    for d in root.iterdir():
        if d.is_dir() and d.name[0] != '.' and d.name[0] != '_':
            categories.append(d.name)
    return categories


def _create_image_cl_dataset(path):
    root = pathlib.Path(path)
    categories = get_categories(path)
    for p in ['train', 'val']:
        for c in categories:
            d = root.parent / p / c
            d.mkdir(parents=True, exist_ok=True)
            print(f'已创建 {d} 目录')


def make_image_cl_dataset(raw_path, ratio=0.8):
    """创建图像分类数据集。该函数会自动在 raw_path 的同级目录下创建 train 和 val 文件夹，
       以用于存放训练集和验证集图片。

    Args:
        raw_path (str): 原始图片数据目录，该目录下有 N 个子目录，每个子目录下存放一个分类的图片
        ratio (float, optional): 训练集占比. Defaults to 0.8.
    """
    _create_image_cl_dataset(raw_path)
    categories = get_categories(raw_path)
    root = pathlib.Path(raw_path)
    all_paths = {c: list(root.joinpath(c).glob('*.jpg')) for c in categories}
    count = {c: len(all_paths[c]) for c in categories}
    for c in categories:
        print(f'{c} 图片有 {count[c]} 张')

    val_samples = {
        c: random.sample(all_paths[c], int(count[c] * (1 - ratio)))
        for c in categories
    }
    train_samples = {
        c: list(set(all_paths[c]) - set(val_samples[c]))
        for c in categories
    }

    for c in categories:
        for src in val_samples[c]:
            src_name = src.name
            dst = src.parent.parent.parent / 'val' / c / src_name
            os.link(src, dst)

    for c in categories:
        for src in train_samples[c]:
            src_name = src.name
            dst = src.parent.parent.parent / 'train' / c / src_name
            os.link(src, dst)
    print(f'训练集图片已存放在 {root.parent / "train"} 目录下')
    print(f'验证集图片已存放在 {root.parent / "val"} 目录下')
