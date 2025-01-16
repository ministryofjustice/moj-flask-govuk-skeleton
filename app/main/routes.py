from flask import flash, json, make_response, redirect, render_template, request
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException
from flask_pydantic import validate
from pydantic import BaseModel
from app.main import bp

# Pydantic model for cookie preferences
class CookiesPolicy(BaseModel):
    functional: str
    analytics: str


@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@bp.route("/accessibility", methods=["GET"])
def accessibility():
    return render_template("accessibility.html")


@bp.route("/cookies", methods=["POST"])
@validate()
def cookies_post(body: CookiesPolicy):
    # Default cookies policy if none is provided
    cookies_policy = body.dict()

    # Create flash message confirmation
    flash("You’ve set your cookie preferences.", "success")

    # Create the response so we can set the cookie before returning
    response = make_response(render_template("cookies.html", form=None))

    # Set cookies policy for one year
    response.set_cookie(
        "cookies_policy",
        json.dumps(cookies_policy),
        max_age=31557600,
        secure=True,
    )
    return response


@bp.route("/cookies", methods=["GET"])
def cookies_get():
    form_data = {"functional": "no", "analytics": "no"}  # Default values

    # Load cookies policy if it exists
    if request.cookies.get("cookies_policy"):
        cookies_policy = json.loads(request.cookies.get("cookies_policy"))
        form_data.update(cookies_policy)

    # Render the page with the current consent
    return render_template("cookies.html", form=form_data)


@bp.route("/privacy", methods=["GET"])
def privacy():
    return render_template("privacy.html")


@bp.app_errorhandler(HTTPException)
def http_exception(error):
    return render_template(f"{error.code}.html"), error.code


@bp.app_errorhandler(CSRFError)
def csrf_error(error):
    flash("The form you were submitting has expired. Please try again.")
    return redirect(request.full_path)
