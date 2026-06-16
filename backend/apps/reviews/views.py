from rest_framework.decorators import api_view
from rest_framework.response import Response

from services.review_service import (
    generate_project_review
)


@api_view(["POST"])
def review_project(request):

    repo_url = request.data.get(
        "repo_url"
    )

    if not repo_url:
        return Response(
            {"error": "Please provide a GitHub URL"},
            status=400
        )

    result = generate_project_review(
        repo_url
    )

    if not result["success"]:
        return Response(
            {"error": result["error"]},
            status=400
        )

    return Response(result)