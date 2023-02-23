#!/usr/bin/env python

import octane
from os import getenv
from flask import Flask, request, jsonify, make_response, send_from_directory

octane.api_key = getenv("OCTANE_API_KEY")

app = Flask("antler-db-cloud-shop")

# Application settings and defaults
port = getenv("APP_PORT", 3000)
bind = getenv("APP_BIND", "127.0.0.1")
meter_name = getenv("OCTANE_METER_NAME", "hours")
price_plan_name = getenv("OCTANE_PRICE_PLAN_NAME", "standard")
price_plan_rate = getenv("OCTANE_PRICE_PLAN_RATE", 30)


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


@app.route("/api/customers", methods=["GET"])
def api_customers():
    print("[octane] Listing customers in account")
    try:
        customers = octane.Customer.list()
        return jsonify(customers)
    except octane.error.APIError as e:
        print("[octane] Error listing customers in account")
        return e.json_body, e.http_status


@app.route("/api/customers/<name>", methods=["DELETE"])
def api_customers_name_delete(name):
    return {
        "code": 501,
        "status": "Not Implemented",
        "message": "Python version does not yet support customer deletion",
    }, 501

    # TODO: uncomment below once deletion is supported
    """
    print(f"[octane] Attempting to unsubscribe customer \"{name}\" " +
          f"from price plan \"{price_plan_name}\"")
    try:
        octane.Customer.delete_subscription(name)
        print(f"[octane] Customer \"{name}\" successfully unsubscribed " +
              f"from price plan \"{price_plan_name}\"")
        print("f[octane] Attempting to delete customer \"{name}\"")
        try:
            octane.Customer.delete(name)
            return {
                "code": 200,
                "message": "success"
            }
        except octane.error.APIError as e:
            print(f"[octane] Error deleting customer \"{name}\"")
            return e.json_body, e.http_status
    except octane.error.APIError as e:
        print(f"[octane] Error unsubscribing customer \"{name}\" " +
              f"from price plan \"{price_plan_name}\"")
        return e.json_body, e.http_status
    """


@app.route("/api/customers", methods=["POST"])
def api_customers_post():
    data = request.json
    name = data["name"]
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
                f'[octane] Successfully subscribed customer "{name}"'
                + f'to price plan "{price_plan_name}"'
            )
            return {"code": 201, "message": "success"}, 201
        except octane.error.APIError as e:
            print(
                f'[octane] Error subscribing customer "{name}" '
                + f'to price plan "{price_plan_name}"'
            )
            return e.json_body, e.http_status
    except octane.error.APIError as e:
        print('[octane] Error creating customer "{name}"')
        return e.json_body, e.http_status


@app.route("/api/hours", methods=["POST"])
def api_hours_post():
    data = request.json
    name = data["name"]
    hours = data["hours"]
    print(f'[octane] Attempting to create measurement for customer "{name}"')
    try:
        octane.Measurement.create(
            meter_name=meter_name,
            value=int(hours),
            labels={"customer_name": name},
        )
        print(
            f'[octane] Measurement for customer "{name}" successfully created'
        )
        return {"code": 201, "message": "success"}, 201
    except octane.error.APIError as e:
        print('[octane] Error creating measurement for customer "{name}"')
        return e.json_body, e.http_status


def check_octane_api_key():
    if not octane.api_key:
        raise Exception("Must set OCTANE_API_KEY.")


def check_octane_resource_meter():
    print(f'[octane] Checking if meter "{meter_name}" exists')
    try:
        octane.Meter.retrieve(meter_name)
        print(f'[octane] Meter "{meter_name}" already exists')
    except octane.error.APIError as e:
        if e.http_status == 401:
            raise Exception("Unauthorized, please check your OCTANE_API_KEY.")
        print(f'[octane] Meter "{meter_name}" does not exist, creating')
        try:
            octane.Meter.create(
                name=meter_name,
                display_name="Number of hours worked",
                meter_type="COUNTER",
                unit_name="hour",
                is_incremental=True,
                expected_labels=["customer_name"],
            )
            print(f'[octane] Meter "{meter_name}" successfully created')
        except octane.error.APIError as e:
            print(e.http_body)
            raise Exception("Unable to create meter")


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
            rate = int(price_plan_rate) * 100  # convert dollars to cents
            octane.PricePlan.create(
                name=price_plan_name,
                period="month",
                metered_components=[
                    {
                        "meter_name": meter_name,
                        "price_scheme": {
                            "prices": [{"price": rate}],
                            "scheme_type": "FLAT",
                            "unit_name": "hour",
                        },
                    }
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
    check_octane_resource_meter()
    check_octane_resource_price_plan()
    print(f"[server] Listening at http://{bind}:{port}/")
    app.run(host=bind, port=port)
