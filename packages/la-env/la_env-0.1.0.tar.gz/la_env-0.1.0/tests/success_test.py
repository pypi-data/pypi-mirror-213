import os
from unittest import TestCase, main

from la_env import env_exists


class TestSuccess(TestCase):
    def setUp(self) -> None:
        os.environ["LA_ENV_TEST1"] = "OKAY"
        os.environ["LA_ENV_TEST2"] = "OKAY"
        os.environ["LA_ENV_TEST3"] = "OKAY"

        return super().setUp()

    def test_existing_one(self):
        env_exists(["LA_ENV_TEST1"])

    def test_existing_two(self):
        env_exists(["LA_ENV_TEST1", "LA_ENV_TEST2"])

    def test_missing_three(self):
        env_exists(["LA_ENV_TEST1", "LA_ENV_TEST2", "LA_ENV_TEST3"])


if __name__ == "__main__":
    main()
