import unittest

# import all test cases, otherwise unittest won't find them
from tests.dict_helper import (
    DropUndefinedUseCase, 
    DropExceptKeysUseCase, 
    AsDictDataclassUseCase
)

from tests.test_user_repo import postgres_container
if __name__ == "__main__":
    unittest.main()

from unittest import TestCase