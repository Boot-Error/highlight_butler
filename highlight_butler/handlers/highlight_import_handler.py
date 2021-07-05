from typing import List
from highlight_butler.usecase.highlight_importer.contract import HighlightImporterService
from highlight_butler.usecase.highlight_importer.usecase import HighlightImporter
from highlight_butler.service.hypothesis_importer import HypothesisImporterService
from highlight_butler.utils.config import Config
from highlight_butler.utils.singleton import Singleton


class HighlightImportHandler(metaclass=Singleton):
    def __init__(self):
        self.config = Config()

    def handle(self):
        
        # get all importers and renderers from the config
        _service_names = self.config.get_value("butler.importers").keys()
        services: List[HighlightImporterService] = list(map(self._import_service, _service_names))

        hypothesisImporterService: HypothesisImporterService = self._import_service("hypothesis")
        highlightImporter: HighlightImporter = HighlightImporter(hypothesisImporterService)
        highlights = highlightImporter.import_highlight()
        print(highlights)
        
    def _import_service(self, service: str):
        return {
            "hypothesis": HypothesisImporterService
        }.get(service)
