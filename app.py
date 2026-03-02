from flask import Flask, render_template, request, send_file
import os
import uuid
import zipfile

from services.downloader import download_video
from services.video_processor import process_video
from services.transcription import transcribe_video
from services.caption_engine import generate_caption
from services.rule_engine import apply_platform_rules

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    try:
        job_id = str(uuid.uuid4())
        job_folder = os.path.join("outputs", job_id)
        os.makedirs(job_folder, exist_ok=True)

        video_url = request.form["video_url"]
        niche = request.form["niche"]
        cta = request.form.get("cta", "")

        # 1️⃣ Download video
        input_video = download_video(video_url, job_folder)

        # 2️⃣ Transcribe video
        transcript = transcribe_video(input_video)

        platforms = ["instagram", "facebook", "twitter", "youtube", "linkedin"]

        for platform in platforms:

            output_video = os.path.join(job_folder, f"{platform}.mp4")

            # 3️⃣ Process video (trim + resize)
            process_video(input_video, output_video)

            # 4️⃣ Generate caption
            caption = generate_caption(platform, niche, transcript, cta)

            # 5️⃣ Apply platform rules
            caption = apply_platform_rules(platform, caption)

            # ✅ FIX: Write file with UTF-8 encoding (prevents emoji crash)
            with open(os.path.join(job_folder, f"{platform}.txt"), "w", encoding="utf-8") as f:
                f.write(caption)

        # 6️⃣ Create ZIP file
        zip_path = job_folder + ".zip"

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in os.listdir(job_folder):
                full_path = os.path.join(job_folder, file)
                zipf.write(full_path, arcname=file)

        return send_file(zip_path, as_attachment=True)

    except Exception as e:
        return f"Error occurred: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)