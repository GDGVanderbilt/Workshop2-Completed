import os
from pathlib import Path

credentials_path = Path(__file__).resolve().parent / "service-account.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(credentials_path)

from flask import Flask, render_template, request
import markdown
from google import genai
from google.genai import types

app = Flask(__name__, template_folder=".")

PROJECT_ID = "project id"

client = genai.Client(
    enterprise=True,
    project=PROJECT_ID,
    location="us",
)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


def generate(youtube_link, model, additional_prompt):
    youtube_video = types.Part.from_uri(
        file_uri=youtube_link,
        mime_type="video/*",
    )
    if not additional_prompt:
        additional_prompt = " "
    contents = [
        youtube_video,
        types.Part.from_text(text="""Provide a summary of the video."""),
        additional_prompt,
    ]
    generate_content_config = types.GenerateContentConfig(
        max_output_tokens=8192,
        response_modalities=["TEXT"],
    )
    return client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    ).text


@app.route("/summarize", methods=["POST"])
def summarize():
    youtube_link = request.form["youtube_link"]
    model = request.form["model"]
    additional_prompt = request.form["additional_prompt"]
    summary = generate(youtube_link, model, additional_prompt)
    html = markdown.markdown(summary, extensions=["fenced_code", "tables"])
    return render_template("summary.html", summary=html)


if __name__ == "__main__":
    server_port = os.environ.get("PORT", "8080")
    app.run(debug=False, port=server_port, host="0.0.0.0")
