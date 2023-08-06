# la-env
Simple function to raise error if environment variables do not exists.

# install
`pip install la-env`

# usage
```python
from la_env import env_exists

env_exists(["POSTGRES_URI", "RABBIT_URI", "REDIS_URI"])
```