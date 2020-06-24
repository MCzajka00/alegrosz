from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, FileField, SubmitField, SelectField
from wtforms.validators import InputRequired, DataRequired, Length


class ItemForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired("Input is required!"), DataRequired("Data is required!"),
                                             Length(min=5, max=20,
                                                    message="Input must be between 5 and 20 characters long.")])
    price = StringField("Price")
    description = TextAreaField("Description",
                                validators=[InputRequired("Input is required!"), DataRequired("Data is required!"),
                                            Length(min=5, max=40,
                                                   message="Input must be between 5 and 40 characters long.")])
    image = FileField("Image", validators=[FileAllowed(["jpg", "jpeg", "png"], "Images only")])


class NewItemForm(ItemForm):
    category = SelectField("Category", coerce=int)
    subcategory = SelectField("Subcategory", coerce=int)
    submit = SubmitField("Submit")


class EditItemForm(ItemForm):
    submit = SubmitField("Update item")


class DeleteItemForm(FlaskForm):
    submit = SubmitField("Delete item")
