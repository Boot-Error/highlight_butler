from typing import List
from highlight_butler.usecase.highlight_renderer.contract import HighlightRendererService
from highlight_butler.entities.highlight import Highlight, HighlightDocument

class MarkdownRendererService(HighlightRendererService):
    def __init__(self):
        pass

    def load_document(self, document: str) -> HighlightDocument:
        return super().load_document(document)
    
    def update_document(self, highlightDocument: HighlightDocument, highlights: List[Highlight]):
        return super().update_document(highlightDocument, highlights)
    
    def render_document(self, highlightDocument: HighlightDocument) -> str:
        return super().render_document(highlightDocument)

