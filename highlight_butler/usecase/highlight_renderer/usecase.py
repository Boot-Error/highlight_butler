from highlight_butler.entities.highlight import HighlightDocument
from highlight_butler.usecase.highlight_renderer.contract import HighlightRendererService


class HighlightRenderer:
    def __init__(self, service: HighlightRendererService):
        self._service: HighlightRendererService = service
        
    def render_highlight(self, document: HighlightDocument):
        rendered_document = self._service.render_document(document)
        return rendered_document