from .models import Section


def show_pages_menu(context):
    pages_menu = Section.objects.all()
    menu_root = Section.objects.first().get_root()
    return {'menu': pages_menu}
