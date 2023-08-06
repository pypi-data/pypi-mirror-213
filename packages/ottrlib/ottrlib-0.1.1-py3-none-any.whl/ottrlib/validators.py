from typing import Iterator


class TemplateValidator:
    def __init__(self, template) -> None:
        self.template = template

    def validate(self, instance) -> Iterator:
        def parameters(number: int) -> str:
            if number == 1:
                return "1 parameter"
            else:
                return f"{number} parameters"

        def fewer_parameters(number: int) -> str:
            if number == 0:
                return "none were provided."
            elif number == 1:
                return "only 1 was provided."
            else:
                return f"only {number} were provided."

        def more_parameters(number: int) -> str:
            if number == 0:
                return "none were provided."
            elif number == 1:
                return "1 was provided."
            else:
                return f"{number} were provided."

        if len(instance.arguments) < len(
            [p for p in self.template.parameters if not p.optional]
        ):
            yield instance.create_error(
                f"Not enough parameters for an instance of {instance.name}! "
                f"The template expects {parameters(len(self.template.parameters))} but "
                + fewer_parameters(len(instance.arguments))
            )

        if len(instance.arguments) > len(self.template.parameters):
            yield instance.create_error(
                f"Too many parameters for an instance of {instance.name}! "
                f"The template expects {parameters(len(self.template.parameters))} but "
                + more_parameters(len(instance.arguments))
            )
