import sys

from tests.excel import test_excel


def main():
    test_excel.run_tests()


if __name__ == '__main__':
    sys.path.append('./src/pyspeedinsights')
    main()