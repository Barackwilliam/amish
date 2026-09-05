# Mfumo wa picha za default — AMISH

## Jinsi inavyofanya kazi

Template haiulizi "picha ipo?" kila mahali. Kuna tag moja inayofanya
uamuzi: ikiwa picha imewekwa kwenye admin, inatumika hiyo. Ikiwa
haijawekwa, inatumika ya default iliyopo kwenye static.

`core/templatetags/amish.py`

```python
from django import template
from django.templatetags.static import static

register = template.Library()


@register.simple_tag
def bg(image, fallback):
    """Picha ya database ikiwepo, la sivyo ya default."""
    try:
        if image and image.url:
            return image.url
    except ValueError:
        pass
    return static(f"img/defaults/{fallback}")
```

Matumizi kwenye template:

```html
{% load amish %}

{% for slide in slides %}
  <div class="sl ken {% if forloop.first %}on{% endif %}"
       style="background-image:url('{% bg slide.image "hero-1.jpg" %}')"></div>
{% empty %}
  <div class="sl ken on" style="background-image:url('{% static 'img/defaults/hero-1.jpg' %}')"></div>
{% endfor %}
```

Moh'd akipakia picha zake, default zinatoweka zenyewe. Hakuna code
inayobadilishwa, na site haionekani tupu siku ya kwanza.

## Zilizomo tayari

Michoro 24 ya muda ipo tayari ndani ya `static/img/defaults/`. Ni michoro ya vitu halisi kwa
rangi za AMISH: mifuko ya saruji, rundo la matofali, nondo, hanger zenye
suti, buibui na nguo za watoto, na sura ya duka. Site inaonekana kamili tangu
dakika ya kwanza, na mtu anaelewa kila sehemu inauza nini.

Kuzitengeneza upya baada ya kubadilisha rangi:

```bash
python tools/make_placeholders.py
```

Hizi ni za kushikilia tu. Zibadilishe na picha halisi mapema uwezavyo — mchoro
hauuzi saruji, picha ya saruji ndiyo inauza.

## Picha zinazohitajika

Ukipata picha halisi, badilisha zilizomo kwa majina yale yale. Zote ziwe JPG
au WebP, upana 1800px kwa hero na band, 900px kwa zingine.

| Faili | Sehemu | Inatakiwa ionyeshe |
|---|---|---|
| hero-1.jpg | Hero slide 1 | Rafu za saruji dukani, mwanga wa ndani |
| hero-2.jpg | Hero slide 2 | Rafu za nguo, mwanga wa asili |
| hero-3.jpg | Hero slide 3 | Mbele ya duka au mtaa wa biashara |
| hardware-1..3.jpg | Paneli ya Hardware | Saruji, matofali, ndani ya duka |
| nguo-1..3.jpg | Paneli ya Nguo | Rafu za nguo, suti, nguo za watoto |
| band-1..3.jpg | Ukanda wa Vision | Mafundi kazini, mzigo ukipakiwa, duka likiwa na wateja |
| p-saruji.jpg, p-matofali.jpg, p-nondo.jpg | Kadi za bidhaa | Bidhaa moja moja, background safi |
| p-watoto.jpg, p-suti.jpg, p-buibui.jpg | Kadi za bidhaa | Nguo moja moja |
| g-1..8.jpg | Mstari wa picha | Mchanganyiko wa duka, bidhaa na kazi |

Jumla: picha 21.

## Wapi kuzipata bila hakimiliki

Tumia hizi tu. Zina leseni inayoruhusu matumizi ya kibiashara bila
malipo wala kutaja chanzo:

- **Pexels** — pexels.com
- **Unsplash** — unsplash.com
- **Pixabay** — pixabay.com

Maneno ya kutafutia:
`cement bags warehouse`, `hardware store interior`, `construction
materials shop`, `clay bricks stack`, `steel rebar`, `clothing store
racks`, `childrens clothing shop`, `mens suits rack`, `abaya`,
`african shop front`, `builders carrying cement`

**Usitumie:** picha kutoka Google Images, Dreamstime, iStock,
Shutterstock au Getty. Zina hakimiliki, na mmiliki akiiona kwenye
site ya biashara anaweza kudai malipo.

## Muhimu

Hizi ni za muda tu. Zinashikilia site hadi picha halisi za AMISH
zipatikane. Picha ya duka la Ulaya haitomshawishi mtu wa Kigamboni
kama picha ya duka lao lenyewe. Mkubaliane na Moh'd siku ya kupiga
picha ndani ya wiki mbili za kwanza.
