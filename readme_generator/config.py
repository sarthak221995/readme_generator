import os
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class Config(BaseModel):
    """Configuration for README Generator"""
    
    # LLM Configuration
    llm_provider: str = Field(default="gemini", description="LLM provider to use")
    model_name: str = Field(default="gemini/gemini-2.0-flash-exp", description="Model name")
    temperature: float = Field(default=0.7, description="Temperature for LLM")
    
    # API Keys
    google_api_key: Optional[str] = Field(default=None, description="Google API key")
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API key")
    
    # GitHub Configuration
    github_token: Optional[str] = Field(default=None, description="GitHub token for higher rate limits")
    
    # Output Configuration
    include_badges: bool = Field(default=True, description="Include badges in README")
    include_toc: bool = Field(default=True, description="Include table of contents")
    
    # Crew Configuration
    verbose: bool = Field(default=True, description="Enable verbose logging")
    
    class Config:
        env_prefix = "README_GEN_"
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables"""
        return cls(
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            github_token=os.getenv("GITHUB_TOKEN"),
        )
    
    def setup_environment(self):
        """Setup environment variables for LLM providers"""
        if self.google_api_key:
            os.environ["GOOGLE_API_KEY"] = self.google_api_key
        if self.openai_api_key:
            os.environ["OPENAI_API_KEY"] = self.openai_api_key
        if self.anthropic_api_key:
            os.environ["ANTHROPIC_API_KEY"] = self.anthropic_api_key
        if self.github_token:
            os.environ["GITHUB_TOKEN"] = self.github_token
