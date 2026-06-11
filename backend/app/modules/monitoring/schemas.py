from pydantic import BaseModel


class GrafanaSessionRead(BaseModel):
    grafana_url: str
