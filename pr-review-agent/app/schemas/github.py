from pydantic import BaseModel

class PullRequest(BaseModel):
    url: str
    diff_url: str

class WebhookPayload(BaseModel):
    action: str
    pull_request: PullRequest