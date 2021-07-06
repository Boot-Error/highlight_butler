from datetime import datetime
from typing import List, Optional

import jinja2
from frontmatter import Frontmatter
from highlight_butler.entities.highlight import Highlight, HighlightDocument
from highlight_butler.usecase.highlight_renderer.contract import \
    HighlightRendererService
from highlight_butler.utils.config import Config
from highlight_butler.utils.singleton import Singleton


class Jinja2Renderer:
    def __init__(self, template: str):
        # setup custom filers
        env = jinja2.Environment(lstrip_blocks=True, trim_blocks=True)
        env.filters["prettyDate"] = Jinja2Renderer.prettyDateFilter
        env.filters["asTag"] = Jinja2Renderer.asTagFilter
        # load template
        self.template = env.from_string(template)

    def render(self, args: str) -> str:
        try:
            renderedDocument = self.template.render(args)
            return renderedDocument
        except Exception as e:
            print("Failed to render template due to", e)
            return ""

    @staticmethod
    def prettyDateFilter(value: str) -> str:
        isodt: datetime = value
        suffix = 'th' if 11 <= isodt.day <= 13 else {
            1: 'st', 2: 'nd', 3: 'rd'}.get(isodt.day % 10, 'th')
        return isodt.strftime("%B {S}, %Y").replace('{S}', str(isodt.day) + suffix)
        
    @staticmethod
    def asTagFilter(value: str) -> str:
        return "#{tag}".format(tag=value)

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
