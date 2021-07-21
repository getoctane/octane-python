#!/usr/bin/env python

import octane
from os import getenv
from flask import Flask, request, make_response, send_from_directory

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


def check_octane_api_key():
    if not octane.api_key:
        raise Exception("Must set OCTANE_API_KEY.")


if __name__ == "__main__":
    check_octane_api_key()
    print(f"[server] Listening at http://{bind}:{port}/")
    app.run(host=bind, port=port)
