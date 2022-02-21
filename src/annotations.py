from typing import Dict, List


class Annotation:
    def __init__(self, name: str, interface: type):
        self.name = name
        self.interface = interface

    def __repr__(self):
        return f'{self.name}: {self.interface}'


class AnnotationManager:
    @staticmethod
    def from_dict(values: Dict[str, type]) -> List[Annotation]:
        annotations: List[Annotation] = []
        for value in values.items():
            annotations.append(Annotation(value[0], value[1]))

        return annotations
