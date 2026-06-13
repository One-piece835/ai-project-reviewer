from django.shortcuts import render # type: ignore
from rest_framework.decorators import api_view
from rest_framework.response import Response

from services.github_service import (extract_repo_info, get_repository_metadata, get_readme, get_package_json, get_repository_contents, explore_directory, get_file_contents)
from services.project_analyzer import (detect_technologies, build_project_context, find_important_files, select_best_files)

from services.gemini_service import ( review_project_with_ai)

# Create your views here.

@api_view(["POST"])
def review_project(request):
    repo_url = request.data.get("repo_url")

    print(repo_url)

    repo_info = extract_repo_info(repo_url)


    metadata = get_repository_metadata(
        repo_info["owner"],
        repo_info["repo"]
    )

    readme = get_readme(
    repo_info["owner"],
    repo_info["repo"]
)
    
    package = get_package_json(
    repo_info["owner"],
    repo_info["repo"]
    )

    technologies = detect_technologies(package)

    project_context = build_project_context(
    metadata,
    readme,
    technologies
)
    
    contents = get_repository_contents(
        repo_info["owner"],
        repo_info["repo"]
    )

    important_files = find_important_files(contents)

    directories = important_files["directories"]

    all_code_files = []

    for directory_name in directories:

        files = explore_directory(
            repo_info["owner"],
            repo_info["repo"],
            directory_name
        )

    all_code_files.extend(files)
    
    best_files = select_best_files( all_code_files)

    file_contents = get_file_contents(
        repo_info["owner"],
        repo_info["repo"],
        best_files
    )

    # Gemini

#     ai_review = review_project_with_ai(
#     project_context,
#     readme,
#     technologies,
#     file_contents
# )

    return Response({
        "message": "API Working",
        "repo_info": repo_info,
        "metadata": metadata,
        "readme": readme,
        "package": package,
        "technologies": technologies,
        "project_context": project_context,
        "important_files": important_files,
        "best_files": best_files,
        "file_contents": file_contents,
        # "ai_review": ai_review
    })
