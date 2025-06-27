import os
from typing import Optional
from crewai import Agent, Task, Crew, Process
from .tools import GitHubRepoTool
from .config import Config

class ReadmeGenerator:
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config.from_env()
        self.config.setup_environment()
        
        # Initialize tools
        self.github_tool = GitHubRepoTool()
        
        # Initialize agents
        self._setup_agents()
    
    def _setup_agents(self):
        """Setup CrewAI agents"""
        
        self.repo_analyzer = Agent(
            role='Repository Analyzer',
            goal='Analyze GitHub repositories to understand their structure, purpose, and technical details',
            backstory="""You are an expert software engineer who specializes in analyzing codebases. 
            You can quickly understand the purpose, architecture, and key features of any software project 
            by examining its code structure, dependencies, and configuration files. You provide detailed 
            technical analysis that helps create comprehensive documentation.""",
            tools=[self.github_tool],
            llm=self.config.model_name,
            verbose=self.config.verbose
        )
        
        self.readme_writer = Agent(
            role='Technical Documentation Writer',
            goal='Create comprehensive, well-structured README files that help users understand and use the project',
            backstory="""You are a technical writer with extensive experience in creating developer documentation. 
            You excel at translating complex technical information into clear, accessible documentation that 
            helps developers quickly understand how to install, configure, and use software projects. You know 
            what makes a README truly helpful and engaging.""",
            llm=self.config.model_name,
            verbose=self.config.verbose
        )
        
        self.content_reviewer = Agent(
            role='Documentation Quality Reviewer',
            goal='Review and improve README content for clarity, completeness, and professional presentation',
            backstory="""You are a meticulous editor and documentation specialist who ensures that all technical 
            documentation meets high standards of clarity, accuracy, and professionalism. You have a keen eye 
            for detail and know what makes documentation truly helpful for developers. You ensure consistency 
            in formatting, tone, and structure.""",
            llm=self.config.model_name,
            verbose=self.config.verbose
        )
    
    def generate(self, repo_url: str) -> str:
        """Generate README for a GitHub repository"""
        
        # Create tasks
        analyze_task = Task(
            description=f"""
            Analyze the GitHub repository at {repo_url} and provide a comprehensive analysis including:
            
            1. **Project Overview**: Understand the main purpose and functionality
            2. **Technical Stack**: Programming language, frameworks, and key technologies
            3. **Project Structure**: Important files, directories, and architecture
            4. **Dependencies**: Required packages, libraries, and external dependencies
            5. **Configuration**: Environment variables, config files, and setup requirements
            6. **Features**: Key capabilities and functionality based on code analysis
            7. **Usage Patterns**: How the project is typically used based on code structure
            8. **Installation Requirements**: System requirements and setup dependencies
            
            Use the GitHub Repository Analyzer tool to gather detailed information about the repository.
            Provide a thorough analysis that will help create an excellent README file.
            """,
            agent=self.repo_analyzer,
            expected_output="Comprehensive technical analysis of the repository including all key aspects needed for documentation"
        )
        
        write_task = Task(
            description=f"""
            Based on the repository analysis, create a comprehensive and professional README.md file that includes:
            
            ## Structure Requirements:
            1. **Header Section**:
               - Project title with clear, descriptive name
               - Brief, compelling description (1-2 sentences)
               - Badges for build status, version, license, etc. (if applicable)
               - Table of contents (if README is long)
            
            2. **Overview Section**:
               - Detailed project description
               - Key features and capabilities
               - Screenshots or demos (mention where applicable)
            
            3. **Installation Section**:
               - Prerequisites and system requirements
               - Step-by-step installation instructions
               - Package manager commands (npm, pip, cargo, etc.)
               - Environment setup instructions
            
            4. **Usage Section**:
               - Basic usage examples with code snippets
               - Common use cases and scenarios
               - Configuration options
               - Command-line usage (if applicable)
            
            5. **API Documentation** (if applicable):
               - Main functions, classes, or endpoints
               - Parameters and return values
               - Usage examples
            
            6. **Development Section**:
               - Development setup instructions
               - How to run tests
               - Build instructions
               - Development dependencies
            
            7. **Contributing Section**:
               - How to contribute to the project
               - Code style guidelines
               - Pull request process
               - Issue reporting guidelines
            
            8. **Footer Section**:
               - License information
               - Credits and acknowledgments
               - Contact information
               - Links to documentation, website, etc.
            
            ## Formatting Requirements:
            - Use proper Markdown syntax with clear headers
            - Include code blocks with appropriate language syntax highlighting
            - Use lists, tables, and formatting for readability
            - Include relevant links and references
            - Make it visually appealing and easy to scan
            
            Create a professional, comprehensive README that developers will find genuinely helpful.
            """,
            agent=self.readme_writer,
            expected_output="Complete, well-formatted README.md file with all essential sections and proper Markdown formatting",
            context=[analyze_task]
        )
        
        review_task = Task(
            description="""
            Review and polish the generated README to ensure it meets the highest standards:
            
            ## Review Criteria:
            1. **Content Quality**:
               - All sections are complete and informative
               - Information is accurate and helpful
               - Examples are clear and functional
               - Instructions are easy to follow
            
            2. **Structure and Organization**:
               - Logical flow and organization
               - Proper heading hierarchy
               - Good use of sections and subsections
               - Table of contents is accurate (if included)
            
            3. **Formatting and Style**:
               - Consistent Markdown formatting
               - Proper code block syntax highlighting
               - Good use of lists, tables, and emphasis
               - Professional appearance
            
            4. **Completeness**:
               - All essential sections are present
               - No missing information for users
               - Clear next steps for different user types
               - Proper attribution and links
            
            5. **Readability**:
               - Clear, concise writing
               - Good balance of detail and brevity
               - Easy to scan and navigate
               - Engaging and professional tone
            
            Provide the final, polished README.md content that's ready for immediate use.
            """,
            agent=self.content_reviewer,
            expected_output="Final, publication-ready README.md file with excellent formatting, complete information, and professional presentation",
            context=[write_task]
        )
        
        # Create and run crew
        crew = Crew(
            agents=[self.repo_analyzer, self.readme_writer, self.content_reviewer],
            tasks=[analyze_task, write_task, review_task],
            process=Process.sequential,
            verbose=self.config.verbose
        )
        
        result = crew.kickoff()
        
        return str(result)
