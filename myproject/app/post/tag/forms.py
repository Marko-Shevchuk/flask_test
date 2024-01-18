from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError


from app.domain.Tag import Tag


class TagForm(FlaskForm):
    name = StringField('Name',
                       render_kw={'placeholder': 'Tag name'},
                       validators=[
                           DataRequired(message='Tag name required.')]
                       )
    

    def __init__(self, id=None):
        super().__init__()
        self.__id = id

    def validate_name(self, field):
        tag = None if self.__id is None else Tag.query.get(self.__id)
        name = field.data
        if Tag.query.filter(Tag.name == name).first() and (tag is None or tag.name != name):
            raise ValidationError('Tag name already exists.')