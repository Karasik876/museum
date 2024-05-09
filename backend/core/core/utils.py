import json
from django.core.cache import cache
from django.conf import settings
import boto3
import uuid
from opentelemetry import trace


def add_open_telemetry_spans(_, __, event_dict):
    span = trace.get_current_span()
    if not span.is_recording():
        return event_dict

    ctx = span.get_span_context()
    parent = getattr(span, "parent", None)

    event_dict["span_id"] = f"{ctx.span_id:x}"
    event_dict["trace_id"] = f"{ctx.trace_id:x}"
    if parent:
        event_dict["parent_span_id"] = f"{parent.span_id:x}"

    return event_dict


def delete_cache(key_prefix: str):
    keys_pattern = f"views.decorators.cache.cache_*.{key_prefix}.*.{settings.LANGUAGE_CODE}.{settings.TIME_ZONE}"
    cache.delete_pattern(keys_pattern)


def upload_image(img, app: str):
    key = f'{app}/{uuid.uuid4()}.png'
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url=settings.AWS_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS,
        aws_secret_access_key=settings.AWS_SECRET,
    )
    s3.put_object(Body=img, Bucket='digital-portfolio', Key=key)
    return f'{settings.AWS_URL}{key}'