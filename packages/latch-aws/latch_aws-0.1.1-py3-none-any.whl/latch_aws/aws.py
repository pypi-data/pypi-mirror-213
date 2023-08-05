import asyncio
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Literal, TypeAlias
from urllib.parse import urlparse

import opentelemetry.context as context
from aiobotocore.client import AioBaseClient
from aiobotocore.config import AioConfig
from aiobotocore.session import get_session
from aiobotocore.signers import AioRequestSigner
from botocore.client import Config
from botocore.exceptions import ClientError
from botocore.session import Session
from latch_data_validation.data_validation import validate
from latch_o11y.o11y import dict_to_attrs, trace_function_with_span
from opentelemetry.sdk.resources import Attributes
from opentelemetry.trace import Span, SpanKind, Status, StatusCode, get_tracer
from types_aiobotocore_s3.client import S3Client
from types_aiobotocore_s3.type_defs import (
    EmptyResponseMetadataTypeDef,
    ResponseMetadataTypeDef,
)

tracer = get_tracer(__name__)

AWSRegion: TypeAlias = (
    Literal["us-east-1"]
    | Literal["us-east-2"]
    | Literal["us-west-1"]
    | Literal["us-west-2"]
    | Literal["af-south-1"]
    | Literal["ap-east-1"]
    | Literal["ap-southeast-1"]
    | Literal["ap-southeast-2"]
    | Literal["ap-southeast-3"]
    | Literal["ap-south-1"]
    | Literal["ap-northeast-3"]
    | Literal["ap-northeast-2"]
    | Literal["ap-northeast-1"]
    | Literal["ca-central-1"]
    | Literal["eu-central-1"]
    | Literal["eu-west-1"]
    | Literal["eu-west-2"]
    | Literal["eu-west-3"]
    | Literal["eu-south-1"]
    | Literal["eu-north-1"]
    | Literal["me-south-1"]
    | Literal["sa-east-1"]
    | Literal["us-gov-east-1"]
    | Literal["us-gov-west-1"]
)

sess = get_session()

max_presigned_url_age = timedelta(days=7) // timedelta(seconds=1)

# >>> TCP Keep-alive
# see https://github.com/boto/botocore/issues/2249 and https://github.com/boto/botocore/pull/2766
# aiobotocore uses a botocore that is really old and so does not have this in the config

_vanilla_get_scoped_config = Session.get_scoped_config


def keep_alive_get_scoped_config(self: Session):
    res = _vanilla_get_scoped_config(self)
    res["tcp_keepalive"] = True
    return res


Session.get_scoped_config = keep_alive_get_scoped_config

# >>> Tracing

_ignore_errors_key = context.create_key("_aws_ignore_errors")

_vanilla_generate_presigned_url = AioRequestSigner.generate_presigned_url

_vanilla_make_api_call = AioBaseClient._make_api_call


def add_response_metadata_attributes(span: Span, meta: ResponseMetadataTypeDef):
    status_code = meta["HTTPStatusCode"]
    if (400 <= status_code <= 499 or 500 <= status_code <= 599) and context.get_value(
        _ignore_errors_key
    ) is not True:
        span.set_status(Status(StatusCode.ERROR, HTTPStatus(status_code).phrase))

    attrs: Attributes = {
        "http.status_code": status_code,
        "rpc.aws-api.request_id": meta["RequestId"],
        "rpc.aws-api.host_id": meta["HostId"],
        # datadog
        "aws.requestid": meta["RequestId"],
    }
    if "x-amz-id-2" in meta["HTTPHeaders"]:
        attrs["rpc.aws-api.request_id_2"] = meta["HTTPHeaders"]["x-amz-id-2"]
        # datadog
        attrs["aws.requestid2"] = meta["HTTPHeaders"]["x-amz-id-2"]
    span.set_attributes(attrs)


async def traced_generate_presigned_url(
    self: AioRequestSigner,
    request_dict,
    operation_name: str,
    expires_in: int = 3600,
    region_name=None,
    signing_name=None,
):
    # todo(maximsmol): add more attributes?
    with tracer.start_as_current_span(
        f"generate_presigned_url.{operation_name}",
        attributes={} | dict_to_attrs(request_dict, "params"),
    ):
        return await _vanilla_generate_presigned_url(
            self, request_dict, operation_name, expires_in, region_name, signing_name
        )


async def traced_make_api_call(self: AioBaseClient, operation_name: str, api_params):
    # todo(maximsmol): add otel attributes
    # http.method
    # http.flavor
    # http.url
    # http.request_content_length
    # http.response_content_length
    # net.peer.port
    # http.retry_count - note: this must be in spans created *per request*
    #   the datadog instrumentation goes against spec here

    endpoint_parts = urlparse(self._endpoint.host)

    port = endpoint_parts.port
    if port is None:
        if endpoint_parts.scheme == "http":
            port = 80
        elif endpoint_parts.scheme == "https":
            port = 443

    endpoint_name = self._endpoint._endpoint_prefix
    with tracer.start_as_current_span(
        f"aws-api.{endpoint_name}/{operation_name}",
        # todo(maximsmol): remove if not needed
        # f"{endpoint_name}.command", # dd span name (kept around in case dd won't recognize the otel one)
        kind=SpanKind.CLIENT,
        attributes={
            # todo(maximsmol): is this service name override a datadog idiosyncrasy?
            "service.name": f"aws.{endpoint_name}",
            "http.scheme": endpoint_parts.scheme,
            "http.host": endpoint_parts.netloc,
            "net.peer.name": str(endpoint_parts.hostname),
            "rpc.method": operation_name,
            "rpc.system": "aws-api",
            "rpc.service": endpoint_name,
            # datadog:
            "span.type": "http",
            "resource.name": f"{endpoint_name}.{operation_name.lower()}",
            "aws.agent": "aiobotocore",
            "aws.operation": operation_name,
            "aws.region": self.meta.region_name,
        }
        | (
            {
                "net.peer.port": port,
            }
            if port is not None
            else {}
        )
        | dict_to_attrs(api_params, "rpc.aws-api.params"),
        set_status_on_exception=context.get_value(_ignore_errors_key) is not True,
    ) as s:
        try:
            res: EmptyResponseMetadataTypeDef = await _vanilla_make_api_call(
                self, operation_name, api_params
            )

            add_response_metadata_attributes(s, res["ResponseMetadata"])

            return res
        except ClientError as e:
            err_res = e.response

            attrs: Attributes = {}
            if "Error" in err_res:
                err = err_res["Error"]
                if "Code" in err:
                    attrs["rpc.aws-api.error_code"] = err["Code"]
                if "Message" in err:
                    attrs["rpc.aws-api.error_message"] = err["Message"]
            if "Status" in err_res:
                attrs["rpc.aws-api.status"] = err_res["Status"]
            if "StatusReason" in err_res:
                attrs["rpc.aws-api.status_reason"] = err_res["StatusReason"]
            s.set_attributes(attrs)

            if "ResponseMetadata" in err_res:
                add_response_metadata_attributes(s, err_res["ResponseMetadata"])

            raise e


AioRequestSigner.generate_presigned_url = traced_generate_presigned_url
AioBaseClient._make_api_call = traced_make_api_call

# >>> Main

_s3_clients: dict[AWSRegion, S3Client] = {}


@trace_function_with_span(tracer)
async def s3_client(s: Span, region: AWSRegion = "us-west-2"):
    s.set_attributes({"rpc.aws-api.region": region, "cached": region in _s3_clients})

    if region not in _s3_clients:
        _s3_clients[region] = await sess.create_client(
            "s3",
            region_name=region,
            config=AioConfig().merge(Config(signature_version="s3v4")),
        ).__aenter__()

    return _s3_clients[region]


async def s3_cleanup():
    async def close_client(region: AWSRegion, x: S3Client):
        with tracer.start_as_current_span(
            "close s3 client", attributes={"rpc.aws-api.region": region}
        ):
            await x.__aexit__(None, None, None)

    deferred: list[asyncio.Task[object]] = []
    for k, v in _s3_clients.items():
        deferred.append(asyncio.create_task(close_client(k, v)))

    await asyncio.gather(*deferred)


_bucket_region_cache: dict[str, tuple[AWSRegion, datetime]] = {}


@trace_function_with_span(tracer)
async def get_bucket_region(
    s: Span,
    *,
    Bucket: str,  # noqa: N803 (variables should be lowercase)
    ExpectedBucketOwner: str | None = None,  # noqa: N803
) -> AWSRegion:
    now = datetime.now()

    cached_value = _bucket_region_cache.get(Bucket)
    if cached_value is not None and cached_value[1] <= now:
        cached_value = None
        del _bucket_region_cache[Bucket]

    s.set_attributes({"bucket": Bucket, "cached": cached_value is not None})
    if cached_value is not None:
        return cached_value[0]

    default_s3 = await s3_client()

    ctx_reset_token: object | None = None
    try:
        new_ctx = context.set_value(_ignore_errors_key, True)
        ctx_reset_token = context.attach(new_ctx)

        if ExpectedBucketOwner is not None:
            head = await default_s3.head_bucket(
                Bucket=Bucket, ExpectedBucketOwner=ExpectedBucketOwner
            )
        else:
            head = await default_s3.head_bucket(Bucket=Bucket)

        region = head["ResponseMetadata"]["HTTPHeaders"]["x-amz-bucket-region"]
    except ClientError as e:
        # the request WILL error for some reason despite returning the correct header

        if e.operation_name != "HeadBucket":
            raise e

        region = (
            e.response.get("ResponseMetadata", {})
            .get("HTTPHeaders", {})
            .get("x-amz-bucket-region")
        )
        if region is None:
            raise e
    finally:
        if ctx_reset_token is not None:
            context.detach(ctx_reset_token)

    res: AWSRegion = validate(region, AWSRegion)
    _bucket_region_cache[Bucket] = (res, now + timedelta(hours=1))
    return res
