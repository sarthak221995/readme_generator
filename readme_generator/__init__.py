"""
CrewAI README Generator - AI-powered README generation for GitHub repositories
"""

__version__ = "0.1.0"
__author__ = "Sarthak Dargan"
__email__ = "sarthak221995@gmail.com"

from .core import ReadmeGenerator
from .config import Config

__all__ = ["ReadmeGenerator", "Config"]