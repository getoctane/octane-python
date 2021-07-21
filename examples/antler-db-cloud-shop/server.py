#!/usr/bin/env python

import octane
from os import getenv
from flask import Flask, send_from_directory

octane.api_key = getenv("OCTANE_API_KEY")

app = Flask("antler-db-cloud-shop")

# Application settings and defaults
port = getenv("APP_PORT", 3000)
bind = getenv("APP_BIND", "127.0.0.1")
octane_redirect_url = getenv("OCTANE_REDIRECT_URL", "https://cloud.getoctane.io")
price_plan_name = getenv("OCTANE_PRICE_PLAN_NAME", "antlerdb")
meter_name_storage = getenv("OCTANE_METER_NAME_STORAGE", "storage")
meter_name_bandwidth = getenv("OCTANE_METER_NAME_BANDWIDTH", "bandwidth")
meter_name_machines = getenv("OCTANE_METER_NAME_MACHINES", "machines")
meter_rate_storage = getenv("env.OCTANE_METER_RATE_STORAGE", 2)
meter_rate_bandwidth = getenv("env.OCTANE_METER_RATE_BANDWIDTH", 5)
meter_rate_machines = getenv("env.OCTANE_METER_RATE_MACHINES", 10)


@app.route("/")
@app.route("/index.html")
def public_index_html():
    return send_from_directory("public", "index.html")


@app.route("/scripts.js")
def public_scripts_js():
    return send_from_directory("public", "scripts.js")


@app.route("/styles.css")
def public_styles_css():
    return send_from_directory("public", "styles.css")


def check_octane_api_key():
    if not octane.api_key:
        raise Exception("Must set OCTANE_API_KEY.")


def check_octane_resource_meter(meter):
    name = meter["name"]
    print(f"[octane] Checking if meter \"{name}\" exists")
    try:
        octane.Meter.retrieve(name)
        print(f"[octane] Meter \"{name}\" already exists")
    except octane.error.APIError as e:
        if e.http_status == 401:
            raise Exception("Unauthorized, please check your OCTANE_API_KEY.")
        print(f"[octane] Meter \"{name}\" does not exist, creating")
        try:
            octane.Meter.create(**meter)
            print(f"[octane] Meter \"{name}\" successfully created")
        except octane.error.APIError as e:
            print(e.http_body)
            raise Exception("Unable to create meter")


def check_octane_resource_meter_storage():
    check_octane_resource_meter({
        "name": meter_name_storage,
        "display_name": "Storage in gigabytes",
        "meter_type": "COUNTER",
        "unit_name": "gigabyte",
        "is_incremental": True,
        "expected_labels": ["customer_name"]
    })


def check_octane_resource_meter_bandwidth():
    check_octane_resource_meter({
        "name": meter_name_bandwidth,
        "display_name": "Bandwidth in gigabytes",
        "meter_type": "COUNTER",
        "unit_name": "gigabyte",
        "is_incremental": True,
        "expected_labels": ["customer_name"],
    })


def check_octane_resource_meter_machines():
    check_octane_resource_meter({
        "name": meter_name_machines,
        "display_name": "Number of machines",
        "meter_type": "COUNTER",
        "is_incremental": True,
        "expected_labels": ["customer_name"],
    })


def check_octane_resource_price_plan():
    pass


if __name__ == "__main__":
    check_octane_api_key()
    check_octane_resource_meter_storage()
    check_octane_resource_meter_bandwidth()
    check_octane_resource_meter_machines()
    check_octane_resource_price_plan()
    print(f"[server] Listening at http://{bind}:{port}/")
    app.run(host=bind, port=port)
