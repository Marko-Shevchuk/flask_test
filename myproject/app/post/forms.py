
from flask_wtf import FlaskForm

from wtforms import TextAreaField, StringField, SelectField, FileField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import ListWidget, CheckboxInput

from app.domain.Category import Category
from app.domain.Post import Post, PostType
from app.domain.Tag import Tag


class PostForm(FlaskForm):
    title = StringField('Title',
                        render_kw={'placeholder': 'Title'},
                        validators=[
                            DataRequired(message='Title required.')
                        ])

    text = TextAreaField('Text',
                         render_kw={'placeholder': 'Content'},
                         validators=[
                             DataRequired(message="Enter the text of your post.")
                         ])
    type = SelectField(label="Type",
                       render_kw={'placeholder': 'Type'},
                       choices=[(postType.name, postType.value.lower().capitalize()) for postType in PostType],
                       validators=[
                           DataRequired(message='Type selection is required.')
                       ])
    categories = SelectField('Category', coerce=int, validators=[
                             DataRequired(message='Category selection is required.')])
    tags = SelectMultipleField('Tags', coerce=int, option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False))

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.categories.choices = [(category.id, category.name) for category in Category.query.all()]
        self.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
    image = FileField('Profile picture',
                           render_kw={'placeholder': 'Image', 'accept': '.jpg, .jpeg, .png'})
    enabled = BooleanField('Enabled', default=True)

    def __init__(self):
        super().__init__()

    def validate_categories(self, field):
        category_id = field.data
        if not Category.query.get(category_id):
            raise ValidationError('Unknown category.')


class CategorySearchForm(FlaskForm):
    categories = SelectField('Category', coerce=int)

    def __init__(self, *args, **kwargs):
        super(CategorySearchForm, self).__init__(*args, **kwargs)
        self.categories.choices = [(category.id, category.name) for category in Category.query.all()]