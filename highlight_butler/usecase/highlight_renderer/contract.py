from typing import List
from highlight_butler.entities.highlight import Highlight, HighlightDocument

class HighlightRendererService:
    def load_document(self, document: str) -> HighlightDocument:
        raise NotImplementedError()
    
    def update_document(self, highlightDocument: HighlightDocument, highlights: List[Highlight]):
        raise NotImplementedError()
    
    def render_document(self, highlightDocument: HighlightDocument) -> str:
        raise NotImplementedError()