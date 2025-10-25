# 视觉查找指定编号或二维码示例

下面的示例脚本展示了如何在静态图像中查找指定的编号（通过 OCR）或二维码。脚本依赖于 OpenCV 和 pytesseract，能够定位匹配区域并在需要时绘制可视化框。

## 依赖安装

```bash
pip install opencv-python pytesseract numpy
# 如果还没有安装 Tesseract OCR 引擎，请根据操作系统下载对应安装包。
```

## 使用说明

```bash
python docs/examples/visual_identifier_search.py <图片路径> \
    --serial "SB-00192" \
    --qr \
    --show
```

- `--serial`：设置需要查找的编号，支持大小写不敏感匹配。
- `--qr`：启用二维码检测并打印识别到的内容。
- `--show`：在窗口中展示标注结果。

脚本会输出匹配到的编号位置以及识别到的二维码数据，并在启用 `--show` 时在窗口中显示识别框，方便进行视觉确认。

## 下载示例代码

如果需要将示例脚本打包成单独的压缩包供他人下载，可以运行仓库中提供的打包工具：

```bash
python docs/examples/package_visual_identifier_search.py
# 或者指定输出路径
python docs/examples/package_visual_identifier_search.py --output /tmp/visual-search-example.zip
```

上述命令会生成 `visual_identifier_search_example.zip`，其中包含 Python 示例脚本以及本使用指南，便于分发或离线查看。
