"""
Michoro ya muda ya AMISH — vitu vinavyotambulika, si nakshi tupu.

    python tools/make_placeholders.py

Inachora mifuko ya saruji, matofali, nondo na nguo kwa mtindo wa flat
illustration kwa rangi za kampuni. Ni za kushikilia hadi picha halisi
za duka zipatikane; ukipakia picha kwenye admin, hizi hazitumiki tena.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(__file__), "..", "static", "img", "defaults")

BLUE = (0, 58, 188)
BLUE_L = (92, 125, 240)
NAVY = (10, 27, 74)


def canvas(size, top, bottom, glow=None):
    w, h = size
    strip = Image.new("RGB", (1, h))
    px = strip.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        px[0, y] = tuple(round(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    img = strip.resize(size, Image.BILINEAR)
    if glow:
        cx, cy, r, col = glow
        layer = Image.new("RGB", size, (0, 0, 0))
        ImageDraw.Draw(layer).ellipse(
            [cx - r, cy - r, cx + r, cy + r], fill=col)
        layer = layer.filter(ImageFilter.GaussianBlur(r * 0.6))
        img = Image.blend(img, layer, 0.4)
    return img


def floor(d, size, y, colour, alpha):
    w, _ = size
    d.rectangle([0, y, w, size[1]], fill=colour + (alpha,))
    d.line([(0, y), (w, y)], fill=colour + (alpha + 40,), width=3)


def cement_bag(d, x, y, w, h, fill, edge, alpha):
    """Mfuko wa saruji — mstatili wenye kona zilizokunjwa."""
    r = h * 0.18
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill + (alpha,),
                        outline=edge + (alpha + 60,), width=3)
    d.line([(x + w * .18, y + h * .30), (x + w * .82, y + h * .30)],
           fill=edge + (alpha + 50,), width=3)
    d.line([(x + w * .30, y + h * .52), (x + w * .70, y + h * .52)],
           fill=edge + (alpha + 30,), width=3)
    d.line([(x + w * .35, y + h * .68), (x + w * .65, y + h * .68)],
           fill=edge + (alpha + 20,), width=3)


def bag_stack(d, size, cols, rows, fill, edge, alpha, base=None, bw=None):
    w, h = size
    base = base or h * 0.79
    bw = bw or w / (cols + 1.4)
    bh = bw * 0.42
    for r in range(rows):
        offset = (bw * 0.28) if r % 2 else 0
        for c in range(cols - (1 if r % 2 else 0)):
            x = w * 0.5 - (cols * bw) / 2 + c * bw * 1.02 + offset
            y = base - (r + 1) * bh * 1.06
            cement_bag(d, x, y, bw * 0.96, bh, fill, edge, alpha)


def brick_stack(d, size, fill, edge, alpha, cols=6, rows=7):
    w, h = size
    bw = w / (cols + 2.2)
    bh = bw * 0.40
    base = h * 0.79
    for r in range(rows):
        shift = bw * 0.5 if r % 2 else 0
        n = cols - (1 if r % 2 else 0)
        for c in range(n):
            x = w * 0.5 - (cols * bw) / 2 + c * bw * 1.04 + shift
            y = base - (r + 1) * bh * 1.12
            d.rectangle([x, y, x + bw * 0.98, y + bh], fill=fill + (alpha,),
                        outline=edge + (alpha + 70,), width=3)


def rebar(d, size, fill, edge, alpha, count=7):
    w, h = size
    base, top = h * 0.79, h * 0.14
    gap = w / (count + 3)
    for i in range(count):
        x = w * 0.5 - (count * gap) / 2 + i * gap + gap * 0.5
        lean = (i - count / 2) * gap * 0.16
        d.line([(x, base), (x + lean, top)], fill=fill + (alpha + 30,), width=int(gap * 0.20))
        for k in range(9):
            t = k / 9
            yy = base + (top - base) * t
            xx = x + lean * t
            d.line([(xx - gap * .12, yy), (xx + gap * .12, yy - gap * .07)],
                   fill=edge + (alpha + 10,), width=3)


def hanger(d, cx, top, span, drop, fill, edge, alpha, style="shirt"):
    hook_r = span * 0.10
    d.arc([cx - hook_r, top - hook_r * 2, cx + hook_r, top], 180, 360,
          fill=edge + (alpha + 70,), width=4)
    d.line([(cx, top), (cx, top + drop * 0.10)], fill=edge + (alpha + 70,), width=4)
    sy = top + drop * 0.10
    d.line([(cx, sy), (cx - span * 0.5, sy + drop * 0.10)], fill=edge + (alpha + 70,), width=4)
    d.line([(cx, sy), (cx + span * 0.5, sy + drop * 0.10)], fill=edge + (alpha + 70,), width=4)
    sh = sy + drop * 0.10
    if style == "shirt":
        pts = [(cx - span * .5, sh), (cx - span * .58, sh + drop * .22),
               (cx - span * .36, sh + drop * .26), (cx - span * .36, sh + drop),
               (cx + span * .36, sh + drop), (cx + span * .36, sh + drop * .26),
               (cx + span * .58, sh + drop * .22), (cx + span * .5, sh)]
        d.polygon(pts, fill=fill + (alpha,), outline=edge + (alpha + 60,))
        d.line([(cx, sh), (cx, sh + drop)], fill=edge + (alpha + 40,), width=3)
    elif style == "suit":
        pts = [(cx - span * .5, sh), (cx - span * .54, sh + drop),
               (cx + span * .54, sh + drop), (cx + span * .5, sh)]
        d.polygon(pts, fill=fill + (alpha,), outline=edge + (alpha + 60,))
        d.polygon([(cx - span * .16, sh), (cx, sh + drop * .52),
                   (cx + span * .16, sh)], fill=edge + (alpha + 25,))
    else:  # buibui / kanzu — mrefu, mpana chini
        pts = [(cx - span * .42, sh), (cx - span * .70, sh + drop * 1.12),
               (cx + span * .70, sh + drop * 1.12), (cx + span * .42, sh)]
        d.polygon(pts, fill=fill + (alpha,), outline=edge + (alpha + 60,))
        d.line([(cx, sh), (cx, sh + drop * 1.12)], fill=edge + (alpha + 30,), width=3)


def rail(d, size, fill, edge, alpha, styles=("shirt", "suit", "abaya", "shirt")):
    w, h = size
    top = h * 0.13
    d.line([(w * .06, top), (w * .94, top)], fill=edge + (alpha + 80,), width=5)
    n = len(styles)
    for i, st in enumerate(styles):
        cx = w * (0.16 + i * (0.68 / max(n - 1, 1)))
        hanger(d, cx, top, w * 0.17, h * 0.46, fill, edge, alpha, st)


def shelf_boxes(d, size, fill, edge, alpha, rows=3, cols=5):
    w, h = size
    for r in range(rows):
        y = h * (0.20 + r * 0.19)
        d.line([(w * .05, y + h * .16), (w * .95, y + h * .16)],
               fill=edge + (alpha + 70,), width=5)
        for c in range(cols):
            bw = w * 0.14
            x = w * .08 + c * (w * .84 / cols)
            d.rectangle([x, y, x + bw, y + h * .155], fill=fill + (alpha,),
                        outline=edge + (alpha + 50,), width=3)


def bottles(d, size, fill, edge, alpha, count=5):
    """Chupa za cosmetics — lotion, shampoo, perfume."""
    w, h = size
    base = h * 0.79
    gap = w / (count + 1.6)
    for i in range(count):
        cx = w * 0.5 - (count * gap) / 2 + i * gap + gap * 0.8
        bw = gap * (0.52 if i % 2 else 0.66)
        bh = h * (0.30 + 0.10 * (i % 3))
        top = base - bh
        d.rounded_rectangle([cx - bw / 2, top, cx + bw / 2, base],
                            radius=bw * 0.22, fill=fill + (alpha,),
                            outline=edge + (alpha + 70,), width=3)
        # shingo na kifuniko
        nw = bw * 0.32
        d.rectangle([cx - nw / 2, top - h * 0.045, cx + nw / 2, top],
                    fill=fill + (alpha,), outline=edge + (alpha + 60,), width=3)
        d.rounded_rectangle([cx - nw * 0.72, top - h * 0.082, cx + nw * 0.72, top - h * 0.04],
                            radius=nw * 0.2, fill=edge + (alpha + 30,))
        # lebo
        d.rectangle([cx - bw * 0.36, top + bh * 0.30, cx + bw * 0.36, top + bh * 0.58],
                    outline=edge + (alpha + 50,), width=3)


def bus(d, size, fill, edge, alpha):
    """Basi la mkoa."""
    w, h = size
    base = h * 0.74
    bw, bh = w * 0.66, h * 0.34
    x = (w - bw) / 2
    y = base - bh
    d.rounded_rectangle([x, y, x + bw, base], radius=bh * 0.16,
                        fill=fill + (alpha,), outline=edge + (alpha + 70,), width=4)
    # madirisha
    for i in range(5):
        ww = bw * 0.13
        wx = x + bw * 0.08 + i * (bw * 0.165)
        d.rounded_rectangle([wx, y + bh * 0.18, wx + ww, y + bh * 0.48],
                            radius=ww * 0.14, outline=edge + (alpha + 60,), width=3)
    # mlango
    d.rectangle([x + bw * 0.86, y + bh * 0.18, x + bw * 0.95, base - bh * 0.08],
                outline=edge + (alpha + 60,), width=3)
    # magurudumu
    for cx in (x + bw * 0.22, x + bw * 0.78):
        r = bh * 0.17
        d.ellipse([cx - r, base - r * 0.55, cx + r, base + r * 1.45],
                  fill=edge + (alpha + 30,), outline=edge + (alpha + 80,), width=3)


def house(d, size, fill, edge, alpha, count=3):
    """Nyumba — kwa real estate."""
    w, h = size
    base = h * 0.79
    for i, f in enumerate((0.78, 1.0, 0.62)[:count]):
        bw = w * 0.20 * f + w * 0.06
        bh = h * 0.30 * f
        cx = w * (0.26 + i * 0.24)
        x0, y0 = cx - bw / 2, base - bh
        d.rectangle([x0, y0, x0 + bw, base], fill=fill + (alpha,),
                    outline=edge + (alpha + 70,), width=4)
        d.polygon([(x0 - bw * 0.12, y0), (cx, y0 - bh * 0.42), (x0 + bw * 1.12, y0)],
                  fill=fill + (alpha + 12,), outline=edge + (alpha + 70,))
        # mlango na dirisha
        d.rectangle([cx - bw * 0.11, base - bh * 0.42, cx + bw * 0.11, base],
                    outline=edge + (alpha + 60,), width=3)
        d.rectangle([x0 + bw * 0.12, y0 + bh * 0.20, x0 + bw * 0.32, y0 + bh * 0.42],
                    outline=edge + (alpha + 50,), width=3)


def shopfront(d, size, fill, edge, alpha):
    w, h = size
    base = h * 0.79
    d.rectangle([w * .10, h * .24, w * .90, base], fill=fill + (alpha,),
                outline=edge + (alpha + 60,), width=4)
    d.polygon([(w * .06, h * .24), (w * .50, h * .07), (w * .94, h * .24)],
              fill=fill + (alpha + 18,), outline=edge + (alpha + 60,))
    d.rectangle([w * .38, h * .50, w * .62, base], fill=edge + (alpha + 20,))
    for i in range(2):
        x = w * (.16 + i * .56)
        d.rectangle([x, h * .33, x + w * .16, h * .46], fill=edge + (alpha + 30,))
    d.line([(0, base), (w, base)], fill=edge + (alpha + 60,), width=5)




def draw(name, size, palette, scene, **kw):
    dark = palette == "dark"
    if dark:
        img = canvas(size, (30, 42, 68), (8, 12, 22),
                     glow=(size[0] * .62, size[1] * .30, min(size) * .70, (46, 66, 122)))
        fill, edge, alpha = (255, 255, 255), (255, 255, 255), 26
    else:
        img = canvas(size, (236, 240, 248), (206, 215, 233))
        fill, edge, alpha = (120, 142, 190), (58, 82, 142), 60

    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    floor(d, size, size[1] * 0.80, edge, max(alpha - 12, 10))

    if scene == "bags":
        bag_stack(d, size, kw.get("cols", 5), kw.get("rows", 4), fill, edge, alpha)
    elif scene == "bricks":
        brick_stack(d, size, fill, edge, alpha)
    elif scene == "rebar":
        rebar(d, size, fill, edge, alpha)
    elif scene == "rail":
        rail(d, size, fill, edge, alpha, kw.get("styles", ("shirt", "suit", "abaya", "shirt")))
    elif scene == "shelf":
        shelf_boxes(d, size, fill, edge, alpha)
    elif scene == "front":
        shopfront(d, size, fill, edge, alpha)
    elif scene == "bus":
        bus(d, size, fill, edge, alpha)
    elif scene == "house":
        house(d, size, fill, edge, alpha)
    elif scene == "one-house":
        house(d, size, fill, edge, alpha + 14, count=1)
    elif scene == "bottles":
        bottles(d, size, fill, edge, alpha)
    elif scene == "one-bottle":
        w, h = size
        bottles(d, size, fill, edge, alpha + 14, count=1)
    elif scene == "one-bag":
        w, h = size
        cement_bag(d, w * .26, h * .32, w * .48, h * .34, fill, edge, alpha + 14)
    elif scene == "one-brick":
        w, h = size
        for r in range(3):
            for c in range(2 - r % 2):
                bw, bh = w * .30, h * .13
                x = w * .34 + c * bw * 1.05 + (bw * .5 if r % 2 else 0)
                y = h * .70 - r * bh * 1.15
                d.rectangle([x, y, x + bw, y + bh], fill=fill + (alpha + 14,),
                            outline=edge + (alpha + 80,), width=3)
    elif scene == "one-garment":
        w, h = size
        hanger(d, w * .5, h * .12, w * .34, h * .52, fill, edge, alpha + 14,
               kw.get("style", "shirt"))

    # wimbi la logo
    w, h = size
    top = [(x, h * .90 + math.sin(x / w * math.pi * 1.5) * h * .045)
           for x in range(0, w + 6, 6)]
    band_h = h * .055
    poly = top + [(x, y + band_h) for x, y in reversed(top)]
    d.polygon(poly, fill=BLUE + (185 if not dark else 205,))

    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    img.save(os.path.join(OUT, name), "JPEG", quality=85, optimize=True, progressive=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    hero, panel, band, card, strip = (1800, 1000), (1200, 900), (1800, 900), (900, 675), (900, 630)

    draw("hero-1.jpg", hero, "dark", "bags", cols=6, rows=5)
    draw("hero-2.jpg", hero, "dark", "rail", styles=("shirt", "suit", "abaya", "shirt", "suit"))
    draw("hero-3.jpg", hero, "dark", "front")

    draw("hardware-1.jpg", panel, "dark", "bags", cols=5, rows=4)
    draw("hardware-2.jpg", panel, "dark", "bricks")
    draw("hardware-3.jpg", panel, "dark", "rebar")

    draw("clothing-1.jpg", panel, "dark", "rail")
    draw("clothing-2.jpg", panel, "dark", "rail", styles=("suit", "suit", "shirt"))
    draw("clothing-3.jpg", panel, "dark", "shelf")

    for i, sc in enumerate(("bottles", "shelf", "bottles"), start=1):
        draw(f"cosmetics-{i}.jpg", panel, "dark", sc, shift=(i - 2) * 60)

    for i, sc in enumerate(("bus", "bus", "front"), start=1):
        draw(f"transport-{i}.jpg", panel, "dark", sc, shift=(i - 2) * 60)
    for i, sc in enumerate(("house", "house", "front"), start=1):
        draw(f"real-estate-{i}.jpg", panel, "dark", sc, shift=(i - 2) * 60)

    draw("p-bus.jpg", card, "light", "bus")
    draw("p-house.jpg", card, "light", "one-house")
    draw("p-plot.jpg", card, "light", "house")

    foot = (1800, 700)
    draw("footer-1.jpg", foot, "dark", "front")
    draw("footer-2.jpg", foot, "dark", "bags", cols=8, rows=3)
    draw("footer-3.jpg", foot, "dark", "house")
    draw("footer.jpg", foot, "dark", "front")

    draw("band-1.jpg", band, "dark", "bags", cols=7, rows=4)
    draw("band-2.jpg", band, "dark", "front")
    draw("band-3.jpg", band, "dark", "bricks")

    draw("p-saruji.jpg", card, "light", "one-bag")
    draw("p-matofali.jpg", card, "light", "one-brick")
    draw("p-nondo.jpg", card, "light", "rebar")
    draw("p-watoto.jpg", card, "light", "one-garment", style="shirt")
    draw("p-suti.jpg", card, "light", "one-garment", style="suit")
    draw("p-buibui.jpg", card, "light", "one-garment", style="abaya")

    for name in ("p-lotion", "p-hair", "p-perfume", "p-soap"):
        draw(f"{name}.jpg", card, "light", "one-bottle")

    plan = [("bags", "dark"), ("rail", "light"), ("bricks", "dark"), ("shelf", "light"),
            ("front", "dark"), ("rebar", "light"), ("bags", "light"), ("rail", "dark")]
    for i, (scene, pal) in enumerate(plan, start=1):
        draw(f"g-{i}.jpg", strip, pal, scene)

    print("Michoro zimetengenezwa kwenye static/img/defaults/")


if __name__ == "__main__":
    main()
