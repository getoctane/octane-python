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
max_network_retries = 0
ca_bundle_path = os.path.join(
    os.path.dirname(__file__), "data", "ca-certificates.crt"
)

# Octane reporting configuration
octane_tags = []
session_id = ""
consent = None
reporter = None
try:
    import uuid

    from humbug.consent import HumbugConsent, environment_variable_opt_out, no
    from humbug.report import HumbugReporter

    from octane.version import VERSION

    octane_tags = ["version:{}".format(VERSION)]

    session_id = str(uuid.uuid4())

    reporter_token = "8fffe9ff-a402-4f8b-a3b3-c7706ba935fc"

    consent = HumbugConsent(environment_variable_opt_out("OCTANE_REPORTING_ENABLED", no))
    reporter = HumbugReporter(
        "octane",
        consent,
        client_id=client_id,
        session_id=session_id,
        bugout_token=reporter_token
    )

    reporter.system_report(tags=octane_tags)
    reporter.setup_excepthook(tags=octane_tags)
except:
    pass

enable_telemetry = True if consent is None else consent.check()

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
