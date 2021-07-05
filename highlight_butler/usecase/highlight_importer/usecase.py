from highlight_butler.entities.highlight import HighlightDocument
from typing import List, Optional
from highlight_butler.usecase.highlight_importer.contract import HighlightImporterService


class HighlightImporter:
    def __init__(self, highlightImporterService: HighlightImporterService):
        self._service = highlightImporterService()
        
    def import_highlight(self, params: Optional[dict] = None) -> List[HighlightDocument]:
        return self._service.import_highlights()