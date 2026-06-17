import os
import json
from dotenv import load_dotenv
from google import genai
import time

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(
        api_key=GEMINI_API_KEY
    )

def review_project_with_ai(
    project_context,
    readme,
    technologies,
    file_contents
):

    prompt = f"""
        # ROLE
        You are a strict but helpful Senior Software Engineer, code reviewer, and mentor.

        Your job is to review a GitHub project as if you were reviewing a candidate's portfolio project before hiring them.

        Use the provided project context, README, package/dependency files, and sampled code files as evidence.
        Do not guess. If something is missing, say it is missing.

        # REVIEW CRITERIA

        Analyze the project based on:
        - Code Quality
        - Project Structure
        - Readability
        - Component Design
        - Maintainability
        - Scalability
        - Error Handling
        - Best Practices
        - Documentation Quality
        - Resume Value

        # SCORING RULES

        - Give an overall score between 0 and 100.
        - Base the score only on the provided evidence.
        - Mention specific file names whenever possible.
        - Do not invent project features.
        - Do not assume technologies that are not present.
        - Penalize missing documentation and poor code quality.
        - Reward clean architecture and good coding practices.

        # PROJECT INFORMATION
        {project_context}

        # README
        {readme["content"][:3000] if readme["found"] else "README not found"}

        # TECHNOLOGIES DETECTED

        {technologies}

        # CODE FILES
        {file_contents}

        # REVIEW REQUIREMENTS

        When reviewing:

        - Mention strengths backed by evidence.
        - Identify real problems found in the code.
        - Explain why each problem matters.
        - Provide actionable improvements.
        - Suggest features that could improve the project.
        - Provide resume advice for the developer.
        - Mention file names when discussing code issues.

        # RESPONSE FORMAT

        Return ONLY valid JSON.

        {{
            "overall_score": 0,
            "project_summary": "",
            "strengths": [],
            "problems_found": [
                {{
                    "problem": "",
                    "why_it_matters": "",
                    "suggestion": "",
                    "example_fix": ""
                }}
            ],
            "improvements": [],
            "resume_advice": [],
            "next_version_suggestions": []
        }}


        # IMPORTANT

        - Do NOT return markdown.
        - Do NOT return code fences.
        - Do NOT return explanations outside JSON.
        - Do NOT return any text before or after the JSON.
        - Return ONLY the JSON object.
        """

    print("Prompt length:", len(prompt))
    # model = genai.GenerativeModel(
    # "gemini-2.5-flash"
    # )

    # print("Before Gemini")
    # response = model.generate_content(
    #     prompt
    # )
    # print("After Gemini")
    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            break

        except Exception as e:

            if attempt < 2:
                print(
            f"Gemini Attempt {attempt + 1} Failed: {e}"
        )
                time.sleep(2)
            else:

                raise e

    response_text = response.text

    response_text = response_text.replace(
        "```json",
        ""
    )

    response_text = response_text.replace(
        "```",
        ""
    )

    try:
        review_data = json.loads(
            response_text
        )

        return review_data

    except Exception as e:

        print("Gemini Parse Error:", e)

        return {
            "overall_score": 0,
            "project_summary": "AI analysis failed",
            "strengths": [],
            "problems_found": [],
            "improvements": [],
            "resume_advice": [],
            "next_version_suggestions": []
        }