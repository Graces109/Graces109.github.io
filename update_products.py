# -*- coding: utf-8 -*-
"""
Yuexin Lighting — 产品自动导入脚本
=================================
扫描 L:\\2018.3.20FTTX资料\\ 下的产品文件夹，把新产品自动加入 products.json 并压缩产品图。

用法（在网站根目录 template\\alstar-main 下运行）：
    python update_products.py                # 扫描并更新 products.json + 压缩图片
    python update_products.py --dry-run      # 只扫描预览，不改动

工作方式：
1. 遍历 L 盘各分类文件夹下的每个产品文件夹。
2. 从文件夹名提取型号（YX-XXX）和产品名。
3. 从产品文件夹里的子目录（优先 "6. 原图" 或 "1. 岳鑫水印"，否则任一图片）挑一张主图。
4. 压缩主图到 assets/img/products/<model>.jpg（800x600，白底，<80KB）。
5. 把新产品追加进 assets/data/products.json（已存在的型号跳过，不覆盖）。

添加新产品流程：
  A. 把产品图放进 L 盘对应分类文件夹（与现有产品文件夹同结构）。
  B. 运行本脚本（或在豆包里说"更新产品"），它会自动把新产品加进网站。
  C. push 上线后，网站右侧 Product Overview 自动显示新产品。

注意：产品名 / 型号解析只识别 "YX-XXX" 格式。其它命名需手动在 products.json 补充。
"""
import os
import re
import sys
import json
from PIL import Image

L_ROOT = r"L:\2018.3.20FTTX资料"
SITE = os.path.dirname(os.path.abspath(__file__))
PROD_DIR = os.path.join(SITE, "assets", "img", "products")
DATA_JSON = os.path.join(SITE, "assets", "data", "products.json")

# 分类文件夹前缀 -> 英文一级类目
CAT_MAP = {
    "1. 摇头灯": "Moving Head Light",
    "2. 帕灯": "LED Wash Light",
    "3. 投光灯": "LED Wash Light",
    "4. 效果灯": "LED Effect Light",
    "5. 激光灯": "LED Laser Light",
    "6. 烟雾机": "Fog Machine",
    "7. 影视灯": "LED Movies Light",
    "8. 显示屏": "LED Effect Light",
    "9.控制台": "DMX Console",
    "10.追光灯": "Follow Spot Light",
    "14.配件": "Accessories",
}

# 优先取图的子目录名（按优先级）
PREF_DIRS = ["6. 原图", "1. 岳鑫水印", "原图", "图片"]

MODEL_RE = re.compile(r"(YX-?[A-Za-z0-9\-]+)", re.IGNORECASE)


def pick_image(product_dir):
    """从产品文件夹里挑一张主图，返回绝对路径或 None。"""
    # 按优先级选子目录
    for pref in PREF_DIRS:
        d = os.path.join(product_dir, pref)
        if os.path.isdir(d):
            for f in sorted(os.listdir(d)):
                if f.lower().endswith((".jpg", ".jpeg", ".png")):
                    return os.path.join(d, f)
    # 退回：直接扫描文件夹下所有图片，优先主效果图（含 model / d 之类）
    imgs = []
    for f in sorted(os.listdir(product_dir)):
        if f.lower().endswith((".jpg", ".jpeg", ".png")):
            imgs.append(os.path.join(product_dir, f))
    if imgs:
        return imgs[0]
    return None


def process_image(src, model):
    """压缩图片到 800x600 白底，返回保存路径。"""
    os.makedirs(PROD_DIR, exist_ok=True)
    out = os.path.join(PROD_DIR, model.lower() + ".jpg")
    img = Image.open(src).convert("RGB")
    w, h = img.size
    # 白底，等比缩放居中，保留产品全貌
    W, H = 800, 600
    bg = Image.new("RGB", (W, H), (255, 255, 255))
    scale = min((W - 40) / w, (H - 40) / h)
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
    img2 = img.resize((nw, nh), Image.LANCZOS)
    bg.paste(img2, ((W - nw) // 2, (H - nh) // 2))
    for q in (80, 75, 70, 65, 60):
        bg.save(out, "JPEG", quality=q, optimize=True)
        if os.path.getsize(out) < 80000:
            break
    return out


def main():
    dry = "--dry-run" in sys.argv
    if not os.path.isdir(L_ROOT):
        print(f"L 盘目录不存在: {L_ROOT}")
        return

    # 读取现有 products.json
    existing = {}
    if os.path.isfile(DATA_JSON):
        with open(DATA_JSON, "r", encoding="utf-8") as f:
            for p in json.load(f):
                existing[p["model"].lower()] = p

    found_new = 0
    for cat_dir in os.listdir(L_ROOT):
        cat_path = os.path.join(L_ROOT, cat_dir)
        if not os.path.isdir(cat_path):
            continue
        cat_en = None
        for prefix, en in CAT_MAP.items():
            if cat_dir.startswith(prefix):
                cat_en = en
                break
        for prod in os.listdir(cat_path):
            pdir = os.path.join(cat_path, prod)
            if not os.path.isdir(pdir):
                continue
            m = MODEL_RE.search(prod)
            if not m:
                continue
            raw_model = m.group(1).upper()          # 保留原始格式，如 YX-MHQ1000
            model = raw_model
            # 兼容 products.json 现有 model（可能去连字符）
            key = model.lower()
            if key in existing or model in existing:
                continue
            src = pick_image(pdir)
            if not src:
                print(f"  [跳过] 无图片: {prod}")
                continue
            # 产品名 = 文件夹名去掉型号部分，清理首尾分隔符
            name = prod.replace(raw_model, "").replace("YX-" + raw_model, "").strip(" -–—")
            print(f"  [新增] {model}  {name}  ({cat_dir})")
            found_new += 1
            if dry:
                continue
            out = process_image(src, model)
            existing[model] = {
                "model": model,
                "name": name,
                "category": cat_en or "",
                "img": os.path.join("assets", "img", "products", os.path.basename(out)).replace("\\", "/"),
            }

    print(f"\n共发现新模型: {found_new}")
    if dry:
        print("(--dry-run 模式，未写入)")
        return

    if found_new:
        # 保持原顺序：现有产品在前，新追加在后
        merged = list(existing.values())
        with open(DATA_JSON, "w", encoding="utf-8") as f:
            json.dump(merged, f, ensure_ascii=False, indent=2)
        print(f"已更新 products.json: {len(merged)} 个产品")
    else:
        print("没有新产品需要更新。")


if __name__ == "__main__":
    main()
