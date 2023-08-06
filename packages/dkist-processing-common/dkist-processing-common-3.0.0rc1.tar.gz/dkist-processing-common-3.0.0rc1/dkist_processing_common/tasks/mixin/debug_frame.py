"""Helper to handling saving debug output frames."""
import logging

import numpy as np
from astropy.io import fits
from astropy.io.fits import Header

from dkist_processing_common.codecs.fits import fits_array_encoder
from dkist_processing_common.models.tags import Tag

logger = logging.getLogger(__name__)


class DebugFrameMixin:
    """
    Mixin for writing arrays as 'debug' outputs.

    There are two important properties of debug frames:

    1. They are tagged with DEBUG and thus easily retrievable by downstream tasks.

    2. They have expressive file names. These names can either be specified exactly by the user or automatically generated
       based on the other tags.
    """

    def debug_frame_write_array(
        self,
        array: np.ndarray,
        header: Header | None = None,
        name: str | None = None,
        raw_name: str | None = None,
        tags: list | None = None,
        overwrite: bool = True,
    ) -> None:
        """
        Write a single array to a FITS file and tag it with DEBUG.

        A header can also be specified.

        The on-disk name of the resulting FITS file can be controlled in a few ways:

        * If `name` is provided then the file will be called "DEBUG_{CallingClass}_{name}.dat" with all spaces replaced
          underscores.

        * If `raw_name` is provided then the filename will be exactly the value of `raw_name`. Your milage may vary with
          spaces in `raw_name`.

        * Otherwise a default name is built from the remaining tags provided in the `tags` argument.
        """
        if raw_name and name:
            raise ValueError("Cannot specify `name` and `raw_name` together.")

        default_tags = [Tag.debug(), Tag.frame()]
        if tags:
            # This is not `+=` because that would modify the input tags in place
            tags = tags + default_tags
        else:
            tags = default_tags

        if raw_name:
            file_name = raw_name
        else:
            base_name = name or self._construct_base_name_from_tags(tags=tags)
            file_name = self._finalize_file_name(base_name)

        self.write(
            data=array,
            header=header,
            tags=tags,
            encoder=fits_array_encoder,
            relative_path=file_name,
            overwrite=overwrite,
        )
        logger.info(f"Wrote debug file with {tags = } to {file_name}")

    def _construct_base_name_from_tags(self, tags: list) -> str:
        """Turn a list of tags into a useful file name."""
        name_parts = []
        for t in tags:
            if t in [Tag.frame(), Tag.debug()]:
                continue

            name_parts.append(t.replace("_", "-"))

        name_parts.sort()

        return "_".join(name_parts)

    def _finalize_file_name(self, base_name: str) -> str:
        """Prepend a debug prefix and the class name to a filename."""
        despaced_name = base_name.replace(" ", "_")

        debug_prefix = f"DEBUG_{self.__class__.__name__}_"

        file_name = debug_prefix + despaced_name

        # You can have any extension you want, as long as it's `.dat` :)
        if not file_name.endswith(".dat"):
            file_name += ".dat"

        return file_name
