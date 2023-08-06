from .colormap import color_map
class Blessable:
    def bless(self, markup):
        parts = markup.split('<')
        converted_markup = ''
        for part in parts:
            if '>' in part:
                color_tag, text = part.split('>', 1)
                color_tag = color_tag.strip()
                if color_tag in color_map:
                    converted_markup += color_map[color_tag](text)
                else:
                    converted_markup += text
            else:
                converted_markup += part
        return converted_markup
