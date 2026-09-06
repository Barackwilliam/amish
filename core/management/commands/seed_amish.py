"""
Seeds AMISH Company Limited with its real content, in English.

    python manage.py seed_amish

Safe to run repeatedly: it uses update_or_create, so anything Moh'd edits
in the admin is preserved rather than wiped.
"""

from datetime import time

from django.core.management.base import BaseCommand

from company.models import About, CoreValue, Milestone, Person
from core.models import (
    FAQ, BusinessHour, ContactInfo, HeroSlide, Reason, SiteSettings, Stat,
)
from divisions.models import Category, Division

INTRO = (
    "AMISH Company Limited is a Kigamboni trading company supplying building "
    "materials, clothing and cosmetics, and running transport and real estate "
    "services across Dar es Salaam."
)

ABOUT_INTRO = (
    "AMISH Company Limited is a family-run trading company based in Geza, "
    "Kigamboni. We supply the two things our neighbourhood asks for most: "
    "materials for people building homes, and clothing for the families who "
    "live in them. We opened in September 2026, and we are building this "
    "company one satisfied customer at a time."
)

STORY = (
    "AMISH Company Limited opened in Kigamboni in September 2026, and the "
    "reason was simple enough to see from the roadside. Geza and the wards "
    "around it are growing faster than the businesses serving them. New homes "
    "go up every month, but a family laying a foundation still had to travel "
    "into the city centre for a few bags of cement, losing half a day and a "
    "fare that could have paid for another bag. Parents did the same journey "
    "for school clothes and for a decent suit.\n\n"
    "We started with the two things people asked for most often. Our hardware "
    "division supplies cement, burnt bricks, reinforcement bar and general "
    "building materials, serving both the homeowner buying a single bag and "
    "the contractor ordering for a whole site. Our clothing division covers "
    "the family: children's wear, cadet and school uniforms, suits and buibui, "
    "kept in the sizes people actually come looking for.\n\n"
    "Being a young company shapes how we work rather than limiting it. We have "
    "no long list of past projects to point at, so we compete on the things a "
    "customer can judge on the first visit: an honest price quoted the same day "
    "you ask, stock that is actually on the shelf when we say it is, and "
    "someone who picks up the phone. Every customer who walks in during our "
    "first year is someone whose trust we have to earn from nothing.\n\n"
    "Three further divisions are in preparation: restaurants, transport and "
    "furniture. Each will open only when we can run it to the same standard, "
    "because a business that opens badly is harder to fix than one that opens "
    "late. That standard is written into our name and into the promise we "
    "trade under: Your Success, Our Commitment."
)

VALUES = [
    ("Integrity",
     "We hold to what we say. Prices are quoted honestly and stock is described "
     "as it actually is, because a customer who feels misled once does not come "
     "back, and in a neighbourhood business word travels faster than any "
     "advertising we could buy. This is the foundation every long-term "
     "relationship with our customers and suppliers is built on."),
    ("Accountability",
     "We take responsibility for our decisions, our promises, our stock and our "
     "results. If an order is delayed or something arrives wrong, we say so "
     "directly and put it right rather than leaving the customer to chase us. "
     "Ownership sits with us, not with circumstances."),
    ("Excellence",
     "We supply materials and clothing we would be willing to use ourselves. "
     "That means checking what we buy before it reaches our shelves, refusing "
     "stock that falls short, and accepting a smaller margin over a sale we "
     "would be embarrassed by later."),
    ("Prompt Service",
     "A customer's time is worth as much as ours. We answer the phone, quote "
     "the same day, and prepare orders so that nobody waits at the counter "
     "longer than necessary. For anyone building, a day lost waiting on "
     "materials is a day of labour paid for and wasted."),
    ("Innovation",
     "We look for better ways to run the business, from how we hold stock to "
     "how customers reach us. That is why you can get today's price over "
     "WhatsApp instead of travelling to ask, and why our range keeps changing "
     "in response to what people actually request."),
]

DIVISIONS = [
    {
        "name": "AMISH Hardware", "slug": "hardware",
        "tagline": "Cement, bricks and building materials for homeowners, "
                   "tradesmen and contractors.",
        "description": (
            "Our hardware division serves everyone building in Kigamboni and the "
            "surrounding areas, from a homeowner adding a room to a contractor "
            "running a full site. We carry cement, burnt bricks, reinforcement "
            "bar and the general materials a job needs from foundation to "
            "finishing.\n\n"
            "We sell in whatever quantity suits you. A single bag for a small "
            "repair is as welcome as a bulk order for a project, and for larger "
            "orders we can arrange transport to your site so that materials "
            "arrive when your fundis do, not days later.\n\n"
            "Prices for cement and bricks move with the market, sometimes week "
            "to week. Rather than publish a figure that goes stale, we quote you "
            "today's price over the phone or WhatsApp before you travel. Call "
            "us, tell us what the job needs, and we will tell you what it costs "
            "and what is on the shelf right now."
        ),
        "status": "active", "kind": "products", "order": 1,
        "categories": ["Cement", "Bricks", "Reinforcement bar", "General materials"],
    },
    {
        "name": "AMISH Clothing", "slug": "clothing",
        "tagline": "Children's wear, cadet uniforms, suits and buibui for the "
                   "whole family.",
        "description": (
            "Our clothing division is built around the family rather than a "
            "single shopper. Children's wear runs across the ages parents "
            "actually buy for, and we keep cadet and school uniforms stocked "
            "ahead of each term rather than scrambling once the term begins.\n\n"
            "For adults we carry suits in a range of sizes and colours, and "
            "buibui chosen for how they wear over time rather than how they look "
            "on the first day. We would rather stock fewer pieces that last than "
            "fill the rails with items that disappoint after a few washes.\n\n"
            "You are welcome to come and see for yourself, and that is still the "
            "best way to judge a garment. If you cannot get to Geza, message us "
            "on WhatsApp and we will send photographs of what is currently in "
            "stock in the size you need."
        ),
        "status": "active", "kind": "products", "order": 2,
        "categories": ["Children's wear", "Cadet uniforms", "Suits", "Buibui"],
    },
    {
        "name": "AMISH Cosmetics", "slug": "cosmetics",
        "tagline": "Skin care, hair care, fragrance and everyday beauty essentials.",
        "description": (
            "Our cosmetics division carries the products people use every day rather "
            "than a shelf of novelties: body lotion and petroleum jelly, soap and "
            "shower gel, hair oil, relaxers and shampoo, roll-on and perfume, and the "
            "small items that always run out at the wrong moment.\n\n"
            "We buy from suppliers we can trace, because counterfeit cosmetics are "
            "common and the harm falls on the customer's skin, not on the shop. If we "
            "cannot verify where a product came from, we do not put it on the shelf, "
            "even when the margin looks good.\n\n"
            "Tell us what you normally use and we will tell you whether we have it and "
            "what it costs today. If we do not stock it yet and enough people ask, we "
            "will bring it in — most of what is on our shelves arrived exactly that way."
        ),
        "status": "active", "kind": "products", "order": 3,
        "categories": ["Skin care", "Hair care", "Fragrance", "Soap and bath"],
    },
    {
        "name": "AMISH Restaurants", "slug": "restaurants",
        "tagline": "A food service for Kigamboni, currently in preparation.",
        "description": (
            "Our restaurant division is in preparation. We are working through "
            "location, kitchen and supply before opening, because food is a "
            "business where a poor start is very hard to recover from. It will "
            "open here when it is ready to run properly."
        ),
        "status": "coming_soon", "kind": "services", "order": 6,
        "launch_note": "In preparation", "categories": [],
    },
    {
        "name": "AMISH Transport", "slug": "transport",
        "tagline": "Regional bus services and delivery of goods across Tanzania.",
        "description": (
            "Our transport division runs two services from the same office. The first "
            "is regional bus travel — scheduled coaches between Dar es Salaam and the "
            "upcountry regions, booked in advance so you are not standing at the stand "
            "hoping for a seat.\n\n"
            "The second is cargo. We move building materials to site for our hardware "
            "customers, and we carry general goods on the same routes our buses run, "
            "which keeps the cost down for anyone sending something upcountry.\n\n"
            "Seats and cargo space both fill up, particularly around holidays and the "
            "start of school terms. Call or message us to book rather than arriving on "
            "the day and hoping."
        ),
        "status": "active", "kind": "services", "order": 4,
        "categories": ["Regional routes", "Cargo and delivery"],
    },
    {
        "name": "AMISH Real Estate", "slug": "real-estate",
        "tagline": "Plots, houses and rentals in Kigamboni and across Dar es Salaam.",
        "description": (
            "Our real estate division handles plots, houses and rentals, with most of "
            "our listings in Kigamboni and the areas we know well. Knowing the ground "
            "matters here: we can tell you which plots flood in the long rains and "
            "which roads are actually passable in April, because we live here.\n\n"
            "Every property we list is one we have visited, with documents we have "
            "seen. Land disputes are the most expensive mistake a buyer can make in "
            "Dar es Salaam, and we would rather lose a sale than pass on a title we "
            "are not confident about.\n\n"
            "Tell us your budget and the area you have in mind and we will show you "
            "what fits. If we do not have it, we will say so rather than walk you "
            "around something that does not."
        ),
        "status": "active", "kind": "services", "order": 5,
        "categories": ["Plots for sale", "Houses for sale", "Rentals"],
    },
    {
        "name": "AMISH Furniture", "slug": "furniture",
        "tagline": "Home and office furniture, in preparation.",
        "description": (
            "Our furniture division is in preparation. It follows naturally from "
            "hardware: the same customer who builds a house then has to furnish "
            "it, and would rather deal with a supplier they already know."
        ),
        "status": "coming_soon", "kind": "products", "order": 7,
        "launch_note": "In preparation", "categories": [],
    },
]

REASONS = [
    ("It is in your neighbourhood",
     "No half-day trip into the city centre for a few bags of cement or a school "
     "uniform. We are in Geza, opposite GMK Super Market, which means the fare "
     "and the hours you would have spent travelling stay in your pocket."),
    ("Today's price, before you travel",
     "Cement and brick prices move constantly. Call or message us and we will "
     "give you the current price and tell you what is in stock, so you know the "
     "cost of the job before you leave the house."),
    ("Small orders and large ones",
     "One bag for a repair or a full delivery for a site: both are served "
     "properly. Small customers are not an inconvenience to us, they are most of "
     "our business, and many of them grow into large ones."),
    ("Two needs, one company",
     "Building materials and clothing under a single name you can hold "
     "accountable. If something goes wrong with either, you are dealing with the "
     "same people, not being passed between strangers."),
]

FAQS = [
    ("Where exactly are you located?",
     "We are in Geza, Kigamboni, directly opposite GMK Super Market. If you are "
     "coming from the ferry, continue along the main road and ask for GMK; "
     "everyone in the area knows it. Call us when you are close and we will "
     "guide you the last part of the way."),
    ("What are your opening hours?",
     "We open Monday to Saturday, from 7:30 in the morning until 6:00 in the "
     "evening, and we are closed on Sunday. If you need something urgently "
     "outside those hours, call us and we will do what we reasonably can."),
    ("Can I get a price without coming to the shop?",
     "Yes, and we would encourage it. Message us on WhatsApp or call, tell us "
     "what you need and roughly how much, and we will give you that day's price "
     "along with what is currently in stock. It saves you a wasted journey if "
     "an item has run out."),
    ("Do you deliver to site?",
     "For larger orders of cement, bricks and materials we can arrange transport "
     "to your site. Ask about it when we quote you, because the cost depends on "
     "the distance and the size of the load, and we would rather give you one "
     "complete figure than surprise you afterwards."),
    ("Do you keep school and cadet uniforms in stock?",
     "Yes. We stock cadet and school uniforms and try to build up quantities "
     "ahead of each new term rather than after it starts. If we do not have the "
     "size you need, tell us and we will let you know when it comes in."),
    ("Can I order a quantity you do not currently have?",
     "In most cases yes. Tell us what you need and by when, and we will tell you "
     "honestly whether we can meet that date. We would rather turn down a job we "
     "cannot deliver on time than accept it and hold up your work."),
]

HERO = [
    ("Cement and bricks, without the trip into town.",
     "One bag for a repair or a full order for a site. Get today's price on the "
     "phone before you travel, and know what is on the shelf before you leave "
     "the house."),
    ("Clothing for the whole family, under one roof.",
     "Children's wear, cadet uniforms, suits and buibui, kept in the sizes "
     "people actually come looking for. Come and see, or message us for photos "
     "of what is in stock."),
    ("One company. Five divisions.",
     "Five divisions are trading today from Geza, Kigamboni: hardware, clothing, "
     "cosmetics, transport and real estate. Restaurants and furniture are in "
     "preparation."),
]


class Command(BaseCommand):
    help = "Seeds AMISH Company Limited content"

    def handle(self, *args, **options):
        site = SiteSettings.load()
        site.company_name = "AMISH Company Limited"
        site.slogan = "Your Success, Our Commitment"
        site.short_intro = INTRO
        site.color_primary = "#003ABC"
        site.color_ink = "#000000"
        site.color_surface = "#FFFFFF"
        site.meta_description = (
            "Cement, bricks, building materials and clothing in Geza, Kigamboni "
            "— opposite GMK Super Market. Open Monday to Saturday."
        )
        site.save()

        contact = ContactInfo.load()
        contact.phone_primary = "0717 003 466"
        contact.phone_secondary = "+255 711 686 816"
        contact.whatsapp = "255711686816"
        contact.email = "info@amish.co.tz"
        contact.street = "Geza, opposite GMK Super Market"
        contact.ward = "Kigamboni"
        contact.city = "Dar es Salaam"
        contact.save()

        for day in range(1, 8):
            closed = day == 7
            BusinessHour.objects.update_or_create(
                day=day,
                defaults={
                    "opens_at": None if closed else time(7, 30),
                    "closes_at": None if closed else time(18, 0),
                    "is_closed": closed,
                    "order": day,
                },
            )

        about = About.load()
        about.intro = ABOUT_INTRO
        about.story = STORY
        about.vision_en = (
            "To become a trusted and leading company, recognized for sustainable "
            "growth, excellence, innovation and reliable service."
        )
        about.vision_sw = (
            "Kuwa kampuni inayoaminika na inayoongoza, inayotambuliwa kwa ukuaji "
            "endelevu, ubora wa hali ya juu, ubunifu na huduma zinazotegemewa."
        )
        about.mission_en = (
            "To deliver quality products and prompt services that create lasting "
            "value for our customers, partners and communities through integrity, "
            "excellence and innovation."
        )
        about.mission_sw = (
            "Kutoa bidhaa bora na huduma za haraka zinazotengeneza thamani ya "
            "kudumu kwa wateja, washirika na jamii kupitia uadilifu, ubora na "
            "ubunifu."
        )
        about.save()

        for i, (title, description) in enumerate(VALUES, start=1):
            CoreValue.objects.update_or_create(
                title=title, defaults={"description": description, "order": i},
            )

        # Jina la zamani la Kiswahili likibadilika kuwa la Kiingereza
        Division.objects.filter(slug="nguo").update(slug="clothing")
        Division.objects.filter(slug="migahawa").update(slug="restaurants")
        Division.objects.filter(slug="usafiri").update(slug="transport")

        for data in DIVISIONS:
            payload = dict(data)
            categories = payload.pop("categories", [])
            division, _ = Division.objects.update_or_create(
                slug=payload["slug"], defaults=payload,
            )
            division.categories.exclude(
                name__in=categories
            ).delete() if categories else None
            for j, name in enumerate(categories, start=1):
                Category.objects.update_or_create(
                    division=division,
                    slug=name.lower().replace(" ", "-").replace("'", ""),
                    defaults={"name": name, "order": j},
                )

        Person.objects.update_or_create(
            full_name="Salim Hassan Iddi",
            defaults={
                "position": "Managing Director",
                "bio": (
                    "Salim holds a Master's degree in Business Administration and "
                    "leads AMISH across both its hardware and clothing operations. "
                    "He founded the company in 2026 around a principle he applies "
                    "to every transaction: a customer served properly once will "
                    "come back, and will bring someone with them."
                ),
                "is_director": True,
                "on_business_card": True,
                "order": 1,
            },
        )

        Milestone.objects.update_or_create(
            year="2026",
            defaults={
                "title": "AMISH opens in Kigamboni",
                "description": (
                    "The company is registered and opens with two divisions "
                    "trading from Geza: hardware and clothing."
                ),
                "order": 1,
            },
        )

        for i, (value, label) in enumerate(
            [("5", "Divisions trading today"),
             ("2", "Divisions in preparation"),
             ("6", "Days open each week")], start=1,
        ):
            Stat.objects.update_or_create(label=label, defaults={"value": value, "order": i})

        for i, (title, description) in enumerate(REASONS, start=1):
            Reason.objects.update_or_create(
                title=title, defaults={"description": description, "order": i},
            )

        for i, (question, answer) in enumerate(FAQS, start=1):
            FAQ.objects.update_or_create(question=question, defaults={"answer": answer, "order": i})

        if not HeroSlide.objects.exists():
            for i, (headline, subline) in enumerate(HERO, start=1):
                HeroSlide.objects.create(
                    headline=headline, subline=subline,
                    cta_label="See what we stock", cta_url="/divisions/", order=i,
                )

        self.stdout.write(self.style.SUCCESS(
            "AMISH content seeded. Upload the logo and photographs via the admin."
        ))
