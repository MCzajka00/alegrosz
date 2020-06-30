from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, HiddenField
from wtforms.validators import InputRequired, DataRequired


class NewCommentForm(FlaskForm):
    content = TextAreaField("Comment",
                            validators=[InputRequired("Input is required."), DataRequired("Data is required.")])
    item_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField("Submit")
