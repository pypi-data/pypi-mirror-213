import importlib
import pkgutil
import inspect
import pytest
import os
import pysnooper

from abc import ABC, abstractmethod


class Module(ABC):

    subclasses = []
    modules = {}

    def __init__(self) -> None:
        self.import_subclasses()
        self.modules = {
            item.__class__.__name__: item for item in self.subclasses
        }

    def import_subclasses(self) -> list:
        module_name = self.__module__
        package = importlib.import_module(module_name).__package__
        module = importlib.import_module(f'{package}.module')
        for cls_name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, Module) \
                    and obj != Module and cls_name != 'KayaStrategyModule':
                subclass_instance = obj()
                self.subclasses.append(subclass_instance)
        return self.subclasses

    # TODO - Refactor - run unit and sanity tests
    @pysnooper.snoop
    def run_tests(self, *args: str):
        results = {}
        test_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

        # TODO - Remove
        print(f'[ DEBUG ]: Test dir - {test_dir }')

        if 'unit' in args:
            unit_tests = pytest.main(['-s', '-v', test_dir])
            results.update({'unit-tests': unit_tests})
#       if 'integration' in args:
#           # TODO
#           integration_tests =
#           results.update({'integration-tests': integration_tests})
        return result

    @abstractmethod
    def main(self,) -> None:
        pass
