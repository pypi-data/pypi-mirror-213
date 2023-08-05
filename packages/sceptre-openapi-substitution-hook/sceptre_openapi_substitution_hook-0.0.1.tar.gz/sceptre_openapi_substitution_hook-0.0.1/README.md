# README

## Overview

Performs simple string substitution in openapi specifications.

Should be used until CloudFormation [natively supports this feature][1].

## Installation

Installation instructions

To install directly from PyPI
```shell
python3 -m pip install sceptre-openapi-substitution-hook
```

To install from the git repo
```shell
python3 -m pip install git+https://github.com/nicholasphair/sceptre-openapi-substitution-hook
```

## Usage/Examples

Use the hook with a [hook point](https://docs.sceptre-project.org/latest/docs/hooks.html#hook-points)

```yaml
hooks:
  <hook_point>:
    - !openapi_substituter
      openapi:
        input: <input_path>
        output: <output_path>
        substitutions:
          <key>: <val>
```

The substituer will look for strings in the form of `${<key>}` and replace them
with `<val>`.

## Example

```yaml
hooks:
  before_validate:
    - !openapi_substituter
      openapi:
        input: ../templates/openapi.yaml
        output: ../templates/openapi.yaml
        substitutions:
          foo: bar
          baz: qux
```



[1]: https://github.com/aws-cloudformation/cloudformation-coverage-roadmap/issues/1233
