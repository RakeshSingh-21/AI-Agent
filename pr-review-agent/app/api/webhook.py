from fastapi import APIRouter, Request
from app.services.pr_service import handle_pr
from app.schemas.github import WebhookPayload

router = APIRouter()

# @router.post("/webhook")
# async def github_webhook(request: Request):
#     data = await request.json()
#     print(data,'8weyyetfgcsuejbfksudsjdi')

#     if data.get("action") == "opened":
#         await handle_pr(data)

#     return {"status": "received"}

@router.post("/webhook")
async def github_webhook(payload: WebhookPayload):
    print("Received:", payload)

    if payload.action == "opened":
        print("PR Opened:", payload.pull_request.diff_url)

    return {"status": "received"}