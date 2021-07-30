from __future__ import absolute_import, division, print_function

import os

# Octane Python bindings
# API docs at http://getoctane.io/docs/api

# Configuration variables

api_key = None
client_id = None
api_base = "https://api.cloud.getoctane.io"
api_version = None
verify_ssl_certs = True
proxy = None
default_http_client = None
app_info = None
enable_telemetry = True
max_network_retries = 2
ca_bundle_path = os.path.join(
    os.path.dirname(__file__), "data", "ca-certificates.crt"
)

# Set to either 'debug' or 'info', controls console logging
log = None

# API resources
from octane.api_resources import *  # noqa


# Sets some basic information about the running application that's sent along
# with API requests. Useful for plugin authors to identify their plugin when
# communicating with Octane.
#
# Takes a name and optional version and plugin URL.
def set_app_info(name, partner_id=None, url=None, version=None):
    global app_info
    app_info = {
        "name": name,
        "partner_id": partner_id,
        "url": url,
        "version": version,
    }
