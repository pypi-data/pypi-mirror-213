import inspect
from typing import cast

# We need to import the validio_sdk module due to the `eval`
# ruff: noqa: F401
import validio_sdk
from validio_sdk.graphql_client import (
    GraphQLClientHttpError,
    ListCredentialsCredentialsListAwsRedshiftCredential,
    ListCredentialsCredentialsListPostgreSqlCredential,
    ListCredentialsCredentialsListSnowflakeCredential,
    ReferenceSourceConfigDetails,
)
from validio_sdk.resource._diff import (
    DiffContext,
    GraphDiff,
    ResourceUpdates,
)
from validio_sdk.resource._diff_util import (
    must_find_destination,
    must_find_segmentation,
    must_find_source,
    must_find_window,
)
from validio_sdk.resource._resource import Resource, ResourceGraph
from validio_sdk.resource._util import _sanitize_error
from validio_sdk.resource.credentials import (
    AwsRedshiftCredential,
    Credential,
    DemoCredential,
    GcpCredential,
    PostgreSqlCredential,
    SnowflakeCredential,
)
from validio_sdk.resource.destinations import Destination
from validio_sdk.resource.segmentations import Segmentation
from validio_sdk.resource.sources import Source
from validio_sdk.resource.thresholds import (
    THRESHOLD_CLASSES,
    Threshold,
)
from validio_sdk.resource.validators import VALIDATOR_CLASSES, Reference
from validio_sdk.resource.windows import WINDOW_CLASSES, Window
from validio_sdk.validio_client import ValidioAPIClient


async def load_resources(namespace: str, client: ValidioAPIClient) -> DiffContext:
    g = ResourceGraph()
    ctx = DiffContext(
        credentials={},
        sources={},
        destinations={},
        segmentations={},
        windows={},
        validators={},
    )

    # Ordering matters here - we need to load parent resources before children
    await load_credentials(namespace, client, g, ctx)
    await load_channels(namespace, client, g, ctx)
    await load_destinations(namespace, client, ctx)
    await load_sources(namespace, client, ctx)
    await load_segmentations(namespace, client, ctx)
    await load_windows(namespace, client, ctx)
    await load_validators(namespace, client, ctx)
    await load_notification_rules_v2(namespace, client, ctx)

    return ctx


async def load_credentials(
    # ruff: noqa: ARG001
    namespace: str,
    client: ValidioAPIClient,
    g: ResourceGraph,
    ctx: DiffContext,
):
    credentials = await client.list_credentials()

    for c in credentials:
        name = c.resource_name

        # The 'secret' parts of a credential are left unset since they are not
        # provided by the API. We check for changes to them specially.
        match c.typename__:
            case "DemoCredential":
                credential: Credential = DemoCredential(name=name, __internal__=g)
            case "GcpCredential":
                credential = GcpCredential(
                    name=name, credential="UNSET", __internal__=g
                )
            case "PostgreSqlCredential":
                c = cast(ListCredentialsCredentialsListPostgreSqlCredential, c)
                credential = PostgreSqlCredential(
                    name=name,
                    host=c.config.host,
                    port=c.config.port,
                    user=c.config.user,
                    password="UNSET",
                    default_database=c.config.default_database,
                    __internal__=g,
                )
            case "AwsRedshiftCredential":
                c = cast(ListCredentialsCredentialsListAwsRedshiftCredential, c)
                credential = AwsRedshiftCredential(
                    name=name,
                    host=c.config.host,
                    port=c.config.port,
                    user=c.config.user,
                    password="UNSET",
                    default_database=c.config.default_database,
                    __internal__=g,
                )
            case "SnowflakeCredential":
                c = cast(ListCredentialsCredentialsListSnowflakeCredential, c)
                credential = SnowflakeCredential(
                    name=name,
                    account=c.config.account,
                    user=c.config.user,
                    password="UNSET",
                )
            case _:
                raise RuntimeError(
                    f"unsupported credential '{name}' of type '{type(c)}'"
                )

        credential._id.value = c.id
        credential._namespace = c.resource_namespace

        ctx.credentials[name] = credential


async def load_channels(
    namespace: str,
    client: ValidioAPIClient,
    g: ResourceGraph,
    ctx: DiffContext,
):
    # We need to import the module due to the `eval`
    # ruff: noqa: F401
    from validio_sdk.resource import channels

    server_channels = await client.get_channels()

    for ch in server_channels:
        name = ch.resource_name

        cls = eval(f"validio_sdk.resource.channels.{ch.typename__}")
        channel = cls(
            **{
                **ch.config.__dict__,  # type: ignore
                "name": name,
                "__internal__": g,
            }
        )
        channel._id.value = ch.id
        channel._namespace = ch.resource_namespace
        ctx.channels[name] = channel


async def load_notification_rules_v2(
    namespace: str,
    client: ValidioAPIClient,
    ctx: DiffContext,
):
    # We need to import the module due to the `eval`
    # ruff: noqa: F401
    from validio_sdk.resource import notification_rules_v2

    rules = await client.get_notification_rules_v2()

    source_lookup_by_id = {s._must_id(): s for s in ctx.sources.values()}
    for r in rules:
        name = r.resource_name

        cls = eval(f"validio_sdk.resource.notification_rules_v2.{r.typename__}")
        fields = list(inspect.signature(cls).parameters)
        rule = cls(
            **{
                **{
                    f: getattr(r, f)
                    for f in fields
                    if f not in {"name", "channel", "sources"}
                },
                "name": name,
                "channel": ctx.channels[r.channel.resource_name],
                "sources": [
                    ctx.sources[sid]
                    for sid in r.sources
                    if sid and sid in source_lookup_by_id
                ],
            }
        )
        rule._id.value = r.id
        rule._namespace = r.resource_namespace
        ctx.notification_rules_v2[name] = rule


async def load_destinations(
    namespace: str,
    client: ValidioAPIClient,
    ctx: DiffContext,
):
    # We need to import the module due to the `eval`
    # ruff: noqa: F401
    from validio_sdk.resource import destinations

    server_destinations = await client.list_destinations()

    for d in server_destinations:
        name = d.resource_name

        cls = eval(f"validio_sdk.resource.destinations.{d.typename__}")
        destination = cls(
            **{
                **d.config.__dict__,  # type: ignore
                "name": name,
                "credential": ctx.credentials[d.credential.resource_name],
            }
        )
        destination._id.value = d.id
        destination._namespace = d.resource_namespace
        ctx.destinations[name] = destination


async def load_sources(
    namespace: str,
    client: ValidioAPIClient,
    ctx: DiffContext,
):
    # We need to import the module due to the `eval`
    # ruff: noqa: F401
    from validio_sdk.resource import sources

    server_sources = await client.list_sources()

    for s in server_sources:
        name = s.resource_name

        cls = eval(f"validio_sdk.resource.sources.{s.typename__}")
        params = s.config.__dict__ if hasattr(s, "config") else {}
        source = cls(
            **{
                **params,
                "name": name,
                "credential": ctx.credentials[s.credential.resource_name],
                "jtd_schema": s.jtd_schema,
            }
        )
        source._id.value = s.id
        source._namespace = s.resource_namespace
        ctx.sources[name] = source


async def load_segmentations(
    namespace: str,
    client: ValidioAPIClient,
    ctx: DiffContext,
):
    # We need to import the module due to the `eval`
    # ruff: noqa: F401
    from validio_sdk.resource import segmentations

    server_segmentations = await client.list_segmentations()

    for s in server_segmentations:
        name = s.resource_name

        segmentation = Segmentation(
            name=name,
            source=must_find_source(ctx, s.source.resource_name),
            fields=s.fields,
        )

        segmentation._id.value = s.id
        segmentation._namespace = s.resource_namespace
        ctx.segmentations[name] = segmentation


async def load_windows(
    namespace: str,
    client: ValidioAPIClient,
    ctx: DiffContext,
):
    # We need to import the module due to the `eval`
    # ruff: noqa: F401
    from validio_sdk.resource import windows

    server_windows = await client.list_windows()

    for w in server_windows:
        name = w.resource_name

        cls = None
        for c in WINDOW_CLASSES:
            if w.typename__ == c.__name__:
                cls = c
                break

        if cls is None:
            raise RuntimeError(
                f"missing implementation for window type {w.__class__.__name__}"
            )

        window = cls(
            **{
                **w.config.__dict__,  # type:ignore
                "name": name,
                "source": must_find_source(ctx, w.source.resource_name),
                "data_time_field": w.data_time_field,
            }
        )

        window._id.value = w.id
        window._namespace = w.resource_namespace
        ctx.windows[name] = window


# Takes in a graphql Threshold type
def convert_threshold(t: object) -> Threshold:
    graphql_class_name: str = t.__class__.__name__
    cls = None
    for c in THRESHOLD_CLASSES:
        if graphql_class_name.endswith(c.__name__):
            cls = c
            break

    if cls is None:
        raise RuntimeError(
            f"missing implementation for threshold type {graphql_class_name}"
        )

    # Threshold parameters map 1-1 with resources, so
    # we call the constructor directly.
    return cls(**{k: v for k, v in t.__dict__.items() if k != "typename__"})


# Takes in a graphql ReferenceSourceConfig type
def convert_reference(ctx: DiffContext, r: ReferenceSourceConfigDetails) -> Reference:
    source = must_find_source(ctx, r.source.resource_name)
    window = must_find_window(ctx, r.window.resource_name)

    return Reference(
        source=source,
        window=window,
        history=r.history,
        offset=r.offset,
        filter=r.filter,
    )


async def load_validators(
    namespace: str,
    client: ValidioAPIClient,
    ctx: DiffContext,
):
    for source in ctx.sources.values():
        validators = await client.list_validators(source._must_id())

        for v in validators:
            name = v.resource_name

            cls = None
            for c in VALIDATOR_CLASSES:
                if v.typename__ == c.__name__:
                    cls = c
                    break

            if cls is None:
                raise RuntimeError(
                    f"missing implementation for validator type {v.typename__}"
                )

            window = must_find_window(ctx, v.source_config.window.resource_name)
            segmentation = must_find_segmentation(
                ctx, v.source_config.segmentation.resource_name
            )
            maybe_destination = (
                must_find_destination(ctx, v.destination.name)
                if hasattr(v, "destination") and v.destination
                else None
            )

            threshold = convert_threshold(v.config.threshold)  # type:ignore
            maybe_reference = (
                {
                    "reference": convert_reference(
                        ctx, v.reference_source_config  # type: ignore
                    )
                }
                if hasattr(v, "reference_source_config")
                else {}
            )
            maybe_filter = (
                {"filter": v.source_config.filter}
                if hasattr(v.source_config, "filter")
                else {}
            )

            # These are named inconsistently in the list apis, so we treat
            # them specially.
            metric_names = {
                "metric",
                "relative_volume_metric",
                "volume_metric",
                "distribution_metric",
                "numeric_anomaly_metric",
                "relative_time_metric",
                "categorical_distribution_metric",
            }

            config = {}
            for f, config_value in v.config.__dict__.items():  # type: ignore
                if f == "threshold":
                    continue
                if f in metric_names:
                    config["metric"] = config_value
                else:
                    config[f] = config_value

            validator = cls(
                **{
                    **config,
                    **maybe_reference,
                    **maybe_filter,
                    "threshold": threshold,
                    "name": name,
                    "window": window,
                    "segmentation": segmentation,
                    **({"destination": maybe_destination} if maybe_destination else {}),
                }
            )
            validator._id.value = v.id
            validator._namespace = v.resource_namespace
            ctx.validators[name] = validator


async def apply_updates_on_server(
    namespace: str,
    ctx: DiffContext,
    diff: GraphDiff,
    client: ValidioAPIClient,
    show_secrets: bool,
):
    try:
        await apply_deletes(namespace=namespace, deletes=diff.to_delete, client=client)
        await apply_creates(
            namespace=namespace,
            manifest_ctx=ctx,
            creates=diff.to_create,
            client=client,
            show_secrets=show_secrets,
        )
        await apply_updates(
            namespace=namespace, manifest_ctx=ctx, updates=diff.to_update, client=client
        )
    except GraphQLClientHttpError as e:
        raise RuntimeError(f"API error: ({e.status_code}: {e.response.json()})")


async def apply_deletes(namespace: str, deletes: DiffContext, client: ValidioAPIClient):
    # Delete notification rules first These reference sources so we
    # remove them before removing the sources they reference.
    for r in deletes.notification_rules_v2.values():
        await r._api_delete(client)

    # For pipeline resources, start with sources (This cascades deletes,
    # so we don't have to individually delete child resources).
    for s in deletes.sources.values():
        await s._api_delete(client)

    # For child resources, we only need to delete them if their parent
    # haven't been deleted.
    for w in deletes.windows.values():
        if w.source_name not in deletes.sources:
            await w._api_delete(client)

    for sg in deletes.segmentations.values():
        if sg.source_name not in deletes.sources:
            await sg._api_delete(client)

    for v in deletes.validators.values():
        if v.source_name not in deletes.sources:
            await v._api_delete(client)

    # Next, delete destinations. Validators are deleted before we
    # delete potentially attached destinations.
    for d in deletes.destinations.values():
        await d._api_delete(client)

    # Finally delete credentials - these do not cascade so the api rejects any
    # delete requests if there are existing child resources attached to a credential.
    for c in deletes.credentials.values():
        await c._api_delete(client)

    for ch in deletes.channels.values():
        await ch._api_delete(client)


async def apply_creates(
    namespace: str,
    manifest_ctx: DiffContext,
    creates: DiffContext,
    client: ValidioAPIClient,
    show_secrets: bool,
):
    # Creates must be applied top-down, parent first before child resources
    all_resources: list[list[Resource]] = [
        list(creates.credentials.values()),
        list(creates.sources.values()),
        list(creates.destinations.values()),
        list(creates.segmentations.values()),
        list(creates.windows.values()),
        list(creates.validators.values()),
        list(creates.channels.values()),
        list(creates.notification_rules_v2.values()),
    ]
    for resources in all_resources:
        for r in resources:
            try:
                await r._api_create(namespace, client, manifest_ctx)
            except GraphQLClientHttpError as e:
                raise (
                    _sanitize_error(e, show_secrets) if isinstance(r, Credential) else e
                )


async def apply_updates(
    namespace: str,
    manifest_ctx: DiffContext,
    updates: ResourceUpdates,
    client: ValidioAPIClient,
):
    all_updates = [
        list(updates.credentials.values()),
        list(updates.destinations.values()),
        list(updates.sources.values()),
        list(updates.segmentations.values()),
        list(updates.windows.values()),
        list(updates.validators.values()),
        list(updates.channels.values()),
        list(updates.notification_rules_v2.values()),
    ]

    for up in all_updates:
        for u in up:
            await u.manifest.resource._api_update(namespace, client, manifest_ctx)
