# light_scores
<!--- light_scores  light_scores  light_scores light_scores --->
[![tests](https://github.com/ffreemt/light_scores/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/light_scores.svg)](https://badge.fury.io/py/light_scores)

Calculate bm25 matrix of two lists

## Usage

```python
from light_scores.light_scores import light_scores

res = await light_scores("test me")
print(res)
# '考我 试探我 测试我 试探'

print(await light_scores("test me", to_lang="de"))