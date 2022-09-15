from .nodes import NodesView
from .imports_nodes import ImportsView
from .delete_node import DeleteNodeView

HANDLERS = (
    NodesView, ImportsView, DeleteNodeView
)
