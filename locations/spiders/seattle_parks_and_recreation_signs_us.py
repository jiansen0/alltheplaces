from typing import Iterable

from scrapy.http import Response

from locations.categories import Categories, apply_category
from locations.items import Feature
from locations.storefinders.arcgis_feature_server import ArcGISFeatureServerSpider


class SeattleParksAndRecreationSignsUSSpider(ArcGISFeatureServerSpider):
    name = "seattle_parks_and_recreation_signs_us"
    item_attributes = {"operator": "Seattle Parks and Recreation", "operator_wikidata": "Q7442147", "state": "WA"}
    host = "services.arcgis.com"
    context_path = "ZOyb2t4B0UYuYNYH/ArcGIS"
    service_id = "Park_Signs"
    layer_id = "0"

    def post_process_item(self, item: Feature, response: Response, feature: dict) -> Iterable[Feature]:
        if feature["SIGN_TP"] not in {"INTERPRETIVE", "KIOSK"}:
            return
        item["ref"] = feature["GLOBALID"]
        apply_category(Categories.TOURISM_INFORMATION, item)
        item["extras"]["information"] = "board"
        yield item
