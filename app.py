#!/bin/python

from PIL import Image
from tinydb import TinyDB, Query
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)
db = TinyDB("presentes.json")

WIDTH = 250
HEIGHT = 200
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Chá de fralda - Lian</title>
    <meta charset="utf-8" />
    <style>
        table, th, td {
            border:2px solid black;
            text-align:center;
        }
        .center {
            margin-left: auto;
            margin-right: auto;
        }
        .image {
            display: block;
            margin: 2em auto;
            background-color: #444;
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
        }
    </style>
</head>

<body>
    <h2 style="text-align: center;">Chá de fralda</h2>
    <h1 style="text-align: center;">Lian</h1>
    <table class='center'>
        {% for image in images %}
            <tr id="{{ image.id }}">
                <td>
                    {{ image.src.replace('/imgs/', '').replace('.jpg', '').replace('.jpeg', '') }}
                </td>
                <td>
                    <a class="image" href="{{ '/static/' + image.src }}" style="width: {{ image.width }}px; height: {{ image.height }}px">
                        <img src="{{ url_for('static', filename=image.src) }}" data-src="{{ image.src }}?w={{ image.width }}&amp;h={{ image.height }}" width="{{ image.width }}" height="{{ image.height }}" />
                    </a>
                </td>
                <td><button onClick="reservar({{ image.id }})" type="button">Reservar</button></td>
            </tr>
        {% endfor %}
    </table>
</body>

<script>
    function reservar(id) {
        if (confirm("Confirmar reserva?")) {
            try {
                fetch(`${location.protocol}//${location.host}/reservar/${id}`, { method: 'post' });
            } catch(err) {
                console.error(`Error: ${err}`);
            } finally {
                document.getElementById(id).remove();
            }
        }
    }
</script>
"""


@app.route("/reservar/<index>", methods=["POST"])
def reservar(index):
    index = int(index)
    Item = Query()
    db.update({"reservado": True}, Item._id == index)

    return jsonify(db.get(Item._id == index))


@app.route("/alive")
def keep_alive():
    return 200;

@app.route("/")
def index():
    images = []

    for entry in db.search(Query().reservado == False):
        image = Image.open("./static/" + entry["foto"])
        width, height = image.size
        aspect = 1.0 * width / height

        if aspect > 1.0 * WIDTH / HEIGHT:
            width = min(width, WIDTH)
            height = width / aspect
        else:
            height = min(height, HEIGHT)
            width = height * aspect

        images.append(
            {
                "width": int(width),
                "height": int(height),
                "src": entry["foto"],
                "id": entry["_id"],
            }
        )

    return render_template_string(
        TEMPLATE,
        **{
            "images": images,
        },
    )


if __name__ == "__main__":
    app.run()
