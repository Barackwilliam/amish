"""
Django settings — AMISH Company Limited (amish.co.tz)
"""

import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Inasoma .env kwenye kompyuta yako. Kwenye Render, env vars za dashboard
# zinatumika na .env haipo kabisa — kwa hiyo hii haiathiri production.
try:
    from dotenv import load_dotenv

    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).lower() in ("1", "true", "yes", "on")


SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
DEBUG = env_bool("DEBUG", True)

ALLOWED_HOSTS = [h for h in os.environ.get(
    "ALLOWED_HOSTS", "localhost,127.0.0.1,.onrender.com,amish.co.tz,www.amish.co.tz"
).split(",") if h]

CSRF_TRUSTED_ORIGINS = [
    "https://amish.co.tz",
    "https://www.amish.co.tz",
    "https://*.onrender.com",
]

INSTALLED_APPS = [
    # Unfold lazima itangulie django.contrib.admin
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "core",
    "divisions",
    "company",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Supabase transaction pooler (port 6543) haitumii prepared statements wala
# server-side cursors, na inashikilia connection zake yenyewe — ndiyo maana
# conn_max_age ni 0 na prepare_threshold ni None.
USING_POOLER = ":6543" in os.environ.get("DATABASE_URL", "")

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=0 if USING_POOLER else 600,
        conn_health_checks=not USING_POOLER,
        ssl_require=USING_POOLER,
    )
}

if USING_POOLER:
    DATABASES["default"].setdefault("OPTIONS", {})
    DATABASES["default"]["OPTIONS"]["prepare_threshold"] = None
    DISABLE_SERVER_SIDE_CURSORS = True

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Dar_es_Salaam"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = Path(os.environ.get("MEDIA_ROOT", BASE_DIR / "media"))

# Mahali picha zinapohifadhiwa: "local" (disk ya Render) au "s3" (Supabase Storage).
MEDIA_STORAGE = os.environ.get("MEDIA_STORAGE", "local").lower()

if MEDIA_STORAGE == "s3":
    # Supabase: Project Settings > Storage > S3 access keys
    AWS_ACCESS_KEY_ID = os.environ["S3_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = os.environ["S3_SECRET_ACCESS_KEY"]
    AWS_STORAGE_BUCKET_NAME = os.environ.get("S3_BUCKET", "media")
    AWS_S3_ENDPOINT_URL = os.environ["S3_ENDPOINT_URL"]
    AWS_S3_REGION_NAME = os.environ.get("S3_REGION", "us-east-1")
    AWS_S3_ADDRESSING_STYLE = "path"
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False  # URL za wazi, zinazoweza kuindexiwa na Google
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "public, max-age=31536000"}

    # Supabase inapakia kupitia /storage/v1/s3 lakini inasomwa hadharani
    # kupitia /storage/v1/object/public. Bila hii, picha zingepakiwa vizuri
    # lakini browser isingeziona.
    _custom = os.environ.get("S3_CUSTOM_DOMAIN", "")
    if not _custom and "supabase" in AWS_S3_ENDPOINT_URL:
        _host = AWS_S3_ENDPOINT_URL.split("//", 1)[-1].split("/", 1)[0]
        _host = _host.replace(".storage.supabase.co", ".supabase.co")
        _custom = f"{_host}/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}"
    if _custom:
        AWS_S3_CUSTOM_DOMAIN = _custom
        AWS_S3_URL_PROTOCOL = "https:"
    default_storage = {"BACKEND": "storages.backends.s3.S3Storage"}
else:
    default_storage = {"BACKEND": "django.core.files.storage.FileSystemStorage"}

STORAGES = {
    "default": default_storage,
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "amish",
    }
}

# Picha zinazopakiwa hupunguzwa hadi upana huu ili site ifunguke haraka.
IMAGE_MAX_WIDTH = int(os.environ.get("IMAGE_MAX_WIDTH", 1800))
IMAGE_QUALITY = int(os.environ.get("IMAGE_QUALITY", 82))

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

if not DEBUG:
    SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", True)
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "info@amish.co.tz")
ENQUIRY_NOTIFY_EMAIL = os.environ.get("ENQUIRY_NOTIFY_EMAIL", "info@amish.co.tz")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": os.environ.get("LOG_LEVEL", "INFO")},
}


# ---------------------------------------------------------------------------
# Unfold — muonekano wa admin
# ---------------------------------------------------------------------------

from django.templatetags.static import static  # noqa: E402
from django.urls import reverse_lazy  # noqa: E402

UNFOLD = {
    "SITE_TITLE": "AMISH Admin",
    "SITE_HEADER": "AMISH Company Limited",
    "SITE_SUBHEADER": "Your Success, Our Commitment",
    "SITE_URL": "/",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_LANGUAGES": False,
    "BORDER_RADIUS": "6px",
    "COLORS": {
        # #003ABC ikiwa imepanuliwa kuwa mizani kamili
        "primary": {
            "50": "239 244 255",
            "100": "219 232 255",
            "200": "190 214 255",
            "300": "145 187 255",
            "400": "92 146 255",
            "500": "51 104 250",
            "600": "26 68 232",
            "700": "0 58 188",
            "800": "10 45 140",
            "900": "10 27 74",
            "950": "7 18 50",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Website",
                "separator": False,
                "items": [
                    {"title": "Site settings", "icon": "tune",
                     "link": reverse_lazy("admin:core_sitesettings_changelist")},
                    {"title": "Contact details", "icon": "call",
                     "link": reverse_lazy("admin:core_contactinfo_changelist")},
                    {"title": "Opening hours", "icon": "schedule",
                     "link": reverse_lazy("admin:core_businesshour_changelist")},
                    {"title": "Social media", "icon": "share",
                     "link": reverse_lazy("admin:core_sociallink_changelist")},
                ],
            },
            {
                "title": "Home page",
                "separator": True,
                "items": [
                    {"title": "Hero slides", "icon": "wallpaper",
                     "link": reverse_lazy("admin:core_heroslide_changelist")},
                    {"title": "Background images", "icon": "image",
                     "link": reverse_lazy("admin:core_sectionslide_changelist")},
                    {"title": "Why AMISH", "icon": "check_circle",
                     "link": reverse_lazy("admin:core_reason_changelist")},
                    {"title": "Key figures", "icon": "insights",
                     "link": reverse_lazy("admin:core_stat_changelist")},
                    {"title": "Testimonials", "icon": "format_quote",
                     "link": reverse_lazy("admin:core_testimonial_changelist")},
                ],
            },
            {
                "title": "Divisions and stock",
                "separator": True,
                "items": [
                    {"title": "Divisions", "icon": "storefront",
                     "link": reverse_lazy("admin:divisions_division_changelist")},
                    {"title": "Products", "icon": "inventory_2",
                     "link": reverse_lazy("admin:divisions_product_changelist")},
                    {"title": "Categories", "icon": "category",
                     "link": reverse_lazy("admin:divisions_category_changelist")},
                    {"title": "Services", "icon": "handyman",
                     "link": reverse_lazy("admin:divisions_service_changelist")},
                    {"title": "Gallery", "icon": "photo_library",
                     "link": reverse_lazy("admin:divisions_galleryimage_changelist")},
                ],
            },
            {
                "title": "Company",
                "separator": True,
                "items": [
                    {"title": "About the company", "icon": "info",
                     "link": reverse_lazy("admin:company_about_changelist")},
                    {"title": "Core values", "icon": "verified",
                     "link": reverse_lazy("admin:company_corevalue_changelist")},
                    {"title": "Milestones", "icon": "timeline",
                     "link": reverse_lazy("admin:company_milestone_changelist")},
                    {"title": "Team and directors", "icon": "groups",
                     "link": reverse_lazy("admin:company_person_changelist")},
                    {"title": "Registration", "icon": "workspace_premium",
                     "link": reverse_lazy("admin:company_credential_changelist")},
                    {"title": "Clients", "icon": "handshake",
                     "link": reverse_lazy("admin:company_client_changelist")},
                ],
            },
            {
                "title": "Enquiries and pages",
                "separator": True,
                "items": [
                    {"title": "Customer enquiries", "icon": "mail",
                     "link": reverse_lazy("admin:core_enquiry_changelist")},
                    {"title": "FAQs", "icon": "help",
                     "link": reverse_lazy("admin:core_faq_changelist")},
                    {"title": "Pages", "icon": "description",
                     "link": reverse_lazy("admin:core_page_changelist")},
                ],
            },
        ],
    },
}
