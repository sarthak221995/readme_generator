import requests
import json
import os
import logging
from typing import Dict, Any, List
from crewai.tools import BaseTool

class GitHubRepoTool(BaseTool):
    name: str = "GitHub Repository Analyzer"
    description: str = "Fetches repository information, file structure, and content from GitHub"
    
    def _run(self, repo_url: str) -> str:
        """Analyze a GitHub repository and extract relevant information
        
        Args:
            repo_url (str): The GitHub repository URL.
        
        Returns:
            str: JSON string with analysis or error message.
        """
        try:
            logging.info(f"Analyzing repository: {repo_url}")
            # Extract owner and repo name from URL
            parts = repo_url.replace('https://github.com/', '').strip('/').split('/')
            if len(parts) < 2:
                return "Invalid GitHub URL format. Expected: https://github.com/owner/repo"
            owner, repo = parts[0], parts[1]
            
            # GitHub API endpoints
            repo_api = f"https://api.github.com/repos/{owner}/{repo}"
            contents_api = f"https://api.github.com/repos/{owner}/{repo}/contents"
            
            # Headers for GitHub API
            headers = {}
            github_token = os.getenv("GITHUB_TOKEN")
            if github_token:
                headers["Authorization"] = f"token {github_token}"
            
            # Get repository information
            try:
                repo_response = requests.get(repo_api, headers=headers)
                if repo_response.status_code == 404:
                    return f"Repository not found: {owner}/{repo}"
                elif repo_response.status_code == 403:
                    return "GitHub API rate limit exceeded or forbidden."
                elif repo_response.status_code != 200:
                    return f"Failed to fetch repository information: {repo_response.status_code}"
                repo_data = repo_response.json()
            except requests.RequestException as e:
                return f"Network error fetching repo: {str(e)}"
            
            # Get repository contents (top-level only)
            try:
                contents_response = requests.get(contents_api, headers=headers)
                contents_data = contents_response.json() if contents_response.status_code == 200 else []
            except requests.RequestException as e:
                contents_data = []
            
            # Get main files content
            # important_files = [
            #     'package.json', 'requirements.txt', 'setup.py', 'pyproject.toml',
            #     'Cargo.toml', 'go.mod', 'pom.xml', 'build.gradle', 'Gemfile',
            #     'composer.json', 'Dockerfile', 'docker-compose.yml', '.env.example'
            # ]
            
            file_contents = {}
            code_files = []
            
            for item in contents_data:
                if item['type'] == 'file':
                    filename = item['name']
                    
                    # Get important config files
                    # if filename.lower() in [f.lower() for f in important_files]:
                    if item['size'] < 50000:  # Limit file size
                        try:
                            file_response = requests.get(item['download_url'], headers=headers)
                            if file_response.status_code == 200:
                                file_contents[filename] = file_response.text[:2000]
                        except requests.RequestException:
                            continue
                    
                    # Collect code files for analysis
                    if any(filename.endswith(ext) for ext in ['.py', '.js', '.ts', '.go', '.rs', '.java', '.cpp', '.c', '.rb', '.php','.md']):
                        if item['size'] < 10000:  # Smaller limit for code files
                            code_files.append(filename)
            
            # Get a few sample code files
            sample_code = {}
            for filename in code_files[:3]:  # Limit to 3 files
                try:
                    item = next(item for item in contents_data if item['name'] == filename)
                    file_response = requests.get(item['download_url'], headers=headers)
                    if file_response.status_code == 200:
                        sample_code[filename] = file_response.text[:1000]  # First 1000 chars
                except Exception:
                    continue
            
            # Compile analysis
            analysis = {
                'repository': {
                    'name': repo_data.get('name', ''),
                    'full_name': repo_data.get('full_name', ''),
                    'description': repo_data.get('description', ''),
                    'language': repo_data.get('language', ''),
                    'stars': repo_data.get('stargazers_count', 0),
                    'forks': repo_data.get('forks_count', 0),
                    'watchers': repo_data.get('watchers_count', 0),
                    'size': repo_data.get('size', 0),
                    'topics': repo_data.get('topics', []),
                    'license': repo_data.get('license', {}).get('name', '') if repo_data.get('license') else '',
                    'clone_url': repo_data.get('clone_url', ''),
                    'homepage': repo_data.get('homepage', ''),
                    'has_issues': repo_data.get('has_issues', False),
                    'has_wiki': repo_data.get('has_wiki', False),
                    'has_pages': repo_data.get('has_pages', False),
                    'created_at': repo_data.get('created_at', ''),
                    'updated_at': repo_data.get('updated_at', ''),
                    'pushed_at': repo_data.get('pushed_at', ''),
                },
                'structure': {
                    'files': [item['name'] for item in contents_data if item['type'] == 'file'],
                    'directories': [item['name'] for item in contents_data if item['type'] == 'dir'],
                    'total_files': len([item for item in contents_data if item['type'] == 'file']),
                },
                'configuration_files': file_contents,
                'sample_code': sample_code,
                'languages': {
                    'primary': repo_data.get('language', ''),
                    'detected': list(set([f.split('.')[-1] for f in code_files if '.' in f]))
                }
            }
            
            return json.dumps(analysis, indent=2)
            
        except Exception as e:
            logging.error(f"Error analyzing repository: {str(e)}")
            return f"Error analyzing repository: {str(e)}"
