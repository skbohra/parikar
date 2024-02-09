from .models import Font,FontColor

def get_random_font():
    font = Font.objects.order_by('?').first()
    return font.font_name

def get_random_color():
    font_color = FontColor.objects.order_by('?').first()
    return font_color.hexcode
