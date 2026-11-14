"""ドット絵（しおり・モンスター・宝箱）を SVG にして index.html の SPRITES に書き込む。
絵を直したいときはこのファイルの文字の絵を書きかえて  python3 tools/sprites.py  を実行する。
"""
import os, re, json, runpy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def svg_from(rows, pal, extra_groups=None):
    h = len(rows); w = len(rows[0])
    for r in rows: assert len(r) == w, (r, len(r), w)
    def rects(grid):
        out = []
        for y, row in enumerate(grid):
            x = 0
            while x < w:
                c = row[x]
                if c == ".": x += 1; continue
                x2 = x
                while x2 < w and row[x2] == c: x2 += 1
                out.append(f'<rect x="{x}" y="{y}" width="{x2-x}" height="1" fill="{pal[c]}"/>')
                x = x2
        return "".join(out)
    body = rects(rows)
    for name, g in (extra_groups or {}).items():
        body += f'<g class="f-{name}">{rects(g)}</g>'
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'shape-rendering="crispEdges" aria-hidden="true">{body}</svg>')

K = "#2a1f3d"
MONSTERS = {
  "haniwa": ("だいおうハニワ", {"K": K, "O": "#e08a55", "o": "#b5653a", "D": "#3b1f14", "Y": "#fde047"}, [
    "....KYKYYKYK....",
    ".....KOOOOOK....",
    "...KKOOOOOOOK...",
    "...KOOOOOOOOK...",
    "...KODDOODDOK...",
    "...KODDOODDOK...",
    "...KOOOOOOOOK...",
    "...KOOODDOOOK...",
    "...KOOODDOOOK...",
    "....KOOOOOOK....",
    ".KK.KOOOOOOK.KK.",
    "KOOKKOOOOOOKKOOK",
    ".KOOOOOOOOOOOOK.",
    "...KoOOOOOOoK...",
    "...KooOOOOooK...",
    "....KKKKKKKK....",
  ]),
  "musha": ("おちむしゃゴースト", {"K": K, "G": "#fbbf24", "H": "#475569", "W": "#f1f5f9", "w": "#cbd5e1", "E": "#1e1b4b", "M": "#be123c"}, [
    "...G........G...",
    "...GG......GG...",
    "....GGKKKKGG....",
    "...KHHHHHHHHK...",
    "..KHHHHHHHHHHK..",
    ".KHHHHHHHHHHHHK.",
    "..KWWWWWWWWWWK..",
    "..KWWEEWWEEWWK..",
    "..KWWEEWWEEWWK..",
    "..KWWWWWWWWWWK..",
    "..KWWWWMMWWWWK..",
    "..KWWWWWWWWWWK..",
    "..KwWWWWWWWWwK..",
    "..KwwWWWWWWwwK..",
    "..KwKwwKKwwKwK..",
    "...K.KK..KK.K...",
  ]),
  "chochin": ("ちょうちんおばけ", {"K": K, "B": "#1f2937", "L": "#fca5a5", "l": "#ef4444", "W": "#ffffff", "E": "#1e1b4b", "T": "#f472b6"}, [
    "......KKKK......",
    ".....KBBBBK.....",
    "....KKKKKKKK....",
    "...KLLLLLLLLK...",
    "..KllllllllllK..",
    "..KLWWWWLLLLLK..",
    "..KlWWEEWllllK..",
    "..KLWWEEWLLLLK..",
    "..KlWWWWlllllK..",
    "..KLLLLLLLLLLK..",
    "..KllKKKKKlllK..",
    "..KLLKTTTKLLLK..",
    "...KlllTTlllK...",
    "....KKKKTTKK....",
    ".....KBBTTBK....",
    "......KKKKK.....",
  ]),
  "robo": ("じょうきロボ", {"K": K, "S": "#94a3b8", "s": "#64748b", "Y": "#fde047", "R": "#ef4444", "W": "#e2e8f0"}, [
    "..WW......WW....",
    ".WWW..KKKK.WWW..",
    "..W..KRRRRK..W..",
    "...KKKKKKKKKK...",
    "..KSSSSSSSSSSK..",
    "..KSYYSSSSYYSK..",
    "..KSYYSSSSYYSK..",
    "..KSSSSSSSSSSK..",
    "..KSsKKKKKKsSK..",
    "..KSsKsKsKsKSK..",
    "..KKKKKKKKKKKK..",
    "KK.KssSSSSssK.KK",
    "KSKKsSSRRSSsKKSK",
    ".KK.KsSSSSsK.KK.",
    "....KsK..KsK....",
    "...KKKK..KKKK...",
  ]),
  "tv": ("テレビまじん", {"K": K, "C": "#fb923c", "G": "#67e8f9", "E": "#1e1b4b", "Y": "#fde047"}, [
    "...K........K...",
    "....K......K....",
    ".....K....K.....",
    "......K..K......",
    "..KKKKKKKKKKKK..",
    ".KCCCCCCCCCCCCK.",
    ".KCKKKKKKKKCCCK.",
    ".KCKGGGGGGKCYCK.",
    ".KCKGEGGEGKCCCK.",
    ".KCKGGGGGGKCYCK.",
    ".KCKGEEEEGKCCCK.",
    ".KCKGGGGGGKCCCK.",
    ".KCKKKKKKKKCCCK.",
    ".KCCCCCCCCCCCCK.",
    "..KKKKKKKKKKKK..",
    "...KK......KK...",
  ]),
  "book": ("れきしの まどうしょ", {"K": K, "P": "#7c3aed", "Y": "#fbbf24", "W": "#fff7ed", "E": "#be123c", "R": "#9f1239"}, [
    "................",
    "..KKKKKKKKKKKK..",
    ".KPPPPPPPPPPPPK.",
    ".KPYPPPPPPPPYPK.",
    ".KPPPKKKKKKPPPK.",
    ".KPPKWWWWWWKPPK.",
    ".KPPKWWEEWWKPPK.",
    ".KPPKWWEEWWKPPK.",
    ".KPPPKKKKKKPPPK.",
    ".KPPPPPPPPPPPPK.",
    ".KWWWWWWWWWWWWK.",
    ".KWKWKWKWKWKWWK.",
    ".KRRRRRRRRRRRRK.",
    ".KWKWKWKWKWKWWK.",
    ".KPPPPPPPPPPPPK.",
    "..KKKKKKKKKKKK..",
  ]),
}

CHEST_PAL = {"K": K, "B": "#c2410c", "b": "#7c2d12", "Y": "#fbbf24", "W": "#fffbeb"}
CHEST = [
  ".KKKKKKKKKK.",
  "KbBBBBBBBBbK",
  "KBBBBBBBBBBK",
  "KYYYYYYYYYYK",
  "KBBBBYYBBBBK",
  "KbBBBYKBBBbK",
  "KBBBBBBBBBBK",
  "KYYYYYYYYYYK",
  "KbBBBBBBBBbK",
  "KKKKKKKKKKKK",
]
CHEST_OPEN = [
  ".KKKKKKKKKK.",
  "KbBBBBBBBBbK",
  "KYYYYYYYYYYK",
  "KWYWYWYWYWYK",
  "KYWYWYWYWYWK",
  "KbBBBYYBBBbK",
  "KBBBBBBBBBBK",
  "KYYYYYYYYYYK",
  "KbBBBBBBBBbK",
  "KKKKKKKKKKKK",
]

# しおり（char_src.py が /tmp に書き出す SVG を使う）
ns = runpy.run_path(os.path.join(ROOT, "tools", "char_src.py"))
char_svg = open("/tmp/px/char.svg").read()

sprites = {"char": char_svg, "chest": svg_from(CHEST, CHEST_PAL), "chestOpen": svg_from(CHEST_OPEN, CHEST_PAL)}
names = {}
for key, (name, pal, rows) in MONSTERS.items():
    sprites[key] = svg_from(rows, pal); names[key] = name

js = "/* SPRITES:BEGIN（tools/sprites.py が自動生成。手で書きかえない） */\nconst SPRITES = " + json.dumps(sprites, ensure_ascii=False) + \
     ";\nconst MONSTER_NAMES = " + json.dumps(names, ensure_ascii=False) + ";\n/* SPRITES:END */"
p = os.path.join(ROOT, "index.html")
s = open(p, encoding="utf-8").read()
s, n = re.subn(r"/\* SPRITES:BEGIN.*?/\* SPRITES:END \*/", lambda m: js, s, flags=re.S)
if n != 1: raise SystemExit("index.html に SPRITES の目印が見つかりません")
open(p, "w", encoding="utf-8").write(s)

# 確認用のプレビュー画像
try:
    from PIL import Image
    import io, subprocess
except ImportError:
    pass
print("ok:", ", ".join(sprites))
