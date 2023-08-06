import unittest
from unittest.mock import patch


class ContainerTest(unittest.TestCase):
    @patch("p360_export.utils.utils.resolve_dbutils")
    def test_init(self, patched_resolve_dbutils):
        from p360_export.containers.Container import Container, get_local_config  # pylint: disable=C0415

        patched_resolve_dbutils.return_value = 1
        container = Container()
        container.config.from_dict(get_local_config())
        container.wire(modules=[__name__])

        container.check_dependencies()


if __name__ == "__main__":
    unittest.main()
