#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Give access to ods files.
"""

# Standard library imports.
from typing import List, Union
from pathlib import Path
from zipfile import ZipFile

# Third party library imports.
from lxml import etree

__date__ = "2022/08/11 20:44:03 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2020 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"

try:
    # Local library imports.
    from ._version import __version__
except ImportError:
    __version__ = "0.0.0+unknown0"


class OdfXml:
    """Base XML handling class for ODF processing."""

    def __init__(self, elem: etree._Element):
        """
        Args:
            element (etree._Element): XML Element
        """
        self.root = elem
        self.nsmap = (
            self.root.nsmap if hasattr(elem, "nsmap") else self.root.getroot().nsmap
        )

    def find(self, tag: str) -> etree._Element:
        """Find ``tag`` in this element.

        Args:
            tag (str): XML tag to serarch for.

        Returns:
           etree._Element: Element acc. to ``tag``."""
        return self.root.find(tag, namespaces=self.nsmap)

    def findall(self, tag: str) -> List[etree._Element]:
        """Find all of ``tag``.

        Args:
           tag (str): XML tag to find.

        Returns:
           List[etree._Element]: Element acc. to ``tag``."""
        return self.root.findall(tag, namespaces=self.nsmap)

    def _attrib_map(self, attrib: str) -> str:
        """Helper for ``get``: provide namespace.

        Args:
           attrib (str): attribute name in the form of <namespace name>:<attr name>.

        Returns:
           str: attribute name with extended namespace."""
        ns, tag = attrib.split(":")
        return f"{{{self.nsmap[ns]}}}{tag}"

    def get(self, attrib: str) -> str:
        """Get atribute of this element, honors namespace.

        Args:
           attrib(str): Attrribute name.

        Returns:
           str: Attribute value."""
        return self.root.get(self._attrib_map(attrib))


class Odf(OdfXml):
    """Base class for OpenDocument Format files."""

    def __init__(self, path: Union[str, Path]):
        """Open ODF file from ``path``.

        Args:
           path ([str,Path]): Location of OpenOffice file.
        """
        with ZipFile(path) as odf_zip:
            with odf_zip.open("content.xml") as content:
                doc = etree.parse(content)
        super().__init__(doc)


# Local Variables:
# mode: python
# compile-command: "poetry run tox"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
