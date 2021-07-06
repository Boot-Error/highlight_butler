
import re
from pathlib import Path
from typing import List

import pydash
from highlight_butler.entities.highlight import HighlightDocument
from highlight_butler.service.hypothesis_importer import \
    HypothesisImporterService
from highlight_butler.service.markdown_renderer import MarkdownRendererService
from highlight_butler.usecase.highlight_importer.contract import \
    HighlightImporterService
from highlight_butler.usecase.highlight_importer.usecase import \
    HighlightImporter
from highlight_butler.usecase.highlight_renderer.usecase import \
    HighlightRenderer
from highlight_butler.utils.config import Config
from highlight_butler.utils.singleton import Singleton


class HighlightImportHandler(metaclass=Singleton):
    def __init__(self):
        self.config = Config()

    def handle(self):

        # get all importers and renderers from the config
        _service_names = self.config.get_value("butler.importers").keys()
        services: List[HighlightImporterService] = list(
            map(self._import_service, _service_names))

        highlightDocuments: List[HighlightDocument] = []
        for service in services:
            _highlightDocuments: List[highlightDocuments] = service(
            ).import_highlights()
            highlightDocuments.extend(_highlightDocuments)

        # render all documents
        markdownRendererService: MarkdownRendererService = MarkdownRendererService()
        highlightRenderer: HighlightRenderer = HighlightRenderer(
            markdownRendererService)

        _filenamePrefix = self.config.get_value(
            "butler.library.filenamePrefix", "")
        for highlightDocument in highlightDocuments:
            renderedDocument = highlightRenderer.render_highlight(
                highlightDocument)
            filename = "{prefix}{title}.md".format(
                prefix=_filenamePrefix, title=pydash.strings.replace(highlightDocument.title, re.compile("[ :?]"), "_"))
            filepath = Path(self.config.get_value(
                "butler.library.dir")).joinpath(filename)
            with open(filepath, "w") as f:
                f.write(renderedDocument)

    def _import_service(self, service: str):
        return {
            "hypothesis": HypothesisImporterService
        }.get(service)
