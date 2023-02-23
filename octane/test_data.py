from datetime import timedelta
import dateutil.parser
import time

import octane

octane.api_base = "http://localhost:8080"
octane.api_key = (
    "9aed8aec1b625359132245af12e8108f71ccb9b58b705f18845d9a5fd89cc362"
)

NUM_CUSTOMERS = 100
NUM_SOURCES = 10


def customer_name(i):
    return "customer_{i}".format(i=i)


for i in range(NUM_CUSTOMERS):
    name = customer_name(i)
    octane.Customer.create(name=name, display_name="Customer {i}".format(i=i))
    octane.Customer.create_mapping(name, label="customer", value_regex="name")

count = 0
d = dateutil.parser.isoparse("2021-03-25T00:00:00Z")
while True:
    for i in range(NUM_CUSTOMERS):
        for j in range(NUM_SOURCES):
            octane.Measurement.create(
                meter_name="tot_gauge_meter",
                time=d.isoformat(),
                value=i * count,
                labels={
                    "name": customer_name(i),
                    "source": "source_{j}".format(j=j),
                },
            )
    count += 1
    d += timedelta(minutes=1)
    time.sleep(10)
