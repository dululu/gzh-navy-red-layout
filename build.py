#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把「藏蓝+红 · 章节分隔」排版模板构建成自包含的 index.html。

为什么需要它：
  公众号编辑器粘不了 file:// 或相对路径的图片，全选复制时图片会丢。
  把图片转成 base64 data URI 内嵌进 HTML，复制粘贴时图片就会跟着走。

用法：
  python3 build.py            # 生成 index.html（自包含）
  python3 build.py --plain    # 生成 index.relative.html（引用 assets/，便于阅读源码）
"""
import base64
import mimetypes
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

# 图片 → 文件名
IMG = {
    "sep1": "separator-1-yi.png",
    "sep2": "separator-2-er.png",
    "sep3": "separator-3-san.png",
    "end": "end-the-end.png",
}

FONT = ("'PingFang SC NEW',system-ui,-apple-system,BlinkMacSystemFont,"
        "'Helvetica Neue','Hiragino Sans GB','Microsoft YaHei UI','Microsoft YaHei',"
        "Arial,sans-serif")

# 正文段落样式（除 margin / text-align 外全部继承容器）
P = 'margin:0 16px;'
PC = 'margin:0 16px;text-align:center;'          # 居中：署名、END 后两句
PI = 'margin:0 16px;text-align:center;line-height:0;'  # 图片段落
GLUE = '<strong><br></strong>'


def data_uri(name):
    """把 assets 下的图片读成 base64 data URI。"""
    path = os.path.join(ASSETS, name)
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as fh:
        return "data:%s;base64,%s" % (mime, base64.b64encode(fh.read()).decode("ascii"))


def head_img(name):
    """头图槽位：模板不预置图片，用注释标出位置。"""
    return ('<!-- 【头图】2.35:1（1800×766），放在「作者 | 小铭」之前，'
            '不缩进、居中。把你的图插到这一行下面 -->')


def photo_slot():
    return ('<!-- 【人物图/配图】建议 1080×640 左右，带 16px 边距。'
            '图片段落写法见 README -->')


def build(plain=False):
    src = {} if plain else {k: data_uri(v) for k, v in IMG.items()}

    def img(key, alt=""):
        if plain:
            src[key] = "assets/" + IMG[key]
        return ('<p style="%s"><img src="%s" alt="%s" style="max-width:100%%;'
                'height:auto;display:block;margin:0 auto;"></p>' % (PI, src[key], alt))

    def p(text):
        return '<p style="%s">%s</p>' % (P, text)

    def pc(text):
        return '<p style="%s">%s</p>' % (PC, text)

    def h(text):
        # 层级行：藏蓝加粗，字号不变（仍是 15px）
        return '<p style="%s"><strong><span style="color:#1F4E6E;">%s</span></strong></p>' % (P, text)

    def hc(text):
        # 层级行 + 居中（署名专用）
        return '<p style="%s"><strong><span style="color:#1F4E6E;">%s</span></strong></p>' % (PC, text)

    def gap():
        return '<p style="%s">%s</p>' % (P, GLUE)

    b = []
    a = b.append

    a(head_img("head"))
    a(gap())
    a(hc("作者 | 小铭"))
    a(gap())
    a(p("【① 事实锚点开场】时间 ＋ 机构 ＋ 人数，一句话把新闻摆平，不抒情、不评价。约 40–60 字。"))
    a(gap())
    a(p("【② 悬念】把人物抬到「你好像见过他」的位置。约 40–50 字。"))
    a(gap())
    a(photo_slot())
    a(p("【③ 身份揭示 ＋ 硬数据】本名、网名、关键日期、关键数字，四个锚点全给。约 100–120 字。"))
    a(gap())
    a(img("sep1", "第一章"))
    a(h("【④ 轻问小标题】用一个「这名字怎么来的」式的问句，让人先松下来"))
    a(gap())
    a(p("【本段正文】回答上面那个问句。约 90–120 字。"))
    a(gap())
    a(h("【小标题】爱好/能力的起源"))
    a(gap())
    a(p("【本段正文】从什么具体场景开始、练了多久、在哪里被藏起来。约 250–300 字，可分 2–3 段。"))
    a(gap())
    a(h("【⑥ 反常识转折 —— 全文心脏】「看起来最正确的事，结果最差」"))
    a(gap())
    a(p("【本段正文】先给一句「很多人猜他会一路顺风顺水，其实没有。」约 15 字。"))
    a(gap())
    a(p("【本段正文】他做的那件「最正确的事」，以及随之而来的坏结果。关键数字独立成段。约 80–120 字。"))
    a(gap())
    a(p("【本段正文】他后来那个「看起来像分心」的决定。约 40 字。"))
    a(gap())
    a(p("【本段正文】这个决定为什么反而救了他，用他自己的原话式大白话解释。约 120 字。"))
    a(gap())
    a(p("【本段正文】回正的结果：最终的关键数字（分数/名次/成果）。约 80 字。"))
    a(gap())
    a(img("sep2", "第二章"))
    a(h("【⑦ 作者站出来】一句话把故事掰向读者"))
    a(gap())
    a(p("【本段正文】给一句反常识判断 ＋ 一个大白话比喻。约 80 字。"))
    a(gap())
    a(h("【小标题】方法是怎么找出来的"))
    a(gap())
    a(p("【本段正文】起点要具体到某一天、某个人、某份材料。约 150 字。"))
    a(gap())
    a(p("【本段正文】他提前做了什么功课、摸清了什么。约 80 字。"))
    a(gap())
    a(p("【本段正文】方法论：大多数人是「从热门榜单往下推」，他是「从自己真正投入过的事往回推」。约 130 字。"))
    a(gap())
    a(p("【本段正文】把这条路走宽：这个方向还能去哪些领域，打破大众印象。约 120 字。"))
    a(gap())
    a(img("sep3", "第三章"))
    a(h("【小标题】家长/读者能从这件事里拿走什么"))
    a(gap())
    a(h("第一，【认知纠正】"))
    a(gap())
    a(p("【本段正文】纠正一个流行误解 ＋ 给边界。约 120 字。"))
    a(gap())
    a(h("第二，【可教的方法】"))
    a(gap())
    a(p("【本段正文】读者今天就能照着做的步骤，去哪个官网、查什么。约 120 字。"))
    a(gap())
    a(h("第三，【心态许可】"))
    a(gap())
    a(p("【本段正文】承认不完美，把落点收回人本身。约 120 字。"))
    a(gap())
    a('<p style="%s"><strong>【结尾升维句】一个人在成长路上能为热爱留一方天地，'
      '并把它走成脚下的路，这件事本身就值得被看见。</strong></p>' % P)
    a(img("end", "THE END"))
    a(pc("原创不易，感谢有你！"))
    a(gap())
    a(pc("一起转发出去，让更多人看到。"))

    body = "\n\n  ".join(b)
    doc = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>藏蓝+红 · 章节分隔 —— 公众号排版模板（自包含可复制）</title>
<style>html,body{margin:0;padding:0;background:#E9E9EC;}</style>
</head>
<body>
<!--
  ============================================================
  小铭想 · 排版模板「藏蓝 + 红 · 章节分隔」
  ------------------------------------------------------------
  全部数值来自 2026-09-16 已发文章的内联样式实测，详见 layout-spec.md
  容器    max-width 677px 居中 / 背景 #FFFFFF
  字体    "PingFang SC NEW", system-ui, -apple-system, ...
  正文    15px / 行高 1.75em / 字间距 0.544px / 色 #595959
  层级行  藏蓝 #1F4E6E 加粗（字号不变，仍 15px）
  段边距  margin:0 16px；段间距靠空段 <br> 撑开
  居中    署名 + END 后两句收尾语 + 图片；其余正文左对齐

  用法：浏览器打开 → 全选复制 → 粘进公众号编辑器 → 替换【】里的内容
  图片已 base64 内嵌，复制时不会丢；头图与人物图需你自己插入
  ============================================================
-->
<section style="max-width:677px;margin:0 auto;background:#ffffff;font-family:%s;font-size:15px;letter-spacing:0.544px;line-height:1.75em;color:#595959;padding-bottom:40px;">

  %s

</section>
</body>
</html>
""" % (FONT, body)
    return doc


if __name__ == "__main__":
    plain = "--plain" in sys.argv
    out = os.path.join(HERE, "index.relative.html" if plain else "index.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(build(plain=plain))
    print("已生成 %s（%.1f KB）" % (os.path.basename(out), os.path.getsize(out) / 1024))
