from abc import ABC, abstractmethod


class OutputFormatter(ABC):
    @abstractmethod
    def format(self, mode: str = "standard") -> str:
        pass

    @staticmethod
    def trim(content, top=0, tail=0):
        if top or tail:
            lines = content.splitlines()
            lines_to_return = []

            if top + tail > len(lines):
                return content

            if top > 0:
                lines_to_return.extend(lines[:top])

            if (rest := len(lines) - top - tail) > 0:
                lines_to_return.append(f"# ... {rest} other lines ...")

            if tail > 0:
                lines_to_return.extend(lines[-tail:])

            return "\n".join(lines_to_return)
        else:
            return content
