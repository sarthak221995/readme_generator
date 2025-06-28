import click
import os
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text
from .core import ReadmeGenerator
from .config import Config

console = Console()

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """🚀 CrewAI README Generator - AI-powered README generation for GitHub repositories"""
    pass

@cli.command()
@click.argument('repo_url')
@click.option('--model', '-m', default='gemini/gemini-2.0-flash-exp', help='LLM model to use')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--no-badges', is_flag=True, help='Disable badges in README')
@click.option('--no-toc', is_flag=True, help='Disable table of contents')
def generate(repo_url, model, verbose, no_badges, no_toc):
    """Generate a README for a GitHub repository"""
    
    # Validate repo URL
    if not repo_url.startswith('https://github.com/'):
        console.print("❌ Invalid GitHub URL. Please provide a URL like: https://github.com/owner/repo", style="red")
        return
    
    # Check for API key
    if not os.getenv('GOOGLE_API_KEY') and 'gemini' in model.lower():
        console.print("❌ GOOGLE_API_KEY environment variable not set!", style="red")
        console.print("Please set your Google API key: export GOOGLE_API_KEY=your_api_key", style="yellow")
        return
    
    # Create config
    config = Config(
        model_name=model,
        verbose=verbose,
        include_badges=not no_badges,
        include_toc=not no_toc
    )
    
    # Display configuration
    table = Table(title="🔧 Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Repository", repo_url)
    table.add_row("Model", model)
    table.add_row("Include Badges", str(config.include_badges))
    table.add_row("Include TOC", str(config.include_toc))
    
    console.print(table)
    console.print()
    
    # Generate README
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("🤖 Generating README with AI agents...", total=None)
            
            generator = ReadmeGenerator(config)
            result = generator.generate(repo_url)
        
        # Success message
        console.print(Panel(
            f"✅ README generated successfully!\n\n"
            f"📊 Length: {len(result)} characters\n"
            f"🔗 Repository: {repo_url}",
            title="🎉 Success",
            border_style="green"
        ))
        
        # # Show preview
        # if click.confirm("Would you like to see a preview?"):
        #     preview = result[:500] + "..." if len(result) > 500 else result
        console.print(Panel(result, title="📖 Preview", border_style="blue"))
    
    except Exception as e:
        console.print(f"❌ Error: {str(e)}", style="red")
        if verbose:
            console.print_exception()

@cli.command()
def config():
    """Show current configuration and setup instructions"""
    
    console.print(Panel(
        "🔧 CrewAI README Generator Configuration",
        style="bold cyan"
    ))
    
    # Check API keys
    table = Table(title="API Keys Status")
    table.add_column("Provider", style="cyan")
    table.add_column("Status", style="magenta")
    table.add_column("Model", style="yellow")
    
    providers = [
        ("Google Gemini", "GOOGLE_API_KEY", "gemini/gemini-2.0-flash-exp"),
        ("OpenAI", "OPENAI_API_KEY", "gpt-4o-mini"),
        ("Anthropic", "ANTHROPIC_API_KEY", "claude-3-sonnet-20240229"),
        ("GitHub", "GITHUB_TOKEN", "N/A (Optional)"),
    ]
    
    for provider, env_var, model in providers:
        status = "✅ Set" if os.getenv(env_var) else "❌ Not Set"
        table.add_row(provider, status, model)
    
    console.print(table)
    console.print()
    
    # Setup instructions
    console.print(Panel(
        """
To get started:

1. Set your API key:
   export GOOGLE_API_KEY=your_api_key_here

2. Generate a README:
   readme-gen https://github.com/owner/repo

3. Advanced usage:
   readme-gen https://github.com/owner/repo --model gemini/gemini-2.0-flash-exp

For more help: readme-gen generate --help
        """,
        title="🚀 Quick Start",
        border_style="green"
    ))

@cli.command()
@click.argument('repo_url')
def analyze(repo_url):
    """Analyze a GitHub repository without generating README"""
    
    if not repo_url.startswith('https://github.com/'):
        console.print("❌ Invalid GitHub URL", style="red")
        return
    
    try:
        from .tools import GitHubRepoTool
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("🔍 Analyzing repository...", total=None)
            
            tool = GitHubRepoTool()
            result = tool._run(repo_url)
        
        console.print(Panel(result, title="📊 Repository Analysis", border_style="blue"))
    
    except Exception as e:
        console.print(f"❌ Error: {str(e)}", style="red")

def main():
    """Main entry point for CLI"""
    cli()

if __name__ == "__main__":
    main()