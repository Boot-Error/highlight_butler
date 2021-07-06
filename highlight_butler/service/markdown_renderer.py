from highlight_butler.utils.singleton import Singleton
from typing import List, Optional
from frontmatter import Frontmatter
from jinja2 import Template
from highlight_butler.usecase.highlight_renderer.contract import HighlightRendererService
from highlight_butler.entities.highlight import Highlight, HighlightDocument
from highlight_butler.utils.config import Config


class Jinja2Renderer:
    def __init__(self, template: str):
        self.template = Template(template, lstrip_blocks=True, trim_blocks=True)

    def render(self, args: str) -> str:
        try:
            renderedDocument = self.template.render(args)
            return renderedDocument
        except Exception as e:
            print("Failed to render template due to", e)
            return ""


class MarkdownRendererService(HighlightRendererService):
    def __init__(self):
        self.config = Config()

    def load_document(self, document: str) -> Optional[HighlightDocument]:
        try:
            frontmatterData = Frontmatter.read_file(document)
            highlightDocument: HighlightDocument = HighlightDocument(
                title=frontmatterData.get("title"),
                author=frontmatterData.get("author"),
                category=frontmatterData.get("category"),
                tags=frontmatterData.get("tags"),
                created=frontmatterData.get('created'),
                url=frontmatterData.get('url'),
                highlights=[]
            )
            return highlightDocument

        except Exception as e:
            print("Failed to load document due to:", e)
            return None

    def update_document(self, highlightDocument: HighlightDocument, highlights: List[Highlight]):
        return super().update_document(highlightDocument, highlights)

    def render_document(self, highlightDocument: HighlightDocument) -> str:
        template = self._load_template()
        jinja2renderer: Jinja2Renderer = Jinja2Renderer(template)
        return jinja2renderer.render({"doc": highlightDocument.__dict__})

    def _load_template(self) -> Optional[str]:
        template_path = self.config.get_value(
            "butler.renderer.markdown.template")
        try:
            with open(template_path) as f:
                template_content = f.read()
                return template_content
        except Exception as e:
            print("Failed to load template", e)
            return None
