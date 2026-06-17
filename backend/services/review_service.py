from services.github_service import (
    extract_repo_info,
    get_repository_metadata,
    get_readme,
    get_package_json,
    get_repository_contents,
    explore_directory,
    get_file_contents
)

from services.project_analyzer import (
    detect_technologies,
    build_project_context,
    find_important_files,
    select_best_files
)

from services.gemini_service import (
    review_project_with_ai
)


def generate_project_review(repo_url):

    # Extract owner and repo name
    try:
        repo_info = extract_repo_info(repo_url)

        owner = repo_info["owner"]
        repo = repo_info["repo"]

        # Repository metadata
        metadata = get_repository_metadata(
            owner,
            repo
    )

    # README
        readme = get_readme(
            owner,
            repo
        )

    # package.json
        package = get_package_json(
            owner,
            repo
        )

    # Detect technologies
        technologies = detect_technologies(
            package
        )

    # Build project context
        project_context = build_project_context(
            metadata,
            readme,
            technologies
        )

        # Repository contents
        contents = get_repository_contents(
            owner,
            repo
        )

        important_files = find_important_files(
            contents
        )

        directories = important_files["directories"]

        all_code_files = []

        # Explore directories
        for directory_name in directories:

            files = explore_directory(
                owner,
                repo,
                directory_name
            )

            all_code_files.extend(files)

        # Select best files
        best_files = select_best_files(
            all_code_files
        )

        # Fetch file contents
        file_contents = get_file_contents(
            owner,
            repo,
            best_files
        )

        # AI Review
        ai_review = review_project_with_ai(
            project_context,
            readme,
            technologies,
            file_contents
        )

        return {
            "success": True,
            "repository": repo_url,
            "metadata": metadata,
            "ai_review": ai_review
        }

    except ValueError as e:

        return {
            "success": False,
            "error": str(e)
        }

    except Exception as e:

        error_message = str(e)

        if "503" in error_message:

            return {
                "success": False,
                "error": "AI service is temporarily unavailable. Please try again later."
            }
        
        if "rate limit" in error_message.lower():

            return {
                "success": False,
                "error": "GitHub API rate limit exceeded. Please try again later."
            }

        return {
            "success": False,
            "error": error_message
        }