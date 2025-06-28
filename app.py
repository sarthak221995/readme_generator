import os
from flask import Flask, render_template, request, send_file, jsonify
from threading import Thread
import time
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# Store results in memory for simplicity
results = {}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    repo_url = request.form.get("repo_url")
    if not repo_url or not repo_url.startswith("https://github.com/"):
        return jsonify({"error": "Invalid GitHub URL."}), 400

    # Start background thread to run the generator
    task_id = str(int(time.time() * 1000))
    results[task_id] = {"status": "running", "output": ""}
    Thread(target=run_generator, args=(repo_url, task_id)).start()
    return jsonify({"task_id": task_id})

def run_generator(repo_url, task_id):
    try:
        from readme_generator.core import ReadmeGenerator
        from readme_generator.config import Config
        import re
        # config = Config()
        config = Config(llm_provider='openai', model_name='gpt-4.1')
        generator = ReadmeGenerator(config)
        readme = generator.generate(repo_url)
        # Remove code block tags if present
        # readme = re.sub(r"```markdown", '', readme)
        # readme = re.sub(r'```', '', readme)
        results[task_id] = {"status": "done", "output": readme}
    except Exception as e:
        results[task_id] = {"status": "error", "output": str(e)}

@app.route("/progress/<task_id>")
def progress(task_id):
    return jsonify(results.get(task_id, {"status": "unknown", "output": ""}))

@app.route("/download/<task_id>")
def download(task_id):
    readme = results.get(task_id, {}).get("output", "")
    if not readme:
        return "Not found", 404
    with open("/tmp/README.md", "w") as f:
        f.write(readme)
    return send_file("/tmp/README.md", as_attachment=True, download_name="README.md")

if __name__ == "__main__":
    app.run(debug=True)
