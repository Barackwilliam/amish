"""
Loads sample products so the site looks complete before real stock is entered.

    python manage.py seed_products

Prices are placeholders based on typical Dar es Salaam retail ranges. They
MUST be confirmed with Moh'd before the site goes live. Cement and bricks are
seeded with prices hidden, matching the copy that says those figures move with
the market and are quoted on the day.

Safe to re-run: it matches on slug, so anything edited in the admin survives.
Photographs are added through the admin; until then each product falls back to
the placeholder illustrations in static/img/defaults/.
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from divisions.models import Category, Division

# (name, category, summary, description, price, unit, show_price, featured, in_stock)
HARDWARE = [
    ("Twiga Cement 50kg", "Cement",
     "Ordinary Portland cement, 50 kg bag.",
     "General purpose cement suitable for foundations, blockwork, plaster and "
     "screed. Stored off the ground and under cover so it reaches you dry and "
     "free-flowing. Available by the bag or by the tonne, and we can arrange "
     "delivery to site on larger orders.",
     19000, "per bag", False, True, True),
    ("Dangote Cement 50kg", "Cement",
     "Ordinary Portland cement, 50 kg bag.",
     "An alternative to Twiga at a similar grade, often preferred by fundis for "
     "blockwork and plaster. Ask us which is in stock on the day — we usually "
     "carry both, and the price difference between them is small.",
     18500, "per bag", False, False, True),
    ("Simba Cement 50kg", "Cement",
     "Ordinary Portland cement, 50 kg bag.",
     "Widely used across Dar es Salaam for general construction. Same handling "
     "and storage as our other cement: kept dry, sold by the bag or in bulk.",
     18800, "per bag", False, False, True),
    ("Burnt clay bricks", "Bricks",
     "Standard burnt clay bricks, sold per piece.",
     "Fired clay bricks for walling, sold individually or by the thousand. "
     "Prices drop on larger quantities, and for full loads we can arrange "
     "transport to your site. Tell us how many you need and where the site is, "
     "and we will quote the delivered figure rather than the counter price.",
     700, "per piece", False, True, True),
    ("Cement blocks 6 inch", "Bricks",
     "Hollow cement blocks, 6 inch.",
     "Standard 6 inch hollow blocks for load-bearing and partition walls. "
     "Cured properly before sale, because a block sold too early cracks under "
     "load and the customer carries the cost.",
     1800, "per piece", True, False, True),
    ("Cement blocks 4 inch", "Bricks",
     "Hollow cement blocks, 4 inch.",
     "Lighter 4 inch blocks, generally used for internal partition walls where "
     "the wall is not carrying structural load.",
     1400, "per piece", True, False, True),
    ("Reinforcement bar Y12", "Reinforcement bar",
     "Deformed steel bar, 12 mm, 12 metre length.",
     "Deformed high-tensile bar used in columns, beams and slabs on most "
     "residential work. Supplied in standard 12 metre lengths. Tell us the "
     "schedule your fundi has given you and we will work out the quantity with "
     "you rather than leave you guessing.",
     32000, "per length", True, True, True),
    ("Reinforcement bar Y10", "Reinforcement bar",
     "Deformed steel bar, 10 mm, 12 metre length.",
     "Commonly used for stirrups, lintels and lighter structural work. "
     "Available in standard 12 metre lengths.",
     23000, "per length", True, False, True),
    ("Binding wire", "Reinforcement bar",
     "Soft annealed binding wire, sold per kilogram.",
     "Used for tying reinforcement cages and general site work. Sold by weight, "
     "so you can buy exactly what the job needs instead of a full roll.",
     4500, "per kg", True, False, True),
    ("Building sand", "General materials",
     "Clean building sand, sold by the tipper load.",
     "Screened sand suitable for mortar and plaster. Sold by the load and "
     "delivered directly to site. Call us with the location and we will quote "
     "the delivered price, since transport is usually the larger part of the "
     "cost on sand.",
     None, "per load", False, False, True),
    ("Aggregate stones", "General materials",
     "Crushed stone for concrete, sold by the tipper load.",
     "Crushed aggregate for concrete mixes, available in the common sizes. As "
     "with sand, we quote delivered to your site because haulage drives the "
     "price more than the material itself.",
     None, "per load", False, False, True),
    ("Corrugated iron sheets", "General materials",
     "Galvanised roofing sheets, 30 gauge.",
     "Galvanised corrugated sheets for roofing, available in the standard "
     "lengths. Tell us the roof dimensions and we will help work out the number "
     "of sheets and the ridge caps you will need.",
     28000, "per sheet", True, True, True),
    ("Roofing nails", "General materials",
     "Umbrella head roofing nails, sold per kilogram.",
     "Umbrella head nails with washers for fixing corrugated sheets. Sold by "
     "weight so a small roof does not have to buy a full box.",
     5500, "per kg", True, False, True),
    ("Wire nails assorted", "General materials",
     "Common wire nails in assorted sizes.",
     "General purpose wire nails for carpentry and formwork, stocked in the "
     "sizes most often asked for on site.",
     4200, "per kg", True, False, True),
    ("PVC pipes 4 inch", "General materials",
     "PVC drainage pipe, 4 inch.",
     "Drainage pipe for waste lines, supplied in standard lengths with fittings "
     "available to match. Ask us for the bends and junctions at the same time so "
     "you are not making a second trip.",
     22000, "per length", True, False, True),
    ("Paint, emulsion 20L", "General materials",
     "Interior emulsion paint, 20 litre bucket.",
     "Water based emulsion for interior walls and ceilings, available in white "
     "and the common tints. If you need a specific colour matched, tell us a few "
     "days ahead and we will order it in.",
     85000, "per bucket", True, False, True),
]

CLOTHING = [
    ("Children's shirts", "Children's wear",
     "Cotton shirts for ages 1 to 12.",
     "Everyday cotton shirts in the sizes parents actually come looking for, "
     "from toddler through to twelve years. Chosen for how they hold up to "
     "repeated washing rather than how they look on the hanger on day one.",
     18000, "each", True, True, True),
    ("Children's dresses", "Children's wear",
     "Cotton dresses for ages 2 to 12.",
     "Dresses for everyday wear and for occasions, in a range of colours and "
     "sizes. If we do not have the size you need in the design you like, tell us "
     "and we will let you know when it comes in.",
     25000, "each", True, False, True),
    ("Children's trousers", "Children's wear",
     "Durable trousers for ages 3 to 14.",
     "Hard-wearing trousers for school and everyday use, in the fits and sizes "
     "that move fastest.",
     22000, "each", True, False, True),
    ("Baby sets", "Children's wear",
     "Two-piece sets for newborn to 24 months.",
     "Soft cotton sets for infants, popular as gifts. Kept in the smaller sizes "
     "that are hardest to find locally.",
     28000, "per set", True, False, True),
    ("School uniform set", "Cadet uniforms",
     "Shirt and shorts or skirt, primary school.",
     "Complete primary school uniform sets, stocked ahead of each new term "
     "rather than after it starts. Tell us the school and the size and we will "
     "check what we have before you travel.",
     35000, "per set", True, True, True),
    ("Cadet uniform", "Cadet uniforms",
     "Full cadet uniform, assorted sizes.",
     "Cadet uniform supplied as a complete set. Because sizing matters here more "
     "than most garments, we would rather you came in and had the child measured "
     "than guessed from a table.",
     55000, "per set", True, False, True),
    ("School sweater", "Cadet uniforms",
     "Knitted school sweater, assorted colours.",
     "Knitted sweaters in the colours the local schools use. Stocked more "
     "heavily at the start of terms when demand rises.",
     26000, "each", True, False, True),
    ("Two-piece suit", "Suits",
     "Men's two-piece suit, assorted sizes and colours.",
     "A well cut two-piece suit for work, weddings and formal occasions. We "
     "carry a range of sizes and colours, and we would rather sell you one that "
     "fits properly than the one that happens to be in stock. Come in and try "
     "before you decide.",
     220000, "each", True, True, True),
    ("Three-piece suit", "Suits",
     "Men's three-piece suit with waistcoat.",
     "Three-piece suit including waistcoat, for occasions where the two-piece is "
     "not quite enough. Available in the standard sizes with the common colours "
     "kept in stock.",
     320000, "each", True, False, True),
    ("Formal shirts", "Suits",
     "Long-sleeve formal shirts, assorted sizes.",
     "Cotton formal shirts to go with a suit or to wear on their own for office "
     "work, in the collar sizes most often requested.",
     35000, "each", True, False, True),
    ("Buibui, plain", "Buibui",
     "Plain black buibui, assorted lengths.",
     "Plain buibui in the standard lengths, chosen for fabric that keeps its "
     "shape and colour through repeated washing. We would rather stock fewer "
     "pieces that last than fill the rail with items that disappoint after a "
     "few months.",
     65000, "each", True, True, True),
    ("Buibui, embroidered", "Buibui",
     "Buibui with embroidered detail.",
     "Buibui with embroidered detailing at the cuffs and hem, for occasions. "
     "Designs change with what comes in, so what is on the rail today may not be "
     "there next month.",
     110000, "each", True, False, True),
    ("Hijab, assorted", "Buibui",
     "Hijab in assorted colours and fabrics.",
     "A range of colours and fabrics, from everyday cotton through to lighter "
     "material for warm days.",
     15000, "each", True, False, True),
]


COSMETICS = [
    ("Body lotion", "Skin care",
     "Everyday body lotion, assorted sizes.",
     "Body lotion for daily use, stocked in the sizes people buy most: the small "
     "bottle for a handbag and the large one for the household. We buy from "
     "suppliers we can trace, because counterfeit cosmetics are common and the "
     "harm falls on the customer's skin, not on the shop.",
     12000, "each", True, True, True),
    ("Petroleum jelly", "Skin care",
     "Petroleum jelly, assorted sizes.",
     "A household staple that works as hard on dry heels as it does on a child's "
     "face. Stocked in several tub sizes so you can buy for the week or for the "
     "month.", 6500, "each", True, False, True),
    ("Face cream", "Skin care",
     "Moisturising face cream.",
     "Moisturiser for daily use, in the brands customers ask for by name. If the "
     "one you use is not on the shelf, tell us and we will bring it in.",
     18000, "each", True, False, True),
    ("Hair oil", "Hair care",
     "Hair oil and treatment, assorted.",
     "Hair oils and light treatments for everyday care, chosen for the hair types "
     "our customers actually have rather than what looks good in an advert.",
     9000, "each", True, True, True),
    ("Shampoo and conditioner", "Hair care",
     "Shampoo and conditioner sets.",
     "Shampoo and conditioner sold singly or as a set. We keep the sizes that last "
     "a household a month, not the sample bottles.",
     15000, "each", True, False, True),
    ("Hair relaxer", "Hair care",
     "Relaxer kits, assorted strengths.",
     "Relaxer kits in the standard strengths, complete with what the process needs "
     "so you are not sent to a second shop halfway through.",
     14000, "per kit", True, False, True),
    ("Perfume", "Fragrance",
     "Perfume and body spray, assorted.",
     "Fragrance for men and women, from everyday body spray to something kept for "
     "occasions. Come and try before you decide — scent is the one thing you "
     "cannot judge from a label.",
     35000, "each", True, True, True),
    ("Roll-on deodorant", "Fragrance",
     "Roll-on and stick deodorant.",
     "Deodorant in the brands and sizes that move fastest, kept in stock rather "
     "than ordered when someone asks.",
     7000, "each", True, False, True),
    ("Bathing soap", "Soap and bath",
     "Bathing soap, singles and packs.",
     "Bathing soap sold as singles or in packs, which works out cheaper for a "
     "household. We carry the medicated and the everyday varieties.",
     3500, "each", True, False, True),
    ("Shower gel", "Soap and bath",
     "Shower gel, assorted sizes.",
     "Shower gel in the sizes households actually use, stocked alongside the soap "
     "so you can compare what suits your skin and your budget.",
     13000, "each", True, False, True),
]


TRANSPORT = [
    ("Dar es Salaam – Dodoma", "Regional routes",
     "Daily coach service, morning and evening departures.",
     "Scheduled coach between Dar es Salaam and Dodoma, with morning and evening "
     "departures. Seats are numbered and booked in advance, so you know where you "
     "are sitting before you arrive at the stand. Fares vary with the season and "
     "rise around holidays — call us for the fare on your travel date.",
     None, "per seat", False, True, True),
    ("Dar es Salaam – Morogoro", "Regional routes",
     "Daily service on the Morogoro road.",
     "A short run compared with our other routes, which makes it popular for "
     "same-day business travel. Book ahead on Fridays and Sundays, when the road "
     "is busiest.",
     None, "per seat", False, False, True),
    ("Dar es Salaam – Mbeya", "Regional routes",
     "Long-distance coach to the southern highlands.",
     "An overnight run to Mbeya. Because of the distance we keep the coaches "
     "serviced on a fixed schedule rather than when something goes wrong, and we "
     "do not overload beyond the seats sold.",
     None, "per seat", False, False, True),
    ("Dar es Salaam – Arusha", "Regional routes",
     "Coach service to the northern circuit.",
     "Service to Arusha for travel, business and onward connections to the "
     "northern towns. Ask us about luggage allowance when you book, particularly "
     "if you are carrying trade goods.",
     None, "per seat", False, False, True),
    ("Cargo to upcountry regions", "Cargo and delivery",
     "Goods carried on our regional routes.",
     "We carry parcels and trade goods on the same routes our buses run, which "
     "keeps the price well below a dedicated truck. Charged by weight and "
     "distance. Bring your goods packed and labelled, and we will confirm the "
     "cost before we load.",
     None, "by weight", False, False, True),
    ("Building materials to site", "Cargo and delivery",
     "Delivery of cement, bricks and materials.",
     "Delivery for hardware orders, priced by distance and load size. Order your "
     "materials and delivery together and we will quote you one figure rather "
     "than leaving transport as a surprise at the end.",
     None, "per trip", False, False, True),
]

REAL_ESTATE = [
    ("Residential plots, Kigamboni", "Plots for sale",
     "Surveyed plots with title, various sizes.",
     "Surveyed residential plots in Kigamboni with documents we have seen "
     "ourselves. We will walk the plot with you, show you the boundaries, and "
     "explain honestly what the road and water situation is in the rains. Prices "
     "depend on size and location — tell us your budget and we will show you what "
     "fits it.",
     None, "per plot", False, True, True),
    ("Commercial plots", "Plots for sale",
     "Roadside and commercial-zoned plots.",
     "Plots suited to shops, workshops and other commercial use, generally with "
     "road frontage. We will tell you what the zoning allows before you commit, "
     "not after.",
     None, "per plot", False, False, True),
    ("Two and three bedroom houses", "Houses for sale",
     "Completed family homes in Kigamboni and nearby.",
     "Completed houses ready to move into. Every property we list is one we have "
     "visited, with title documents we have inspected. Land and property disputes "
     "are the most expensive mistake a buyer makes in Dar es Salaam, so we would "
     "rather lose a sale than pass on paperwork we are not confident about.",
     None, "per house", False, True, True),
    ("Houses under construction", "Houses for sale",
     "Properties available before completion.",
     "Homes still being built, usually available below the finished price. We "
     "will be clear with you about what is complete, what is not, and what the "
     "remaining work will realistically cost.",
     None, "per house", False, False, True),
    ("Family homes to rent", "Rentals",
     "Long-term rentals, two to four bedrooms.",
     "Family houses available on long lets. We handle the agreement and the "
     "handover so both sides know what was agreed, which prevents most of the "
     "arguments that come later.",
     None, "per month", False, False, True),
    ("Rooms and self-contained units", "Rentals",
     "Smaller units for singles and couples.",
     "Single rooms and self-contained units, suited to students, young "
     "professionals and small families. Availability changes constantly — call us "
     "for what is open this week rather than relying on an old listing.",
     None, "per month", False, False, True),
]


class Command(BaseCommand):
    help = "Loads sample products for Hardware and Clothing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--replace", action="store_true",
            help="Delete existing products first instead of updating them.",
        )
        parser.add_argument(
            "--only", nargs="+", metavar="SLUG",
            help=(
                "Load only these divisions. Choices: hardware, clothing, "
                "cosmetics, transport, real-estate."
            ),
        )

    def handle(self, *args, **options):
        from divisions.models import Product

        pairs = [("hardware", HARDWARE), ("clothing", CLOTHING), ("cosmetics", COSMETICS),
                 ("transport", TRANSPORT), ("real-estate", REAL_ESTATE)]

        wanted = options.get("only")
        if wanted:
            known = {slug for slug, _ in pairs}
            unknown = set(wanted) - known
            if unknown:
                self.stderr.write(
                    f"Unknown division(s): {', '.join(sorted(unknown))}. "
                    f"Choices: {', '.join(sorted(known))}"
                )
                return
            pairs = [(slug, rows) for slug, rows in pairs if slug in wanted]

        made = 0

        for slug, rows in pairs:
            try:
                division = Division.objects.get(slug=slug)
            except Division.DoesNotExist:
                self.stderr.write(
                    f"Division '{slug}' not found. Run seed_amish first."
                )
                continue

            if options["replace"]:
                Product.objects.filter(division=division).delete()

            for order, row in enumerate(rows, start=1):
                (name, cat_name, summary, description, price, unit,
                 show_price, featured, in_stock) = row

                category = Category.objects.filter(
                    division=division, name=cat_name
                ).first()

                Product.objects.update_or_create(
                    division=division,
                    slug=slugify(name),
                    defaults={
                        "name": name,
                        "category": category,
                        "summary": summary,
                        "description": description,
                        "price": price,
                        "unit": unit,
                        "show_price": show_price,
                        "is_featured": featured,
                        "in_stock": in_stock,
                        "order": order,
                    },
                )
                made += 1

        self.stdout.write(self.style.SUCCESS(
            f"{made} sample products loaded.\n"
            "Prices are placeholders — confirm every one with the client before "
            "launch. Add photographs through the admin."
        ))
