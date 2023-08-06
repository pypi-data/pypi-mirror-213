from validio_sdk.resource._resource import DiffContext
from validio_sdk.resource.destinations import Destination
from validio_sdk.resource.segmentations import Segmentation
from validio_sdk.resource.sources import Source
from validio_sdk.resource.windows import Window


def must_find_source(ctx: DiffContext, name: str) -> Source:
    if name not in ctx.sources:
        raise RuntimeError(f"could not find Source '{name}' in server resource list")
    return ctx.sources[name]


def must_find_window(ctx: DiffContext, name: str) -> Window:
    if name not in ctx.windows:
        raise RuntimeError(f"could not find Window '{name}' in server resource list")
    return ctx.windows[name]


def must_find_segmentation(ctx: DiffContext, name: str) -> Segmentation:
    if name not in ctx.segmentations:
        raise RuntimeError(
            f"could not find Segmentation '{name}' in server resource list"
        )
    return ctx.segmentations[name]


def must_find_destination(ctx: DiffContext, name: str) -> Destination:
    if name not in ctx.destinations:
        raise RuntimeError(
            f"could not find Destination '{name}' in server resource list"
        )
    return ctx.destinations[name]
