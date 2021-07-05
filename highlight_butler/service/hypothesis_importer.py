import functools
import itertools
from highlight_butler.entities.highlight import Highlight, HighlightDocument, HighlightLocation
from typing import List, Optional

import requests
import pydash
from highlight_butler.utils.config import Config
from highlight_butler.utils.singleton import Singleton
from highlight_butler.usecase.highlight_importer.contract import HighlightImporterService


class HypothesisConnector(metaclass=Singleton):
    def __init__(self):
        self.config = Config()
        self._apikey = self.config.get_value(
            "butler.importers.hypothesis.apikey")

    def _headers(self):
        headers = {}
        headers.setdefault("Accept", "application/json")
        headers.setdefault("Content-Type", "application/json")
        headers.setdefault(
            "Authorization", "Bearer {apikey}".format(apikey=self._apikey))

        return headers

    def search_annotation(self, query: dict) -> dict:

        url = "https://api.hypothes.is/api/search"

        try:
            r = requests.get(url, headers=self._headers(), params=query)
            if r.status_code != 200:
                print("Failed to fetch annotations")
                return None
            return r.json()
        except Exception as e:
            print(e)
            return None

    @functools.lru_cache(maxsize=10)
    def group_list(self):

        url = "https://api.hypothes.is/api/groups"

        try:
            r = requests.get(url, headers=self._headers())
            if r.status_code != 200:
                print("Failed to fetch annotations")
                return None
            return r.json()
        except Exception as e:
            print(e)
            return None


class HypothesisImporterService(HighlightImporterService):
    def __init__(self):
        self._hypothesis_connector = HypothesisConnector()
        self._config = Config()

    def import_highlights(self) -> List[HighlightDocument]:
        groups = self._config.get_value("butler.importers.hypothesis.groups")
        groupIds = map(self._get_groupid, groups)
        _annotations = pydash.collections.flat_map(
            groupIds, self._get_all_annotation_by_group)

        annotations_by_uri = itertools.groupby(_annotations,
                                               key=lambda annotation: pydash.get(annotation, "uri"))

        highlightDocuments: List[HighlightDocument] = []
        for url, annotations in annotations_by_uri:
            highlightDocument = self._create_highlight_document(
                url=url, annotations=annotations)
            highlightDocuments.append(highlightDocument)

        return highlightDocuments

    def _create_highlight_document(self, url: str, annotations: List[dict]) -> HighlightDocument:

        # get common values from one annotation
        _annotation = pydash.arrays.head(annotations)

        highlightDocument: HighlightDocument = HighlightDocument(
            author="no-one",
            created="hello, world",
            title=pydash.get(_annotation, "document.title"),
            url=pydash.get(_annotation, "uri"),
            highlights=list(map(self._annotation_to_highlight, annotations)),
            category=self._config.get_value(
                "butler.importers.hypothesis.category"),
            tags=[]
        )
        return highlightDocument

    def _annotation_to_highlight(self, annotation: dict) -> Highlight:
        _tagPrefix = self._config.get_value(
            "butler.importers.hypothesis.tagPrefix")
        _selector = pydash.get(annotation, "target")[0].get("selector")
        _quoter_selector = pydash.collections.find(
            _selector, {"type": "TextQuoteSelector"})
        highlight_text = pydash.get(_quoter_selector, "exact")
        annotation_text = pydash.get(annotation, "text")

        highlight_location: HighlightLocation = HighlightLocation(
            locationIdentifier="url", value=pydash.get(annotation, "links.incontext"))
        highlight: Highlight = Highlight(
            text=highlight_text, annotation=annotation_text, location=highlight_location,
            tags=pydash.map_(pydash.get(annotation, "tags"), lambda tag: _tagPrefix + tag))

        return highlight

    def _get_all_annotation_by_group(self, groupId):
        query = {"group": groupId}
        return self._hypothesis_connector.search_annotation(query).get("rows")

    def _get_groupid(self, group_name: str) -> Optional[str]:
        groups = self._hypothesis_connector.group_list()
        for group in groups:
            if group.get("name") == group_name:
                return group.get("id")
        # TODO: raise exception for invalid group_name
        return None