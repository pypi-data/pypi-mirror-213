import shutil
from pathlib import Path
from typing import Dict, Any
from sphinx_xournal import __version__
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.util.fileutil import copy_asset
from sphinx_xournal.convert import XournalConverter
from sphinx_xournal.directives import XournalImageDirective, XournalFigureDirective, XournalRawDirective


def on_config_inited(app: Sphinx, config: Config) -> None:
    """No need to do anything at the moment."""
    return


def on_build_finished(app: Sphinx, exc: Exception) -> None:
    """Copy over any remaining static files."""
    source = Path(__file__).absolute().parent / Path("xournal.css")
    destination = Path(app.outdir) / Path("_static/css")
    copy_asset(str(source), str(destination))


def setup(app: Sphinx) -> Dict[str, Any]:
    """Sphinx hook entrypoint."""
    app.add_post_transform(XournalConverter)
    app.add_directive("xournal-image", XournalImageDirective)
    app.add_directive("xournal-figure", XournalFigureDirective)
    app.add_directive("xournal-raw", XournalRawDirective)
    xournal_binary_path = shutil.which("xournalpp")
    app.add_config_value("xournal_binary_path", xournal_binary_path, "html")
    app.connect("build-finished", on_build_finished)
    app.connect("config-inited", on_config_inited)
    app.add_css_file("css/xournal.css")
    return {"version": __version__, "parallel_read_safe": True, "parallel_write_safe": True}
