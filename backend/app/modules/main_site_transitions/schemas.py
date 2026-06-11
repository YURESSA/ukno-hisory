from pydantic import BaseModel


class MainSiteTransitionRead(BaseModel):
    total_count: int
    latest_transition_at: str | None
