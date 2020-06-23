from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField


class NewItemForm(FlaskForm):
    title = StringField("Title")
    price = StringField("Price")
    description = TextAreaField("Description")
    submit = SubmitField("Submit")
