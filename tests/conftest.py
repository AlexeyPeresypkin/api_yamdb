# Тесты для rest

# pytest_plugins = [
#     'tests.fixtures.fixture_user',
#     # 'tests.fixtures.fixture_data',
# ]

# Тесты для docker
import sys
from os.path import abspath
from os.path import dirname

root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(root_dir)


pytest_plugins = [
]
