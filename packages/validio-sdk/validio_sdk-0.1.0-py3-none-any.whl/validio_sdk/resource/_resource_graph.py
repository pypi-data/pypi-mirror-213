import atexit
import json
import os

from validio_sdk.code.settings import dump_graph_var, graph_preamble_var
from validio_sdk.resource._resource import ResourceGraph
from validio_sdk.resource._serde import custom_resource_graph_encoder

"""
This holds a 'global' instance of a resource graph. This is the graph
that represents the code configuration. It is automatically populated
as the code declares resources.
Upon exit of the program, we serialize this instance to the parent process.
"""
RESOURCE_GRAPH: ResourceGraph = ResourceGraph()


def _dump_graph():
    # Since we piggyback on stdout, we prefix the graph with a
    # preamble to identify the start of the relevant info in the stream.
    if dump_graph_var in os.environ:
        print(graph_preamble_var)
        print(
            json.dumps(RESOURCE_GRAPH, default=custom_resource_graph_encoder, indent=2)
        )


atexit.register(_dump_graph)
