import os
from unittest import TestCase, main

from la_env import EnvironmentMissing, env_exists


class TestFail(TestCase):
    def setUp(self) -> None:
        os.environ["LA_ENV_TEST2"] = "OKAY"

        return super().setUp()

    def test_missing_one(self):
        with self.assertRaises(EnvironmentMissing):
            env_exists(["LA_ENV_TEST1"])

    def test_missing_first(self):
        env_exists(["LA_ENV_TEST2"])

        with self.assertRaises(EnvironmentMissing):
            env_exists(["LA_ENV_TEST1", "LA_ENV_TEST2"])

    def test_missing_last(self):
        env_exists(["LA_ENV_TEST2"])

        with self.assertRaises(EnvironmentMissing):
            env_exists(["LA_ENV_TEST2", "LA_ENV_TEST1"])


if __name__ == "__main__":
    main()
