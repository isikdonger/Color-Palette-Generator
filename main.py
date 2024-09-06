import os
from flask import Flask, render_template, url_for, redirect, make_response
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from wtforms.validators import DataRequired, URL
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO
import numpy as np

app = Flask(__name__)
app.secret_key = os.environ.get("secret_key")


class ImageForm(FlaskForm):
    img = FileField("Insert Image", validators=[
        FileRequired(),  # Ensure a file is selected
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')  # Limit file types
    ])
    submit = SubmitField("Submit Image")


def img_to_colors(img_array):
    colors = []
    rows, cols, _ = img_array.shape
    for i in range(rows):
        for j in range(cols):
            # Extract RGB values and ignore the alpha channel
            color = tuple(int(value) for value in img_array[i, j][:3])
            colors.append(color)
    return colors


def find_top_colors(colors):
    seen_colors = {}
    for color in colors:
        if color in seen_colors:
            seen_colors[color] += 1
        else:
            seen_colors[color] = 1
    sorted_colors = sorted(seen_colors.items(), key=lambda x: x[1], reverse=True)
    total_colors = len(colors)
    return sorted_colors[:10], total_colors


@app.route("/", methods={"GET", "POST"})
def home():
    form = ImageForm()
    if form.validate_on_submit():
        file = form.img.data
        img = Image.open(BytesIO(file.read()))
        img_arr = np.array(img)
        colors = img_to_colors(img_array=img_arr)
        top_colors, total_colors = find_top_colors(colors=colors)
        print(top_colors)
        return render_template("index.html", form=form, color_data=top_colors, total=total_colors)
    else:
        return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5001)

