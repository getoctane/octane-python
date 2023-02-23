#!/usr/bin/env python

import octane
from os import getenv
from coolname import generate_slug
from flask import Flask, request, make_response, send_from_directory

octane.api_key = getenv("OCTANE_API_KEY")

app = Flask("antler-db-cloud-shop")

# Application settings and defaults
port = getenv("APP_PORT", 3000)
bind = getenv("APP_BIND", "127.0.0.1")
octane_redirect_url = getenv(
    "OCTANE_REDIRECT_URL", "https://cloud.getoctane.io"
)
price_plan_name = getenv("OCTANE_PRICE_PLAN_NAME", "antlerdb")
meter_name_storage = getenv("OCTANE_METER_NAME_STORAGE", "storage")
meter_name_bandwidth = getenv("OCTANE_METER_NAME_BANDWIDTH", "bandwidth")
meter_name_machines = getenv("OCTANE_METER_NAME_MACHINES", "machines")
meter_rate_storage = getenv("env.OCTANE_METER_RATE_STORAGE", 2)
meter_rate_bandwidth = getenv("env.OCTANE_METER_RATE_BANDWIDTH", 5)
meter_rate_machines = getenv("env.OCTANE_METER_RATE_MACHINES", 10)

# The frontend sends us generic resource names,
# which we convert to meter names
resource_meter_map = {
    "storage": meter_name_storage,
    "bandwidth": meter_name_bandwidth,
    "machines": meter_name_machines,
}


@app.route("/")
@app.route("/index.html", methods=["GET"])
def public_index_html():
    return send_from_directory("public", "index.html")


@app.route("/scripts.js", methods=["GET"])
def public_scripts_js():
    return send_from_directory("public", "scripts.js")


@app.route("/styles.css", methods=["GET"])
def public_styles_css():
    return send_from_directory("public", "styles.css")


@app.route("/api/whoami", methods=["GET"])
def api_whoami():
    if request.cookies.get("username"):
        return {
            "code": 200,
            "name": request.cookies.get("username"),
            "url": octane_redirect_url,
        }

    # If no cookie, then generate a name and create the customer in Octane
    name = generate_slug(2)
    print(f'[octane] Attempting to create new customer "{name}"')

    try:
        octane.Customer.create(
            name=name,
            measurement_mappings=[
                {"label": "customer_name", "value_regex": name}
            ],
        )
        print(f'[octane] Customer "{name}" successfully created')
        print(
            f'[octane] Attempting to subscribe customer "{name}" '
            + f'to price plan "{price_plan_name}"'
        )
        try:
            octane.Customer.create_subscription(
                name, price_plan_name=price_plan_name
            )
            print(
                f'[octane] Successfully subscribed customer "{name}" '
                + f'to price plan "{price_plan_name}"'
            )
            resp = make_response(
                {
                    "code": 201,
                    "name": name,
                    "url": octane_redirect_url,
                }
            )
            resp.set_cookie("username", name)
            return resp, 201

        except octane.error.APIError as e:
            print(
                '[octane] Error subscribing customer "{name}" '
                + f'to price plan "{price_plan_name}"'
            )
            return e.json_body, e.http_status

    except octane.error.APIError as e:
        print('[octane] Error creating customer "{name}"')
        return e.json_body, e.http_status


@app.route("/api/resources", methods=["POST"])
def api_resources():
    if not request.cookies.get("username"):
        return {"code": 403, "message": "No session, please refresh"}, 403

    data = request.json
    resource = data["resource"]
    if resource not in resource_meter_map:
        return {"code": 400, "message": "Invalid resource provided"}, 400

    meter_name = resource_meter_map[resource]

    value = data["value"]
    username = request.cookies.get("username")
    print(
        "[octane] Attempting to create measurement "
        + f'for customer "{username}"'
    )
    try:
        octane.Measurement.create(
            meter_name=meter_name,
            value=int(value),
            labels={"customer_name": username},
        )
        print(
            f'[octane] Measurement for customer "{username}" '
            + f'for meter "{meter_name}" successfully created'
        )
        return {"code": 201, "message": "success"}, 201

    except octane.error.APIError as e:
        print(
            "[octane] Error creating measurement "
            + f'for customer "{username}" '
            + f'for meter "{meter_name}"'
        )
        return e.json_body, e.http_status


def check_octane_api_key():
    if not octane.api_key:
        raise Exception("Must set OCTANE_API_KEY.")


def check_octane_resource_meter(meter):
    name = meter["name"]
    print(f'[octane] Checking if meter "{name}" exists')
    try:
        octane.Meter.retrieve(name)
        print(f'[octane] Meter "{name}" already exists')
    except octane.error.APIError as e:
        if e.http_status == 401:
            raise Exception("Unauthorized, please check your OCTANE_API_KEY.")
        print(f'[octane] Meter "{name}" does not exist, creating')
        try:
            octane.Meter.create(**meter)  # convert dictionary to keyword args
            print(f'[octane] Meter "{name}" successfully created')
        except octane.error.APIError as e:
            print(e.http_body)
            raise Exception("Unable to create meter")


def check_octane_resource_meter_storage():
    check_octane_resource_meter(
        {
            "name": meter_name_storage,
            "display_name": "Storage in gigabytes",
            "meter_type": "COUNTER",
            "unit_name": "gigabyte",
            "is_incremental": True,
            "expected_labels": ["customer_name"],
        }
    )


def check_octane_resource_meter_bandwidth():
    check_octane_resource_meter(
        {
            "name": meter_name_bandwidth,
            "display_name": "Bandwidth in gigabytes",
            "meter_type": "COUNTER",
            "unit_name": "gigabyte",
            "is_incremental": True,
            "expected_labels": ["customer_name"],
        }
    )


def check_octane_resource_meter_machines():
    check_octane_resource_meter(
        {
            "name": meter_name_machines,
            "display_name": "Number of machines",
            "meter_type": "COUNTER",
            "is_incremental": True,
            "expected_labels": ["customer_name"],
        }
    )


def check_octane_resource_price_plan():
    print(f'[octane] Checking if price plan "{price_plan_name}" exists')
    try:
        octane.PricePlan.retrieve(price_plan_name)
        print(f'[octane] Price plan "{price_plan_name}" already exists')
    except octane.error.APIError as e:
        if e.http_status == 401:
            raise Exception("Unauthorized, please check your OCTANE_API_KEY.")
        print(
            f'[octane] Price plan "{price_plan_name}" does not exist, creating'
        )
        try:
            octane.PricePlan.create(
                name=price_plan_name,
                period="month",
                metered_components=[
                    {
                        "meter_name": meter_name_storage,
                        "price_scheme": {
                            "prices": [
                                {"price": int(meter_rate_storage) * 100}
                            ],
                            "scheme_type": "FLAT",
                            "unit_name": "gigabyte",
                        },
                    },
                    {
                        "meter_name": meter_name_bandwidth,
                        "price_scheme": {
                            "prices": [
                                {"price": int(meter_rate_bandwidth) * 100}
                            ],
                            "scheme_type": "FLAT",
                            "unit_name": "gigabyte",
                        },
                    },
                    {
                        "meter_name": meter_name_machines,
                        "price_scheme": {
                            "prices": [
                                {"price": int(meter_rate_machines) * 100}
                            ],
                            "scheme_type": "FLAT",
                        },
                    },
                ],
            )
            print(
                f'[octane] Price plan "{price_plan_name}" successfully created'
            )
        except octane.error.APIError as e:
            print(e.http_body)
            raise Exception("Unable to create price plan")


if __name__ == "__main__":
    check_octane_api_key()
    check_octane_resource_meter_storage()
    check_octane_resource_meter_bandwidth()
    check_octane_resource_meter_machines()
    check_octane_resource_price_plan()
    print(f"[server] Listening at http://{bind}:{port}/")
    app.run(host=bind, port=port)
