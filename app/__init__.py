from flask import Flask
from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from govuk_frontend_wtf.main import WTFormsHelpers
from jinja2 import ChoiceLoader, PackageLoader, PrefixLoader
from werkzeug.middleware.proxy_fix import ProxyFix
from app.helpers.static_helpers import get_hashed_filename

from app.config import Config

compress = Compress()
csrf = CSRFProtect()
limiter = Limiter(
    get_remote_address,
    default_limits=["2 per second", "60 per minute"],
)
talisman = Talisman()


def create_app(config_class=Config):
    app: Flask = Flask(__name__, static_url_path="/assets", static_folder="static/dist")
    app.url_map.strict_slashes = False  # This allows www.host.gov.uk/category to be routed to www.host.gov.uk/category/
    app.config.from_object(config_class)
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True
    app.jinja_loader = ChoiceLoader(
        [
            PackageLoader("app"),
            PrefixLoader(
                {
                    "govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja"),
                    "govuk_frontend_wtf": PackageLoader("govuk_frontend_wtf"),
                }
            ),
        ]
    )
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

    # Set content security policy
    csp = {
        "default-src": "'self'",
        "script-src": [
            "'self'",
            "'sha256-GUQ5ad8JK5KmEWmROf3LZd9ge94daqNvd8xy9YS1iDw='",
            "*.googletagmanager.com",
        ],
        "connect-src": [
            "'self'",
            "*.google-analytics.com",
        ],
        "img-src": ["'self'", "*.googletagmanager.com", "www.gov.uk"],
    }

    # Set permissions policy.
    # Remove policy's you do not need for your project.
    permissions_policy = {
        "accelerometer": "()",
        "ambient-light-sensor": "()",
        "autoplay": "()",
        "battery": "()",
        "camera": "()",
        "cross-origin-isolated": "()",
        "display-capture": "()",
        "document-domain": "()",
        "encrypted-media": "()",
        "execution-while-not-rendered": "()",
        "execution-while-out-of-viewport": "()",
        "fullscreen": "()",
        "geolocation": "()",
        "gyroscope": "()",
        "keyboard-map": "()",
        "magnetometer": "()",
        "microphone": "()",
        "midi": "()",
        "navigation-override": "()",
        "payment": "()",
        "picture-in-picture": "()",
        "publickey-credentials-get": "()",
        "screen-wake-lock": "()",
        "sync-xhr": "()",
        "usb": "()",
        "web-share": "()",
        "xr-spatial-tracking": "()",
        "clipboard-read": "()",
        "clipboard-write": "()",
        "gamepad": "()",
        "speaker-selection": "()",
        "conversion-measurement": "()",
        "focus-without-user-activation": "()",
        "hid": "()",
        "idle-detection": "()",
        "interest-cohort": "()",
        "serial": "()",
        "sync-script": "()",
        "trust-token-redemption": "()",
        "unload": "()",
        "window-management": "()",
        "vertical-scroll": "()",
    }

    # Initialise app extensions
    compress.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    talisman.init_app(
        app,
        content_security_policy=csp,
        permissions_policy=permissions_policy,
        content_security_policy_nonce_in=["script-src"],
        force_https=True,
        session_cookie_secure=True,
        session_cookie_http_only=True,
        session_cookie_samesite="Strict",
    )

    WTFormsHelpers(app)

    # Register blueprints
    from app.demos import bp as demo_bp
    from app.main import bp as main_bp

    app.register_blueprint(demo_bp)
    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_hashed_filename():
        """
        Adds the 'get_hashed_filename' function to the Jinja2 context.

        This allows the 'get_hashed_filename' utility function to be used directly
        in Jinja2 templates to dynamically retrieve the correct hashed filename
        for static assets (e.g., CSS and JS files) based on the manifest file.
        """
        return {"get_hashed_filename": get_hashed_filename}

    return app
