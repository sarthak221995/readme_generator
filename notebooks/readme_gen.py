import os
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from typing import Optional, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
import sys
from src.tools import GitHubRepoTool

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Create specialized agents
repo_analyzer = Agent(
    role='Repository Analyzer',
    goal='Analyze GitHub repositories to understand their structure, purpose, and technical details',
    backstory="""You are an expert software engineer who specializes in analyzing codebases. 
    You can quickly understand the purpose, architecture, and key features of any software project 
    by examining its code structure, dependencies, and configuration files.""",
    tools=[GitHubRepoTool()],
    llm=llm,
    verbose=True
)

readme_writer = Agent(
    role='Technical Documentation Writer',
    goal='Create comprehensive, well-structured README files that help users understand and use the project',
    backstory="""You are a technical writer with extensive experience in creating developer documentation. 
    You excel at translating complex technical information into clear, accessible documentation that 
    helps developers quickly understand how to install, configure, and use software projects.""",
    llm=llm,
    verbose=True
)

content_reviewer = Agent(
    role='Documentation Quality Reviewer',
    goal='Review and improve README content for clarity, completeness, and professional presentation',
    backstory="""You are a meticulous editor and documentation specialist who ensures that all technical 
    documentation meets high standards of clarity, accuracy, and professionalism. You have a keen eye 
    for detail and know what makes documentation truly helpful for developers.""",
    llm=llm,
    verbose=True)


def create_readme_generation_crew(github_url: str) -> str:
    """
    Create and execute a crew to generate a README for a GitHub repository
    """
    
    # Task 1: Analyze the repository
    analyze_task = Task(
        description=f"""
        Analyze the GitHub repository at {github_url} and provide a comprehensive analysis including:
        1. Project purpose and main functionality
        2. Programming language and key technologies used
        3. Project structure and important files
        4. Dependencies and requirements
        5. Key features based on code analysis
        6. Installation requirements
        7. Usage patterns from code examples
        
        Use the GitHub Repository Analyzer tool to gather this information.
        """,
        agent=repo_analyzer,
        expected_output="Detailed analysis of the repository structure, purpose, and technical details"
    )
    
    # Task 2: Write the README
    write_task = Task(
        description="""
        Based on the repository analysis, create a comprehensive README.md file that includes:
        
        1. **Project Title and Description**: Clear, engaging project name and description
        2. **Features**: Key functionality and capabilities
        3. **Installation**: Step-by-step installation instructions
        4. **Usage**: Code examples and usage instructions
        5. **API Documentation**: If applicable, document main functions/classes
        6. **Configuration**: Environment variables or config files
        7. **Contributing**: Guidelines for contributors
        8. **License**: License information
        9. **Contact/Support**: How to get help or contact maintainers
        
        Use proper Markdown formatting with headers, code blocks, lists, and links.
        Make it professional, clear, and helpful for developers.
        """,
        agent=readme_writer,
        expected_output="Complete README.md file with proper Markdown formatting",
        context=[analyze_task]
    )
    
    # Task 3: Review and improve
    review_task = Task(
        description="""
        Review the generated README and improve it by:
        1. Checking for clarity and readability
        2. Ensuring all sections are complete and helpful
        3. Verifying proper Markdown formatting
        4. Adding badges if appropriate
        5. Improving code examples and explanations
        6. Ensuring professional presentation
        7. Adding table of contents if needed
        
        Provide the final, polished README.md content.
        """,
        agent=content_reviewer,
        expected_output="Final, polished README.md file ready for use",
        context=[write_task]
    )
    
    # Create and run the crew
    crew = Crew(
        agents=[repo_analyzer, readme_writer, content_reviewer],
        tasks=[analyze_task, write_task, review_task],
        process=Process.sequential,
        verbose=True
    )
    
    result = crew.kickoff()
    return result
