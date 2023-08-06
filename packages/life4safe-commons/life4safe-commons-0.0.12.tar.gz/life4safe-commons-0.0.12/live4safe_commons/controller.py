from flask import Flask, Response, request
from flask_restx import Api, Resource
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
from live4safe_commons.server_instance import server

app, api = server.app , server.api

_INF = float("inf")

graphs = {}
graphs['c'] = Counter('python_request_operations_total', 'The total number of processed requests')
graphs['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds.', buckets=(1, 2, 5, 6, 10, _INF))

@api.route('/health-check')
class HealthCheck(Resource):
    def get(self):
        return {'status':'ok'},200
    
    @app.route("/metrics")
    def requests_count():
        res = []
        for k,v in graphs.items():
            res.append(prometheus_client.generate_latest(v))
        return Response(res, mimetype="text/plain")