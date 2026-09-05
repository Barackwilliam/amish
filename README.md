# AMISH Company Limited — website

Django project ya amish.co.tz. Kila maandishi, picha, bidhaa na mawasiliano
yanahaririwa kupitia Django admin. Hakuna kitu kilichofichwa kwenye code.

## Kuanzisha kwenye kompyuta yako

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# .env ipo tayari ikiwa na DATABASE_URL ya Supabase
python manage.py migrate
python manage.py seed_amish     # taarifa za kampuni
python manage.py seed_products  # bidhaa 29 za sampuli (bei ni za kukadiria)
python manage.py createsuperuser
python manage.py runserver
```

Fungua http://127.0.0.1:8000 na http://127.0.0.1:8000/admin/

## Muundo

| App | Kinachohifadhiwa |
|---|---|
| `core` | mipangilio, rangi, logo, mawasiliano, saa za kazi, social media, hero, takwimu, FAQ, ujumbe wa wateja |
| `divisions` | matawi (Hardware, Nguo, na yanayokuja), picha za paneli, makundi, bidhaa, huduma, gallery |
| `company` | historia, vision, mission, core values, timu na wakurugenzi, BRELA/TIN, wateja |

### Matawi
`Division.status` ina hali mbili. `Inafanya kazi` — tawi lina ukurasa wake
kamili. `Inakuja hivi karibuni` — jina linaonekana homepage na footer kama
teaser, bila ukurasa wa bidhaa. Migahawa, usafiri na furniture zipo hapo sasa.
Zikianza, badilisha dropdown moja — hakuna code inayoandikwa upya.

### Rangi
Zinatoka `SiteSettings` na kuingizwa kama CSS variables kwenye `base.html`.
Rangi kuu ni `#003ABC` (imechukuliwa kwenye logo). Ukibadilisha admin,
site nzima inabadilika.

### Slides
Sehemu nne zina picha zinazobadilika: hero, paneli za matawi, ukanda wa Vision
na mstari wa picha. Zote zinatoka kwenye admin. JavaScript ni faili moja ya
5KB bila maktaba yoyote; slideshow inaanza tu pale section yake inapoonekana
kwenye skrini.

### Picha za default
Michoro 24 ya muda yenye brand ya AMISH ipo tayari kwenye `static/img/defaults/`,
zimetengenezwa na `tools/make_placeholders.py`. Angalia `PICHA-ZA-DEFAULT.md`. Tag ya `{% bg %}` inachagua picha ya database
ikiwepo, la sivyo inatumia ya `static/img/defaults/`.

### Picha
Kila picha inayopakiwa inapunguzwa kiotomatiki hadi upana wa `IMAGE_MAX_WIDTH`
(1800px) na kubanwa. Moh'd anaweza kupakia picha ya simu ya 5MB bila kuathiri
kasi ya site. Angalia `core/imaging.py`.

## Kupeleka Render

`render.yaml` ipo tayari — Render itaisoma yenyewe (Blueprint).

Env vars zinazohitajika:

| Key | Thamani |
|---|---|
| `SECRET_KEY` | Render itaitengeneza |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `amish.co.tz,www.amish.co.tz,.onrender.com` |
| `DATABASE_URL` | connection string ya Supabase (pooler, port 6543) |
| `MEDIA_STORAGE` | `s3` |
| `S3_ENDPOINT_URL` | `https://<project-ref>.supabase.co/storage/v1/s3` |
| `S3_ACCESS_KEY_ID` / `S3_SECRET_ACCESS_KEY` | Supabase > Storage > S3 access keys |
| `S3_BUCKET` | `media` (bucket iwe public) |
| `S3_REGION` | mkoa wa project |

### Database
`.env` ina `DATABASE_URL` ya Supabase transaction pooler (port 6543). Pooler
haitumii prepared statements wala server-side cursors, kwa hiyo `settings.py`
inazizima yenyewe ikiona `:6543` kwenye URL, na `conn_max_age` inakuwa 0.

Alama maalum kwenye password lazima ziandikwe kwa muundo wa URL: `@` ni `%40`,
`#` ni `%23`, `/` ni `%2F`.

### Picha: disk au Supabase Storage

`MEDIA_STORAGE=local` (chaguo-msingi) inatumia disk ya Render. `MEDIA_STORAGE=s3`
inatumia Supabase Storage kupitia django-storages. Hakuna model wala template
inayobadilika — ni env vars pekee:

| Key | Mfano |
|---|---|
| `MEDIA_STORAGE` | `s3` |
| `S3_ENDPOINT_URL` | `https://<project-ref>.supabase.co/storage/v1/s3` |
| `S3_ACCESS_KEY_ID` | kutoka Project Settings > Storage > S3 access keys |
| `S3_SECRET_ACCESS_KEY` | ,, |
| `S3_BUCKET` | `media` |
| `S3_REGION` | mkoa wa project yako |

Bucket lazima iwe **public**, vinginevyo Google haitaziona picha na URL
zitakuwa na muda wa kuisha. `AWS_QUERYSTRING_AUTH` imezimwa kwa sababu hiyo.

**Muhimu kwa Render free tier:** disk za kudumu zinapatikana kwa plan zinazolipiwa
pekee. Bila disk, filesystem ni ya muda — picha zote zinapotea kila deploy au
restart. Kwa hiyo kwenye free tier **lazima** utumie `MEDIA_STORAGE=s3`.
`local` inafaa tu kwa kompyuta yako au kwa Render yenye disk iliyolipiwa.

Baada ya deploy ya kwanza, tengeneza superuser:

```bash
python manage.py createsuperuser
```

## Kitakachofuata

- [ ] Picha halisi zibadilishe za muda zilizopo `static/img/defaults/`
- [ ] Logo ya ubora (AI/SVG/PNG transparent) ipakiwe kwenye SiteSettings
- [ ] Picha za duka la hardware na duka la nguo (cover za matawi)
- [ ] Bidhaa halisi na bei
- [ ] Vyeo na namba za Abdi, Haji na Moh'd (Timu na wakurugenzi)
- [ ] Latitude/longitude ya duka kwa ramani
- [ ] BRELA na TIN zikipatikana
- [ ] Links za social media zikishafunguliwa

---
JamiiTek Digital Agency

> `.env` haiji ndani ya zip kwa makusudi — ingefuta ile yako yenye keys halisi.
> Nakili `.env.example` kuwa `.env` mara ya kwanza pekee, kisha jaza yako.
