"""人物カードの肖像ドット絵（24×24）を、特徴の組み合わせで作る。
sprites.py から読みこまれる。人物を足すときは PEOPLE に1行足す。
"""
W = H = 24
K = "#2a1f3d"
SKIN, SKIN_S = "#ffe4cf", "#f0c3a6"
HAIR, HAIR_H = "#1c1a26", "#4a4560"

# 名前: (かみがた・かぶりもの, ひげ, ふく, ふくの色, もちもの, オプション)
PEOPLE = {
  "卑弥呼":               ("female", None, "miko", "#dc2626", "magatama", {}),
  "聖徳太子":             ("kanmuri", "mustache", "sokutai", "#7f1d1d", "shaku", {}),
  "小野妹子":             ("kanmuri", None, "sokutai", "#1d4ed8", "shaku", {}),
  "中大兄皇子":           ("kanmuri", None, "sokutai", "#6d28d9", "shaku", {}),
  "大海人皇子（天武天皇）": ("kanmuri", "beard", "sokutai", "#a16207", "shaku", {}),
  "聖武天皇":             ("kanmuri", "mustache", "sokutai", "#ca8a04", "shaku", {}),
  "桓武天皇":             ("kanmuri", "fullbeard", "sokutai", "#b91c1c", "shaku", {}),
  "菅原道真":             ("kanmuri", "fullbeard", "sokutai", "#1f2937", "ume", {}),
  "藤原道長":             ("kanmuri", "mustache", "sokutai", "#1f2937", "moon", {}),
  "白河上皇":             ("monk", None, "monk", "#6b21a8", None, {}),
  "平清盛":               ("monk", None, "monk", "#b91c1c", None, {"fat": True}),
  "源頼朝":               ("kanmuri", "mustache", "sokutai", "#111827", "shaku", {}),
  "北条泰時":             ("eboshi", None, "kimono", "#15803d", None, {}),
  "北条時宗":             ("eboshi", None, "armor", "#b91c1c", None, {}),
  "足利尊氏":             ("eboshi", "mustache", "armor", "#1f2937", None, {}),
  "足利義満":             ("monk", None, "monk", "#ca8a04", "gold", {}),
  "足利義政":             ("eboshi", None, "kimono", "#94a3b8", None, {}),
  "フランシスコ・ザビエル": ("tonsure", "fullbeard", "priest", "#111827", "cross", {"west": True}),
  "織田信長":             ("chasen", "mustache", "kataginu", "#166534", None, {}),
  "豊臣秀吉":             ("kanmuri", "beard", "sokutai", "#b45309", "gourd", {"thin": True}),
  "徳川家康":             ("chonmage", None, "kataginu", "#78350f", None, {"fat": True}),
  "徳川家光":             ("chonmage", None, "kataginu", "#1d4ed8", None, {}),
  "天草四郎":             ("young", None, "ruff", "#e5e7eb", "cross", {}),
  "徳川吉宗":             ("chonmage", None, "kataginu", "#1e3a8a", None, {}),
  "松平定信":             ("chonmage", None, "kataginu", "#047857", None, {}),
  "水野忠邦":             ("chonmage", None, "kataginu", "#4b5563", None, {}),
  "ペリー":               ("curlwhite", None, "uniform", "#1e3a8a", None, {"west": True}),
  "井伊直弼":             ("chonmage", None, "kataginu", "#7f1d1d", None, {}),
  "徳川慶喜":             ("chonmage", None, "kataginu", "#5b21b6", None, {}),
  "西郷隆盛":             ("short", None, "kimono", "#1f2937", None, {"fat": True, "brows": True}),
  "伊藤博文":             ("western", "fullbeard", "suit", "#111827", None, {"gray": True}),
  "陸奥宗光":             ("western", "mustache", "suit", "#111827", None, {}),
  "小村寿太郎":           ("western", "mustache", "suit", "#111827", None, {}),
  "吉田茂":               ("bald", "mustache", "suit", "#111827", "glasses", {"gray": True}),
}

def shade(hexc, f):
    r, g, b = (int(hexc[i:i+2], 16) for i in (1, 3, 5))
    c = lambda v: max(0, min(255, int(v * f)))
    return "#%02x%02x%02x" % (c(r), c(g), c(b))

def portrait(name):
    hair, facial, cloth, col, item, opt = PEOPLE[name]
    g = [[None] * W for _ in range(H)]
    def put(x, y, c):
        if 0 <= x < W and 0 <= y < H: g[y][x] = c
    def ell(cx, cy, rx, ry, c):
        for y in range(H):
            for x in range(W):
                if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1: put(x, y, c)
    skin = "#f6d2b8" if opt.get("west") else SKIN
    hcol = "#d1d5db" if opt.get("gray") else HAIR
    c1, c0 = col, shade(col, .7)
    # --- からだ（ふく）---
    for y in range(17, 24):
        hw = 7 + min(y - 17, 3) + (1 if opt.get("fat") else 0)
        for x in range(12 - hw, 12 + hw):
            put(x, y, c1 if x < 12 + hw - 3 else c0)
    if cloth == "sokutai":   # まるい えり
        for x in range(9, 15): put(x, 17, c0)
        for x in range(10, 14): put(x, 18, c0)
    if cloth in ("kimono", "kataginu", "monk", "armor"):  # Vの えり（白い した ぎ）
        for i, y in enumerate(range(17, 21)):
            put(10 + i, y, "#f8fafc"); put(13 - i, y, "#f8fafc")
    if cloth == "kataginu":  # かたぎぬ（かたが はった）
        for y in (17, 18):
            for x in list(range(2, 7)) + list(range(17, 22)): put(x, y, c1 if x < 17 else c0)
    if cloth == "monk":      # けさ
        for i in range(7): put(14 + i // 2, 17 + i, "#ca8a04")
    if cloth == "armor":
        for y in range(18, 24):
            for x in (4, 5, 18, 19): put(x, y, "#fbbf24" if y % 2 else c0)
        for x in range(8, 16): put(x, 21, "#fbbf24")
    if cloth == "miko":
        for y in range(17, 24):
            for x in range(4, 20): put(x, y, "#f8fafc" if 8 <= x <= 15 else c1)
    if cloth == "suit":
        for i, y in enumerate(range(17, 24)):
            for x in range(10, 14): put(x, y, "#f8fafc")
        for y in range(18, 23): put(11, y, "#b91c1c"); put(12, y, "#b91c1c")
        for i, y in enumerate(range(17, 21)): put(9 + i, y, c0); put(14 - i, y, c0)
    if cloth == "uniform":
        for y in range(18, 24): put(12, y, "#fbbf24") if y % 2 else None
        for x in list(range(3, 7)) + list(range(17, 21)): put(x, 18, "#fbbf24")
        for x in range(10, 14): put(x, 17, "#f8fafc")
    if cloth == "priest":
        for x in range(10, 14): put(x, 17, "#f8fafc")
    if cloth == "ruff":
        for x in range(6, 18): put(x, 17, "#ffffff"); put(x, 18, "#e5e7eb" if x % 2 else "#ffffff")
        for y in range(19, 24):
            for x in range(4, 20): put(x, y, "#f1f5f9" if x < 15 else "#cbd5e1")
    # --- くび・かお ---
    for y in range(14, 18):
        for x in range(10, 14): put(x, y, SKIN_S)
    rx = 5.6 if opt.get("fat") else (4.6 if opt.get("thin") else 5)
    ell(12, 11, rx, 5.6, skin)
    for y in range(6, 17):
        for x in range(13, 18):
            if g[y][x] == skin and x >= 15: g[y][x] = SKIN_S if not opt.get("west") else "#e8b99c"
    # --- かみ・かぶりもの ---
    if hair in ("kanmuri", "eboshi", "chonmage", "chasen", "short", "western", "young", "female"):
        for x in range(7, 17):
            for y in range(5, 8):
                if ((x + .5 - 12) / 5.2) ** 2 + ((y + .5 - 9) / 4) ** 2 <= 1: put(x, y, hcol)
        for y in range(8, 12): put(7, y, hcol); put(16, y, hcol)
    if hair == "kanmuri":
        for y in range(2, 6):
            for x in range(9, 15): put(x, y, "#111827")
        for y in range(0, 3): put(13, y, "#111827"); put(14, y, "#374151")
        put(10, 3, "#374151")
    if hair == "eboshi":
        for y in range(0, 6):
            for x in range(8 + (5 - y) // 2, 15 + (5 - y) // 3): put(x, y, "#111827")
        put(10, 2, "#374151"); put(11, 1, "#374151")
    if hair == "chonmage":
        for y in range(5, 8):
            for x in range(9, 15): put(x, y, "#c7d2fe" if y < 7 else hcol)   # そりあげ（さかやき）
        for x in range(10, 14): put(x, 4, hcol)
        put(11, 3, hcol); put(12, 3, hcol)
    if hair == "chasen":
        for y in range(5, 7):
            for x in range(9, 15): put(x, y, "#c7d2fe")
        for y in range(0, 5): put(11, y, hcol); put(12, y, hcol)
        put(10, 0, hcol); put(13, 0, hcol); put(12, 4, "#f8fafc")
    if hair == "monk":
        ell(12, 9, 5, 4.2, skin)
        for x in range(10, 13): put(x, 6, "#ffffff")
    if hair == "tonsure":
        ell(12, 8.5, 5.4, 4, "#a16207")
        ell(12, 7, 3, 2, skin)
    if hair == "curlwhite":
        for (cx, cy) in [(8, 8), (16, 8), (7, 11), (17, 11), (9, 5.5), (15, 5.5), (12, 5)]:
            ell(cx, cy, 2.2, 2, "#f1f5f9")
        for y in range(11, 15): put(7, y, "#e2e8f0"); put(17, y, "#e2e8f0")   # もみあげ
    if hair == "western":
        for x in range(7, 17): put(x, 6, hcol)
        for x in range(7, 11): put(x, 7, hcol)
        put(12, 6, skin)
    if hair == "bald":
        ell(12, 9, 5, 4.5, skin)
        for y in range(9, 13): put(7, y, "#e5e7eb"); put(16, y, "#e5e7eb")
    if hair == "short":
        for x in range(7, 17): put(x, 7, hcol)
    if hair == "young":
        for x in range(7, 17):
            for y in range(7, 9): put(x, y, hcol)
        for y in range(9, 14): put(6, y, hcol); put(17, y, hcol)
    if hair == "female":
        for y in range(8, 22):
            for x in (5, 6, 17, 18): put(x, y, hcol)
        for x in range(7, 17): put(x, 7, hcol)
        for x in range(8, 16, 2): put(x, 6, "#22c55e")   # かみかざり
    # --- め・まゆ・くち ---
    put(10, 11, K); put(14, 11, K)
    put(10, 10, K if not opt.get("brows") else K); put(14, 10, K)
    if opt.get("brows"):
        for x in (9, 10, 11, 13, 14, 15): put(x, 9, K)
    else:
        put(9, 9, K); put(10, 9, K); put(14, 9, K); put(15, 9, K)
    put(12, 13, SKIN_S)
    put(11, 15, "#b45353"); put(12, 15, "#b45353")
    if name == "卑弥呼":
        put(9, 13, "#fbb6ce"); put(15, 13, "#fbb6ce")
    # --- ひげ ---
    fcol = "#e5e7eb" if opt.get("gray") else HAIR
    if facial == "mustache":
        for x in (10, 11, 13, 14): put(x, 14, fcol)
    if facial in ("beard", "fullbeard"):
        put(12, 17, fcol); put(11, 17, fcol); put(12, 16, fcol)
    if facial == "fullbeard":
        for x in (10, 11, 13, 14): put(x, 14, fcol)
        for y in range(13, 18):
            for x in range(8, 17):
                if g[y][x] in (skin, SKIN_S, "#e8b99c") and not (10 <= x <= 14 and y <= 15 and y >= 15): pass
        for (x, y) in [(8,13),(9,14),(9,15),(10,16),(11,16),(13,16),(14,16),(15,15),(15,14),(16,13),(11,17),(12,17),(13,17),(12,18)]:
            put(x, y, fcol)
    if item == "glasses":
        for (x, y) in [(9,11),(11,11),(10,10),(10,12),(13,11),(15,11),(14,10),(14,12)]: put(x, y, "#475569")
        put(12, 11, "#475569")
    # --- もちもの（右下）---
    if item == "shaku":
        for y in range(18, 24): put(12, y, "#e7d3a1")
    if item == "magatama":
        for x in range(8, 16): put(x, 18, "#16a34a" if x % 3 else "#fbbf24")
    if item == "cross":
        for y in range(18, 23): put(12, y, "#fbbf24")
        for x in range(11, 14): put(x, 19, "#fbbf24")
    if item == "ume":
        for (x, y) in [(20,3),(19,4),(20,4),(21,4),(20,5)]: put(x, y, "#f472b6")
        put(20, 4, "#fde047")
    if item == "moon":
        for (x, y) in [(19,2),(20,2),(18,3),(18,4),(19,5),(20,5),(21,3),(21,4)]: put(x, y, "#fde047")
        put(19, 3, "#fde047"); put(19, 4, "#fde047"); put(20, 3, "#fde047"); put(20, 4, "#fde047")
    if item == "gourd":
        for (x, y) in [(20,18),(19,19),(20,19),(21,19),(20,20),(19,21),(20,21),(21,21),(19,22),(20,22),(21,22)]: put(x, y, "#fbbf24")
    if item == "gold":
        for (x, y) in [(20,2),(19,3),(20,3),(21,3),(20,4)]: put(x, y, "#fde047")
    # --- りんかく ---
    out = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] is None:
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    X, Y = x + dx, y + dy
                    if 0 <= X < W and 0 <= Y < H and g[Y][X] is not None and g[Y][X] != "#fde047" and g[Y][X] != "#f472b6":
                        out[y][x] = K; break
    return out

def svg(grid):
    parts = []
    for y, row in enumerate(grid):
        x = 0
        while x < W:
            c = row[x]
            if c is None: x += 1; continue
            x2 = x
            while x2 < W and row[x2] == c: x2 += 1
            parts.append(f'<rect x="{x}" y="{y}" width="{x2-x}" height="1" fill="{c}"/>')
            x = x2
    return f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" shape-rendering="crispEdges" aria-hidden="true">{"".join(parts)}</svg>'

def all_svgs():
    return {name: svg(portrait(name)) for name in PEOPLE}

if __name__ == "__main__":
    from PIL import Image
    names = list(PEOPLE)
    cols = 7; sc = 6; pad = 8
    rows = (len(names) + cols - 1) // cols
    out = Image.new("RGB", (cols * (W * sc + pad) + pad, rows * (H * sc + pad) + pad), (233, 220, 255))
    for i, n in enumerate(names):
        grid = portrait(n)
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); px = im.load()
        for y in range(H):
            for x in range(W):
                c = grid[y][x]
                if c: px[x, y] = tuple(int(c[j:j+2], 16) for j in (1, 3, 5)) + (255,)
        im = im.resize((W * sc, H * sc), Image.NEAREST)
        out.paste(im, (pad + (i % cols) * (W * sc + pad), pad + (i // cols) * (H * sc + pad)), im)
    out.save("/tmp/portraits.png")
