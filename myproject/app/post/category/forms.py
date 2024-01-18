from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError

from app.domain.Category import Category


class CategoryForm(FlaskForm):
    name = StringField('Name',
                       render_kw={'placeholder': 'Category name'},
                       validators=[
                           DataRequired(message='Category name required.')]
                       )

    def __init__(self, id=None):
        super().__init__()
        self.__id = id

    def validate_name(self, field):
        category = None if self.__id is None else Category.query.get(self.__id)
        name = field.data
        if Category.query.filter(Category.name == name).first() and (category is None or category.name != name):
            raise ValidationError('Category name already exists.')