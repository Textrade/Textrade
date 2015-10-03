from models import BookRent


def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def create_book_rent(**kwargs):
    """Create a book for rent."""
    BookRent.create(
        name=kwargs['name'],
        #author=kwargs['author'],
        isbn=kwargs['isbn'],
        condition=kwargs['condition'],
        username=kwargs['username'],
        available='available',
        image_path=kwargs['img_path']
    )
