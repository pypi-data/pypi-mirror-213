import geojson
from fastapi.responses import UJSONResponse
from geojson import FeatureCollection
from geojson.mapping import to_mapping


class GeoJSONResponse(UJSONResponse):
    media_type = "application/geo+json"

    def render(self, content: any) -> bytes:
        if isinstance(content, list):
            content = FeatureCollection([to_mapping(model) for model in content])
        return geojson.dumps(content, ensure_ascii=False).encode("utf-8")
