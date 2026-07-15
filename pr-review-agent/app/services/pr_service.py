from app.services.github_service import get_pr_diff, post_comment
from app.services.llm_service import review_code

async def handle_pr(data):
    pr = data["pull_request"]

    diff_url = pr["diff_url"]
    pr_url = pr["url"]

    diff = get_pr_diff(diff_url)

    review = review_code(diff)

    post_comment(pr_url, review)