import os

import yt_dlp
from flask import Flask, render_template, request, send_file

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/descargar", methods=["POST"])
def link_descargar():
    url = request.form.get("url")
    calidad = request.form.get("calidad")

    output_dir = (
        "/tmp" if os.environ.get("RENDER") else os.path.expanduser("~/links/videos")
    )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    opciones = {
        "format": "best" if calidad == "alta" else "worst",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(opciones) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
