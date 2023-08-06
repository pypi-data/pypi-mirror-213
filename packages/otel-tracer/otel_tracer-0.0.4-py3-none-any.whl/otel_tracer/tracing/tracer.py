from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.pika import PikaInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor


def flask_tracer(app, servicename, endpoint):
    FlaskInstrumentor().instrument_app(app)

    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({"service.name": servicename})
        )
    )

    otlp_exporter = OTLPSpanExporter(
        endpoint=endpoint  # Use the address and port of your OpenTelemetry Collector
    )
    span_processor = BatchSpanProcessor(otlp_exporter)

    trace.get_tracer_provider().add_span_processor(span_processor)
    return app


def requests_tracer():
    RequestsInstrumentor().instrument()


def redis_tracer():
    RedisInstrumentor().instrument()


def pika_tracer():
    PikaInstrumentor().instrument()


def celery_tracer():
    from opentelemetry.instrumentation.celery import CeleryInstrumentor
    CeleryInstrumentor().instrument()


def flask_sqlalchemy_tracer():
    from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
    SQLAlchemyInstrumentor().instrument(enable_commenter=True, commenter_options={})
