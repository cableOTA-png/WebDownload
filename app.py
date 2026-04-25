import os
import yt_dlp
from flask import Flask, render_template, request, send_file, after_this_request

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/descargar", methods=["POST"])
def link_descargar():
    url = request.form.get("url")
    calidad = request.form.get("calidad")

    output_dir = "/tmp" 
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    opciones = {
        "format": "best" if calidad == "alta" else "worst",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        @after_this_request
        def remove_file(response):
            try:
                os.remove(filename)
            except Exception:
                pass
            return response

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
