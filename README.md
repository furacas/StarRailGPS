# StarRailGPS

`StarRailGPS`是一个 Python 包，它提供了一个函数，用于在游戏中找到小地图在大地图中的位置。

## 安装
你可以通过 pip 安装 StarRailGPS：

```commandline
pip install StarRailGPS
```

## 使用
导入`StarRailGPS`包并调用`position`函数：

```python
from StarRailGPS import position

# screen是输入的1080分辨率的图像
x, y = position(screen)
```

## 开发计划

- 现阶段map_name现阶段需要从外面传入，后面可以直接从图片中截取
- 现阶段只支持1080后面考虑全分辨率支持