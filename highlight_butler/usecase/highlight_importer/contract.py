from typing import List

from highlight_butler.entities.highlight import HighlightDocument


class HighlightImporterService:
    def __init__(self) -> None:
	    pass
    def import_highlights(self) -> List[HighlightDocument]:
	    raise NotImplementedError()
