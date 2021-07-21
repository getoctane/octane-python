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
        "message": "Python version does not yet support customer deletion"
    }, 501
    # TODO: uncomment below
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

def check_octane_api_key():
    if not octane.api_key:
        raise Exception("Must set OCTANE_API_KEY.")


if __name__ == "__main__":
    check_octane_api_key()
    print(f"[server] Listening at http://{bind}:{port}/")
    app.run(host=bind, port=port)
