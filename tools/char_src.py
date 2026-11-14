import os
import math, json, sys
W,H=32,36
PAL={"K":"#2a1f3d","H":"#1c1a26","h":"#4a4560","S":"#ffeee6","s":"#f3d2c6",
     "Y":"#fbbf24","y":"#b45309","Z":"#fde68a","E":"#4c2a85","e":"#a78bfa","W":"#ffffff","B":"#fbb6ce","M":"#c0567a",
     "D":"#f472b6","d":"#db2777","X":"#fbcfe8","A":"#e2e8f0","a":"#94a3b8","Q":"#64748b","J":"#3b82f6","R":"#e11d48",
     "T":"#93c5fd","p":"#f9a8d4","U":"#7c2d12"}
def blank(): return [["." for _ in range(W)] for _ in range(H)]
g=blank()
def put(x,y,c,grid=None):
    grid=grid or g
    if 0<=x<W and 0<=y<H: grid[y][x]=c
def ell(cx,cy,rx,ry,c,cond=lambda x,y:True):
    for y in range(H):
        for x in range(W):
            if ((x+.5-cx)/rx)**2+((y+.5-cy)/ry)**2<=1 and cond(x,y): put(x,y,c)
# back hair (long)
ell(16,15,12.5,12,"H")
for y in range(15,30):
    for x in range(4,28):
        if y<29 or 6<=x<=25: put(x,y,"H")
# ponytail (upper right, sticking out)
for (cx,cy,rx,ry) in [(27,5,3,2.6),(29.5,8,2.4,3),(30.5,12,1.6,3)]:
    ell(cx,cy,rx,ry,"H")
for x,y in [(28,6),(29,7),(30,9)]: put(x,y,"h")
for x,y in [(25,3),(26,3),(25,4),(26,4),(24,2),(27,2)]: put(x,y,"D")
put(25,3,"d")
# pink cape behind shoulders
for y in range(26,36):
    w=10+min(y-26,4)
    for x in range(16-w,16+w):
        if g[y][x]==".": put(x,y,"d" if abs(x-15.5)>w-2 else "D")
# skirt/tunic pink under armor
for y in range(28,36):
    w=8+min(y-28,3)
    for x in range(16-w,16+w): put(x,y,"D" if abs(x-15.5)<w-2 else "d")
# breastplate (silver)
for y in range(28,35):
    w=6 if y<33 else 5
    for x in range(16-w,16+w):
        put(x,y,"A" if x<16 else "a")
for x in range(10,22): put(x,28,"Q")
for x,y in [(15,30),(16,30),(15,31),(16,31)]: put(x,y,"Y")
put(15,30,"J"); put(16,31,"J")
for x in range(11,21): put(x,34,"Y")
# pauldrons
for cx in (7,24):
    for y in range(26,31):
        for x in range(cx,cx+7):
            if ((x-cx-3)/3.6)**2+((y-28.2)/2.4)**2<=1: put(x,y,"A" if y<28 else "a")
    for x in range(cx+1,cx+6): put(x,30,"Y")
# necklace + gem
for x in range(13,19): put(x,30,"Y")
put(15,31,"J"); put(16,31,"J")
# neck
for y in range(24,28):
    for x in range(14,18): put(x,y,"s" if y==24 else "S")
# face
ell(16,17.5,9,8,"S")
# bangs
bang=[2,3,4,3,2,3,5,4,3,2,3,4,3,2,3,4,3,2]
for x in range(7,25):
    bot=10+bang[x-7]
    for y in range(4,bot+1):
        if g[y][x] in "S.H": put(x,y,"H")
# hair highlight arc
for x,y in [(11,6),(12,5),(13,5),(14,5),(15,5)]: put(x,y,"h")
# circlet (silver with gold rim + gem)
for x in range(9,23): put(x,8,"A"); put(x,9,"Y")
for x,y in [(15,7),(16,7),(14,8),(17,8)]: put(x,y,"A")
put(15,8,"R"); put(16,8,"R")
for x,y in [(8,7),(7,6),(8,8)]: put(x,y,"A")   # wing ornament left
for x,y in [(23,7),(24,6),(23,8)]: put(x,y,"A")
# sword held upright at left side
for y in range(11,30): put(2,y,"A"); put(3,y,"a")
put(2,10,"A")
for x in range(0,6): put(x,30,"Y")
put(0,30,"y"); put(5,30,"y")
for y in (31,32): put(2,y,"U"); put(3,y,"U")
put(2,33,"Y"); put(3,33,"Y")
for x,y in [(1,31),(4,31),(1,32),(4,32)]: put(x,y,"S")
# blush
for x in (9,10,21,22): put(x,21,"B")
base=[r[:] for r in g]
# outline silhouette
def outline(grid):
    out=[r[:] for r in grid]
    for y in range(H):
        for x in range(W):
            if grid[y][x]==".":
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    X,Y=x+dx,y+dy
                    if 0<=X<W and 0<=Y<H and grid[Y][X]!=".": out[y][x]="K"; break
    return out
base=outline(base)
faces={}
def face(name, pts):
    f=blank()
    for x,y,c in pts: put(x,y,c,f)
    faces[name]=f
normal=[]
EYE=[".EE.","EWEE","EEEE","EeeE",".ee."]
for ex in (9,19):
    for dy,row in enumerate(EYE):
        for dx,c in enumerate(row):
            if c!=".": normal.append((ex+dx,15+dy,c))
normal+=[(8,15,"K"),(23,15,"K")]
normal+=[(14,21,"M"),(15,22,"M"),(16,22,"M"),(17,21,"M")]
face("normal",normal)
happy=[]
for ex in (9,19):
    happy+=[(ex,18,"E"),(ex+1,17,"E"),(ex+2,17,"E"),(ex+3,18,"E")]
happy+=[(14,21,"M"),(15,21,"M"),(16,21,"M"),(17,21,"M"),(15,22,"M"),(16,22,"M")]
happy+=[(1,7,"Z"),(0,8,"Z"),(1,8,"Z"),(2,8,"Z"),(1,9,"Z"),(4,6,"W"),(27,14,"p"),(26,15,"p"),(27,15,"p"),(28,15,"p"),(27,16,"p")]
face("happy",happy)
oops=[]
for (x,y) in [(10,16),(11,17),(12,18),(11,19),(10,20)]: oops.append((x,y,"E"))
for (x,y) in [(22,16),(21,17),(20,18),(21,19),(22,20)]: oops.append((x,y,"E"))
oops+=[(14,22,"M"),(15,21,"M"),(16,22,"M"),(17,21,"M"),(25,11,"T"),(25,12,"T"),(24,12,"T")]
face("oops",oops)

def rects(grid):
    out=[]
    for y in range(H):
        x=0
        while x<W:
            c=grid[y][x]
            if c==".": x+=1; continue
            x2=x
            while x2<W and grid[y][x2]==c: x2+=1
            out.append(f'<rect x="{x}" y="{y}" width="{x2-x}" height="1" fill="{PAL[c]}"/>')
            x=x2
    return "".join(out)
svg=(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" shape-rendering="crispEdges" aria-hidden="true">'
     + rects(base)
     + "".join(f'<g class="f-{n}">{rects(f)}</g>' for n,f in faces.items()) + "</svg>")
os.makedirs("/tmp/px", exist_ok=True); open("/tmp/px/char.svg","w").write(svg)
# preview png
from PIL import Image
for n,f in faces.items():
    im=Image.new("RGBA",(W,H),(0,0,0,0)); px=im.load()
    for y in range(H):
        for x in range(W):
            c=f[y][x] if f[y][x]!="." else base[y][x]
            if c!=".":
                h=PAL[c]; px[x,y]=tuple(int(h[i:i+2],16) for i in (1,3,5))+(255,)
    im.resize((W*8,H*8),Image.NEAREST).save(f"/tmp/px/{n}.png")
print(len(svg))
