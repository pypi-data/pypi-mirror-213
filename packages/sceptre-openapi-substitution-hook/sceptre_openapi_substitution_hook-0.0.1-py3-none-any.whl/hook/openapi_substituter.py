# -*- coding: utf-8 -*-
from pathlib import Path

from sceptre.exceptions import InvalidHookArgumentTypeError
from sceptre.hooks import Hook

OPENAPI_KEY = "openapi"
OPENAPI_INPUT_PATH_KEY = "input"
OPENAPI_OUTPUT_PATH_KEY = "output"
OPENAPI_SUBSTITUTIONS_KEY = "substitutions"


class OpenApiSubstituter(Hook):
    def assert_arguments(self):
        if not self.argument:
            raise Exception(InvalidHookArgumentTypeError)

        if not self.argument.get(OPENAPI_KEY):
            raise Exception(InvalidHookArgumentTypeError)

        if not self.argument.get(OPENAPI_KEY, {}).get(OPENAPI_INPUT_PATH_KEY):
            raise Exception(InvalidHookArgumentTypeError)

        if not self.argument.get(OPENAPI_KEY, {}).get(OPENAPI_SUBSTITUTIONS_KEY):
            raise Exception(InvalidHookArgumentTypeError)

    def run(self):
        self.assert_arguments()

        openapi_input_path = self.argument.get(OPENAPI_KEY, {}).get(
            OPENAPI_INPUT_PATH_KEY
        )
        openapi_output_path = self.argument.get(OPENAPI_KEY, {}).get(
            OPENAPI_OUTPUT_PATH_KEY, openapi_input_path
        )
        openapi_substitutions = self.argument.get(OPENAPI_KEY, {}).get(
            OPENAPI_SUBSTITUTIONS_KEY
        )

        input_path = Path(openapi_input_path)
        if not input_path.exists():
            raise Exception(InvalidHookArgumentTypeError)

        output_path = Path(openapi_output_path)
        if not output_path.parent.exists():
            raise Exception(
                InvalidHookArgumentTypeError, "output directory does not exist"
            )

        with open(input_path, "r") as i:
            spec = i.read()
            for old, new in openapi_substitutions.items():
                old_formatted = f"${{{old}}}"
                spec = spec.replace(old_formatted, str(new))
            with open(output_path, "w") as o:
                o.write(spec)
