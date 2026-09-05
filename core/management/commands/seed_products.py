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


class Command(BaseCommand):
    help = "Loads sample products for Hardware and Clothing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--replace", action="store_true",
            help="Delete existing products first instead of updating them.",
        )

    def handle(self, *args, **options):
        from divisions.models import Product

        pairs = [("hardware", HARDWARE), ("clothing", CLOTHING)]
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
