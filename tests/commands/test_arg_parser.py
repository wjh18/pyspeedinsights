from argparse import Namespace

import pytest

from pyspeedinsights.cli.commands import (
    arg_group_to_dict,
    create_arg_groups,
    set_up_arg_parser,
)


class TestArgParser:
    """Tests parsing of arguments from cli with argparse."""

    def raises_system_exit(self):
        parser = set_up_arg_parser()
        with pytest.raises(SystemExit):
            parser.parse_args()

    def test_no_args_exits(self):
        self.raises_system_exit()

    def test_help_arg_exits(self, patch_argv):
        patch_argv(["psi", "--help"])
        self.raises_system_exit()

    def test_no_url_exits(self, patch_argv):
        patch_argv(["psi", "-c" "seo"])
        self.raises_system_exit()

    def test_invalid_choice_exits(self, patch_argv):
        patch_argv(["psi", "-c" "invalid"])
        self.raises_system_exit()

    def test_parse_all_args(self, patch_argv, all_args):
        patch_argv(all_args)
        parser = set_up_arg_parser()
        args = parser.parse_args()
        for arg in vars(args).values():
            if type(arg) == list:
                arg = arg[0]
            assert arg in all_args


class TestCreateArgGroups:
    """Tests creation of argument groups."""

    def get_arg_groups(self):
        parser = set_up_arg_parser()
        args = parser.parse_args()
        return create_arg_groups(parser, args)

    def test_groups_are_created(self, patch_argv):
        patch_argv(["psi", "url"])
        arg_groups = self.get_arg_groups()
        assert type(arg_groups) == dict
        assert "Processing Group" and "API Group" in arg_groups.keys()
        for v in arg_groups.values():
            assert type(v) == Namespace

    def test_args_belong_to_correct_group(self, patch_argv):
        patch_argv(["psi", "url", "-c", "seo", "-f", "json"])
        arg_groups = self.get_arg_groups()
        assert arg_groups["API Group"].category == "seo"
        assert arg_groups["Processing Group"].format == "json"

    def test_arg_group_to_dict(self, patch_argv):
        patch_argv(["psi", "url", "-c", "seo", "-f", "json"])
        arg_groups = self.get_arg_groups()
        api_args_dict = arg_group_to_dict(arg_groups, "API Group")
        assert api_args_dict.get("category") == "seo"
        proc_args_dict = arg_group_to_dict(arg_groups, "Processing Group")
        assert proc_args_dict.get("format") == "json"
