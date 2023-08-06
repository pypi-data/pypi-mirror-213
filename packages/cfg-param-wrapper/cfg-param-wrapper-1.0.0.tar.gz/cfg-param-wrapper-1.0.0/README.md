# cfg_param_wrapper 1.0.0

a config wrapper I made. It's made to wrap simple functions, and intercept configurations in tandem with a CfgDict object.

## Installation

```bash
# from pypi:
pip install cfg-argparser

# from github:
git clone "https://github.com/zeptofine/cfg-argparser"
cd cfg-argparser
pip install -e .

```

## Example

```python
from cfg_param_wrapper import wrap_config, CfgDict

cfg = CfgDict("test.json")
@wrap_config(cfg)
def test_function(s: str, is_real: bool = True): # I'd advise only wrapping functions all having default methods
    return f"{s} is {'real' if is_real else 'fake'}"

if __name__ == "__main__":
  print(test_function("We"))
  cfg['s'] = "us"
  print(test_function()) # Linters hate him!
```

## Compatibilty

This was mainly tested on 3.9 and 3.10, but it should work from 3.6 onwards. i can't test earlier versions for some reason.
