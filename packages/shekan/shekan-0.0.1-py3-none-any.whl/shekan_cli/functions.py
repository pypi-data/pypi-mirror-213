
class TextStyle:
    GREEN = "\033[92m"
    RED = "\033[91m"
    NC = "\033[0m"  # No Color


def colorify(text: str, style: TextStyle):
    return f"{style}{text}{TextStyle.NC}"