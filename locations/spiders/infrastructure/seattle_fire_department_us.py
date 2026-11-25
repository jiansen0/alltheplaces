from typing import Iterable

from scrapy.http import Response

from locations.categories import Categories, apply_category
from locations.items import Feature
from locations.storefinders.arcgis_feature_server import ArcGISFeatureServerSpider


class SeattleFireDepartmentUSSpider(ArcGISFeatureServerSpider):
    name = "seattle_fire_department_us"
    item_attributes = {"operator": "Seattle Fire Department", "operator_wikidata": "Q7442098", "state": "WA"}
    host = "services.arcgis.com"
    context_path = "ZOyb2t4B0UYuYNYH/ArcGIS"
    service_id = "Fire_Stations"
    layer_id = "0"

    def post_process_item(self, item: Feature, response: Response, feature: dict) -> Iterable[Feature]:
        if not feature["STNID"].removeprefix("SFD ").isdigit():
            return
        item["ref"] = feature["STNID"]
        apply_category(Categories.FIRE_STATION, item)
        yield item
