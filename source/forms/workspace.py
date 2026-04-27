from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, SelectField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, Optional

class CreateWorkspaceForm(FlaskForm):
    name = StringField("Workspace name", validators=[
        DataRequired(),
        Length(min=3, max=50),
    ])
    description = TextAreaField("Description (Optional)", validators=[
        Optional(),
        Length(max=255),
    ])
    color = RadioField("Color", choices=[
        ("violet", "Violet"),
        ("blue", "Blue"),
        ("green", "Green"),
        ("amber", "Amber"),
        ("pink", "Pink"),
        ("red", "Red"),
        ("teal", "Teal"),
        ("stone", "Stone"),
        ("slate", "Slate"),
    ], default="violet")
    icon = RadioField("Icon", choices=[
        ("letter", "Letter"),
        ("business", "Business"),
        ("team", "Team"),
        ("marketing", "Marketing"),
        ("analytics", "Analytics"),
        ("store", "Store"),
        ("favourite", "Favourite"),
        ("startup", "Startup"),
    ], default="letter")
    submit = SubmitField("Create Workspace")