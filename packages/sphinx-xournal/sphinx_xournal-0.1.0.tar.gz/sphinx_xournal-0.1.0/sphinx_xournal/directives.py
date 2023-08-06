from typing import Any, Sequence
from docutils.nodes import Node, image as docutils_image
from docutils.parsers.rst.directives.images import Image
from docutils.parsers.rst.directives.misc import Raw
from sphinx.directives.patches import Figure
from sphinx.util.docutils import SphinxDirective
from docutils.parsers.rst import directives

OUTPUT_FILE_TYPES = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "svg": "image/svg+xml",
}


def format_spec(argument: Any) -> str:
    """Check if the argument is in the list of available output format file types."""
    return directives.choice(argument, list(OUTPUT_FILE_TYPES.keys()))


class XournalBaseDirective(SphinxDirective):
    option_spec = {"format": format_spec}

    def traverse(self, nodes):
        """Traverse all the nodes in depth first fashion."""
        for node in nodes:
            yield node
            yield from self.traverse(node.children)

    def run(self) -> Sequence[Node]:
        """Find the image node and mark it for conversion."""
        nodes = super().run()
        for node in self.traverse(nodes):
            if isinstance(node, docutils_image):
                node["classes"].append("xournal")
                break
        return nodes


class XournalImageDirective(XournalBaseDirective, Image):
    option_spec = Image.option_spec.copy()
    option_spec.update(XournalBaseDirective.option_spec)


class XournalFigureDirective(XournalBaseDirective, Figure):
    option_spec = Figure.option_spec.copy()
    option_spec.update(XournalBaseDirective.option_spec)


class XournalRawDirective(XournalBaseDirective, Raw):
    option_spec = Raw.option_spec.copy()
    option_spec.update(XournalBaseDirective.option_spec)
