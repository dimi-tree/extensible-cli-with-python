#!/usr/bin/env python3
import connexion
from connexion import NoContent

# memory-only metric storage
METRICS = []


def post_metrics():
    global METRICS
    METRICS = METRICS + connexion.request.json['metrics']
    print(METRICS)
    return NoContent, (200)


app = connexion.App(__name__, specification_dir='../openapi/')
app.add_api('telemetry.yml')
app.run(port=8080)
