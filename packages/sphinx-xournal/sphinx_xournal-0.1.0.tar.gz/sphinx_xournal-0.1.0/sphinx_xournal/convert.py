import os
import subprocess
from hashlib import sha1
from pathlib import Path
from subprocess import PIPE
from typing import Any, List
from docutils import nodes
from sphinx.builders import Builder
from sphinx.transforms.post_transforms.images import ImageConverter, get_filename_for
from sphinx_xournal.directives import OUTPUT_FILE_TYPES
from sphinx_xournal.exceptions import XournalCallError, XournalError


class XournalConverter(ImageConverter):
    """Convert xournal (xopp) gzipped files to images."""
    conversion_rules = [("application/gzip", output_type) for output_type in OUTPUT_FILE_TYPES.values()]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def is_available(self) -> bool:
        """Check if we can use this converter."""
        return True

    def guess_mimetypes(self, node: nodes.image) -> List[str]:
        """Should always be application/gzip unless a wrong file got passed in."""
        return ["application/gzip"]

    def handle(self, node: nodes.image) -> None:
        """Find out if we can convert the file and do so."""
        candidates = node.get("candidates", {})
        from_type, to_type = self.get_conversion_rule(node)
        source_path = candidates.get(from_type, candidates["*"])
        absolute_source_path = Path(self.app.srcdir) / source_path
        if not absolute_source_path.exists():
            raise XournalError(f"File '{absolute_source_path}' does not exist")
        out_filename = get_filename_for(source_path, to_type)
        options = node.attributes
        destination_path = str(self.generate(absolute_source_path, options, out_filename))
        node["candidates"][to_type] = destination_path
        node["uri"] = destination_path
        self.env.original_image_uri[destination_path] = source_path
        self.env.images.add_file(self.env.docname, destination_path)

    @staticmethod
    def is_cached(file_path: Path, input_abspath: Path) -> bool:
        """Check if we can reuse the cached image."""
        return file_path.exists() and file_path.stat().st_mtime > input_abspath.stat().st_mtime

    @staticmethod
    def hash_image(input_abspath: Path, builder: Builder, options: dict) -> str:
        """Return the unique hash of the image and its properties."""
        input_relpath = input_abspath.relative_to(builder.srcdir)
        page = str(options.get("page", 0))
        unique_values = (str(input_relpath), page)
        hash_key = "\n".join(unique_values)
        sha_key = sha1(hash_key.encode()).hexdigest()
        return sha_key

    def generate(self, input_abspath: Path, options: dict, out_filename: str) -> Path:
        """"""
        builder = self.app.builder
        sha_key = self.hash_image(input_abspath, builder, options)
        output_image_file_path = Path(self.imagedir) / sha_key / out_filename
        output_image_file_path.parent.mkdir(parents=True, exist_ok=True)
        if self.is_cached(output_image_file_path, input_abspath):
            return output_image_file_path
        binary_path = builder.config.xournal_binary_path
        xournal_args = [binary_path, "--create-img", str(output_image_file_path), str(input_abspath)]
        new_env = os.environ.copy()
        try:
            value = subprocess.run(xournal_args, stderr=PIPE, stdout=PIPE, check=True, env=new_env)
        except OSError as exc:
            raise XournalCallError(binary_path, xournal_args, exc)
        except subprocess.CalledProcessError as exc:
            raise XournalCallError(binary_path, xournal_args, exc.returncode, exc.stderr, exc.stdout)
        return output_image_file_path

    @property
    def imagedir(self) -> str:
        """"""
        return str(Path(self.app.doctreedir) / Path("xournal"))
