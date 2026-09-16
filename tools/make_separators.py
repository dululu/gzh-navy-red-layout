#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把分隔条从原始 4:1 画布改成更扁的比例。

为什么：4:1 在 645px 正文列宽下渲染高 161px（≈6 行正文），章头压得太重。
        END 条尤其浪费——内容只占原画布 12%，上下 474px 全是空白。

两种处理方式，勿混：
  · 章头条（壹/贰/叁）：内容本身占满画布，不能裁。要变扁只能
    「等比缩小内容 → 贴到更扁的画布上居中」，比例 = 新画布宽高比。
  · END 条：内容是居中的一条细带，直接裁掉上下留白即可。

用法：
  python3 tools/make_separators.py                # 用默认比例生成
  python3 tools/make_separators.py --head 340     # 章头条画布高（2160 宽，越小越扁）
  python3 tools/make_separators.py --end-band 161 # END 条裁出的高度
  python3 tools/make_separators.py --restore      # 从 original-4x1/ 还原成 4:1

依赖：Pillow
"""
import argparse
import os
import shutil

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")
ORIG = os.path.join(ASSETS, "original-4x1")

HEAD = ["separator-1-yi.png", "separator-2-er.png", "separator-3-san.png"]
END = "end-the-end.png"

DEFAULT_HEAD_H = 340     # 2160×340 → 6.35:1
DEFAULT_END_BAND = 161   # 2160×161 → 13.42:1


def content_bbox(im, thr=247):
    """找非白内容的包围盒，用来知道 END 条那条细带在哪。"""
    g = im.convert("L")
    px = g.load()
    w, h = g.size
    top = bot = None
    for y in range(h):
        if min(px[x, y] for x in range(0, w, 2)) < thr:
            if top is None:
                top = y
            bot = y
    return top, bot


def flatten_head(name, new_h):
    """章头条：内容等比缩到 new_h，居中贴到 2160×new_h 的白画布上。"""
    src = Image.open(os.path.join(ORIG, name)).convert("RGB")
    w, h = src.size
    content = src.resize((round(w * new_h / h), new_h), Image.LANCZOS)
    canvas = Image.new("RGB", (w, new_h), (255, 255, 255))
    canvas.paste(content, ((w - content.width) // 2, 0))
    canvas.save(os.path.join(ASSETS, name))
    return canvas.size


def crop_end(band):
    """END 条：以内容带为中心裁出 band 高。"""
    src = Image.open(os.path.join(ORIG, END)).convert("RGB")
    w, h = src.size
    top, bot = content_bbox(src)
    mid = (top + bot) // 2
    y0 = max(0, mid - band // 2)
    y1 = min(h, y0 + band)
    y0 = max(0, y1 - band)
    src.crop((0, y0, w, y1)).save(os.path.join(ASSETS, END))
    return (w, y1 - y0)


def restore():
    for f in HEAD + [END]:
        shutil.copy2(os.path.join(ORIG, f), os.path.join(ASSETS, f))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--head", type=int, default=DEFAULT_HEAD_H,
                    help="章头条画布高（宽固定 2160），默认 340 → 6.35:1")
    ap.add_argument("--end-band", type=int, default=DEFAULT_END_BAND,
                    help="END 条裁出高度，默认 161 → 13.42:1")
    ap.add_argument("--restore", action="store_true", help="还原成原始 4:1")
    a = ap.parse_args()

    if a.restore:
        restore()
        print("已还原为原始 4:1")
    else:
        for n in HEAD:
            w, h = flatten_head(n, a.head)
            print(f"{n:26s} {w}×{h}  {w/h:.2f}:1")
        w, h = crop_end(a.end_band)
        print(f"{END:26s} {w}×{h}  {w/h:.2f}:1")
    print("\n接着跑： python3 build.py && python3 build.py --plain")
