from __future__ import absolute_import, division, print_function

import os

import octane


octane.api_key = os.environ.get("OCTANE_SECRET_KEY")

print("Attempting to create customer...")

resp = octane.Customer.create(
    name="Customer1",
)

print("Success: %r" % (resp))
