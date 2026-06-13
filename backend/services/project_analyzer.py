def detect_technologies(package_json):

    if not package_json["found"]:
        return {}
    
    content = package_json["content"]
    
    dependencies = content.get(
    "dependencies",
    {}
)

    dev_dependencies = content.get(
        "devDependencies",
        {}
    )

    all_packages = {
        **dependencies,
        **dev_dependencies
    }

    technologies = {
    "frontend_framework": None,
    "backend_framework": None,
    "database": None,
    "styling": None,
    "api_client": None,
    "state_management": None,
    "build_tool": None,
    "testing": None,
    "routing": None,
    "authentication": None
}
    
    TECH_MAPPING = {
        "react":       ("frontend_framework", "React"),
        "vue":         ("frontend_framework", "Vue"),
        "tailwindcss": ("styling", "Tailwind CSS"),
        "axios":       ("api_client", "Axios"),
        "@reduxjs/toolkit":       ("state_management", "Redux Toolkit"),
        "vite":        ("build_tool", "Vite"),
        "jest":        ("testing", "Jest"),
        "react-router-dom": ("routing", "React Router"),
        "react-scripts": ("build_tool", "Create React App")
}

    for package_name in all_packages:
        if package_name in TECH_MAPPING:
            category, label = TECH_MAPPING[package_name]  
            technologies[category] = label 

    return technologies


def build_project_context(
    metadata,
    readme,
    technologies
):
    
    return {
    "project_name": metadata.get("name"),
    "description": metadata.get("description"),
    "language": metadata.get("language"),
    "stars": metadata.get("stars"),
    "forks": metadata.get("forks"),
    "technologies": technologies,
    "readme_found": readme.get("found", False)
}

def find_important_files(contents):

    if not contents["found"]:
        return {
            "files": [],
            "directories": []
        }
    
    content = contents["content"]
    
    IMPORTANT_FILES = {"README.md", "package.json", "requirements.txt"}

    IMPORTANT_DIRS = {
    "src",
    "app",
    "pages",
    "components",
    "frontend",
    "backend",
    "client",
    "server"
}

    important_files = []
    important_directories = []

    for item in content:
        if item["type"] == "file" and item["name"] in IMPORTANT_FILES:
            important_files.append(item["name"])

        elif item["type"] == "dir" and item["name"] in IMPORTANT_DIRS:
            important_directories.append(item["name"])

    
    return {
        "files": important_files,
        "directories": important_directories
    }

def select_best_files(file_paths):

    scored_files = []

    for file in file_paths:

        score = 0

        if "App.js" in file:
            score += 100

        if "App.jsx" in file:
            score += 100

        if "main.jsx" in file:
            score += 90

        if "index.js" in file:
            score += 80

        if "components" in file:
            score += 50

        scored_files.append(
            (score, file)
        )
    
    scored_files.sort(
    reverse=True
)
    best_files = []

    for score, file in scored_files[:3]:
        best_files.append(file)

    return best_files
