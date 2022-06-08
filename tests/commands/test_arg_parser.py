import pytest

from pyspeedinsights.cli.commands import parse_args, set_up_arg_parser


@pytest.fixture(autouse=True)
def mock_args(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "pytest",
            "https://www.example.com",
            "-c",
            "performance",
            "-l",
            "en",
            "-s",
            "desktop",
            "-uc",
            "test-uc",
            "-us",
            "test-us",
            "-t",
            "test-ct",
            "-f",
            "json",
            "-m",
            "all",
        ],
    )


def test_args_are_parsed_from_cmd_line():
    parser = set_up_arg_parser()
    args = parse_args(parser)
    assert args.url == "https://www.example.com"
    assert args.category == "performance"
    assert args.strategy == "desktop"
    assert args.locale == "en"
    assert args.utm_campaign == "test-uc"
    assert args.utm_source == "test-us"
    assert args.captcha_token == "test-ct"
    assert args.format == "json"
    assert args.metrics == ["all"]
