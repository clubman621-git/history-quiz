"""ドットフォント（DotGothic16, SIL OFL）から、アプリで使う文字だけを抜き出して fonts/dot.woff2 を作る。
問題を追加して新しい漢字が増えたときに実行する。
  npm pack @fontsource/dotgothic16 && tar xzf fontsource-dotgothic16-*.tgz
  python3 tools/make-font.py package/files
（必要: pip install fonttools brotli）
"""
import sys, glob, os
from fontTools.ttLib import TTFont
from fontTools import subset
from fontTools.merge import Merger

src = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
text = open(os.path.join(root, "index.html"), encoding="utf-8").read()
extra = "".join(chr(c) for c in range(0x20, 0x7f))           # 英数字・記号
extra += "".join(chr(c) for c in range(0x3000, 0x3100))      # 句読点・ひらがな・カタカナ
extra += "".join(chr(c) for c in range(0xff01, 0xff5f))      # 全角英数字
extra += "■□▷◆★☆◎○×♥♪…〜・「」『』（）！？"
chars = set(text + extra)

parts = []
for i, f in enumerate(sorted(glob.glob(os.path.join(src, "dotgothic16-*-400-normal.woff")))):
    font = TTFont(f)
    have = set(chr(c) for c in font.getBestCmap())
    need = chars & have
    if not need:
        continue
    opts = subset.Options(); opts.notdef_outline = True; opts.name_IDs = ["*"]; opts.layout_features = ["*"]
    sub = subset.Subsetter(opts); sub.populate(text="".join(need)); sub.subset(font)
    out = f"/tmp/dot-part-{i}.ttf"; font.flavor = None; font.save(out); parts.append(out)
    chars -= need

merged = Merger().merge(parts)
merged.flavor = "woff2"
merged.save(os.path.join(root, "fonts", "dot.woff2"))
print("parts:", len(parts), "missing:", "".join(sorted(c for c in chars if not c.isspace()))[:200])
