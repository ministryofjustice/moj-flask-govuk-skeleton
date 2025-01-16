import os
import yaml
from flask import flash, redirect, render_template, url_for
from werkzeug.exceptions import NotFound
from flask_pydantic import validate
from pydantic import BaseModel

from app.demos import bp

# Pydantic models for form validation
class BankDetails(BaseModel):
    account_name: str
    account_number: str
    sort_code: str

class CreateAccount(BaseModel):
    username: str
    email: str
    password: str

class KitchenSink(BaseModel):
    field1: str
    field2: int
    field3: bool

class ConditionalReveal(BaseModel):
    reveal_field: str

class Autocomplete(BaseModel):
    query: str


@bp.route("/components", methods=["GET"])
def components():
    components = os.listdir("app/demos/govuk_components")
    components.sort()
    return render_template("components.html", components=components)


@bp.route("/components/<string:component>", methods=["GET"])
def component(component):
    try:
        with open(f"app/demos/govuk_components/{component}/{component}.yaml") as yaml_file:
            fixtures = yaml.safe_load(yaml_file)
    except FileNotFoundError:
        raise NotFound

    return render_template("component.html", component=component, fixtures=fixtures)


@bp.route("/forms", methods=["GET"])
def forms():
    return render_template("forms.html")


@bp.route("/forms/bank-details", methods=["POST"])
@validate()
def bank_details(body: BankDetails):
    flash("Demo form successfully submitted", "success")
    return redirect(url_for("demos.forms"))


@bp.route("/forms/create-account", methods=["POST"])
@validate()
def create_account(body: CreateAccount):
    flash("Demo form successfully submitted", "success")
    return redirect(url_for("demos.forms"))


@bp.route("/forms/kitchen-sink", methods=["POST"])
@validate()
def kitchen_sink(body: KitchenSink):
    flash("Demo form successfully submitted", "success")
    return redirect(url_for("demos.forms"))


@bp.route("/forms/conditional-reveal", methods=["POST"])
@validate()
def conditional_reveal(body: ConditionalReveal):
    flash("Demo form successfully submitted", "success")
    return redirect(url_for("demos.forms"))


@bp.route("/forms/autocomplete", methods=["POST"])
@validate()
def autocomplete(body: Autocomplete):
    flash("Demo form successfully submitted", "success")
    return redirect(url_for("demos.forms"))
