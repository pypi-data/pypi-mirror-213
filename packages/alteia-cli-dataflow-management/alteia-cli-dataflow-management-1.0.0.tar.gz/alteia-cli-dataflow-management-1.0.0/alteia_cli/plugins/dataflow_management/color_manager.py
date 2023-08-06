import colorsys
import hashlib

import typer


def get_colored_field_exists(exists: bool) -> str:
    result = typer.style("No", fg=typer.colors.RED)
    if exists:
        result = typer.style("Yes", fg=typer.colors.GREEN)
    return result


class UniqueColor:
    # Ensure for a given string to always get the same color
    def __init__(self):
        self.colored = {}
        self.colors_used = []
        self.hue_start = 0.15  # chartreuse
        self.hue_end = 0.5  # cyan
        self.saturation = 0.9
        self.luminosity = 0.7

    def get_hue(self, to_color: str):
        # This is fun : we get the hash from md5, grab only the first byte part,
        # modulo it with 256 to get a range of 0-255, and divide it to get 0-1
        # So, for a given string, we have always the same hue
        return float((hashlib.md5(to_color.encode("utf-8")).digest()[0] % 256) / 256)

    def generate_color(self, to_color: str, try_nb=0):
        raw_hue = self.get_hue(to_color=to_color)
        result_color = tuple(
            int(x * 255)
            for x in colorsys.hls_to_rgb(raw_hue, l=self.luminosity, s=self.saturation)
        )

        if result_color not in self.colors_used:
            self.colors_used.append(result_color)
        else:
            if try_nb < 10:
                result_color = self.generate_color(try_nb=try_nb + 1, to_color=to_color)
        return result_color

    def get_colored(self, to_color):
        if to_color in self.colored:
            result_color = self.colored[to_color]
        else:
            result_color = self.generate_color(to_color=to_color)
            self.colored[to_color] = result_color
        return typer.style(to_color, fg=result_color)
