import sys, os, glob, io
from fontTools.ttLib import TTFont
from fontTools import subset
from fontTools.merge import Merger
text = open('/home/claude/jjuni5885-commits/mongle-farm/index.html', encoding='utf8').read() + open('en.tsv', encoding='utf8').read()
chars = set(ch for ch in text if 0xAC00 <= ord(ch) <= 0xD7A3 or 0x3131 <= ord(ch) <= 0x318E or ord(ch) in (0xB7, 0x2026, 0x2192, 0xD7, 0x20A9, 0x2605, 0x2764)) | set(chr(c) for c in range(32, 127))
print('chars', len(chars))
def opts():
    o = subset.Options(); o.flavor = None; o.layout_features = ['*']; o.name_IDs = ['*']; o.name_languages = ['*']; o.notdef_outline = True; o.drop_tables = []
    return o
files = sorted(glob.glob('/home/claude/work/tools/node_modules/@fontsource/jua/files/*-400-normal.woff2'))
tmp = '/tmp/mgjua'; os.makedirs(tmp, exist_ok=True); parts, have = [], set()
for i, f in enumerate(files):
    ft = TTFont(f); cmap = ft.getBestCmap() or {}
    need = [ch for ch in chars if ord(ch) in cmap and ch not in have]
    if not need: continue
    have |= set(need); s = subset.Subsetter(opts()); s.populate(text=''.join(need)); s.subset(ft)
    p = os.path.join(tmp, '%03d.ttf' % i); ft.flavor = None; ft.save(p); parts.append(p)
print('pieces', len(parts), 'missing', ''.join(sorted(ch for ch in chars if ch not in have and ord(ch) > 32)))
m = Merger().merge(parts); m.flavor = 'woff2'; bio = io.BytesIO(); m.save(bio)
open('jua_sub.woff2', 'wb').write(bio.getvalue()); print('bytes', len(bio.getvalue()))
