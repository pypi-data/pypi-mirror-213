from __future__ import annotations

import os
import re
import sys
import collections
import logging
from typing import Optional

import yaml

from gcln.exceptions import UserError

############


class WorkspaceRules:
    """helper class for the workspace rules part of config file"""
    def __init__(self, repo_rules:list[dict[str,str]], ws_rules:list[dict[str,str]]):
        self.repo_rules = repo_rules    # a list of dicts, every dict should have exactly one key
        self.ws_rules = ws_rules

        action_re = re.compile(r"(all|none|main|only_branches=\".*\")(?:, *(done))?")

        #print (repo_rules)


        def parse_rules(rules, do_regexp:bool):
            ret = []
            for r_dict in rules:
                if len(r_dict)!=1:
                    raise Exception("should be exactly one:"+str(r_dict))

                regexp, actions = list(r_dict.items())[0]
                m = action_re.match(actions)
                if not m:
                    print (f"Bad rule {regexp} {actions} - ignoring")
                #print (regexp, actions, ":::", m.groups())
                if do_regexp:
                    ret.append( (re.compile(regexp), m.groups()) )
                else:
                    ret.append( (regexp, m.groups()) )
            return ret

        self.repo_matches = parse_rules(self.repo_rules, do_regexp=False)
        self.ws_matches = parse_rules(self.ws_rules, do_regexp=True)
        self.repo_map_matches = collections.defaultdict(list)

        for repo_uid, action in self.repo_matches:
            self.repo_map_matches[repo_uid].append(action)

    def handle_actions(self, actions:list):
        res = True
        for action1,action2 in actions:
            if action1=="none":
                res = False
            elif action1=="all":
                res = True
            else:
                raise Exception("Unhandled action1", action1)

            if action2=="done":
                return res
            elif action2:
                raise Exception("Unhandled action1", action1)
        return res

    def include_repo(self, repo:records.RepoInfo) -> bool:
        if repo.uid in self.repo_map_matches:
            return self.handle_actions(self.repo_map_matches[repo.uid])
        else:
            return True

    def include_ws(self, repo:records.RepoInfo, co:records.GitCheckout) -> bool:
        actions = []
        for regexp, pair in self.ws_matches:
            if regexp.match(co.path):
                actions.append(pair)
        return self.handle_actions(actions)


#############

class Secrets(yaml.YAMLObject):
    """handles the separate yaml file"""
    yaml_tag = "!secrets"
    yaml_loader = yaml.SafeLoader
    yaml_flow_style = list
    secrets = {}
    root = ""

    def __init__(self, x):
        print("x")

    @classmethod
    def from_yaml(cls, loader, node):
        if "/" in node.value:
            fn, key = node.value.split("/")
        else:
            fn = node.value
            key = None
        path = os.path.join(cls.root, fn + ".yaml")
        ret = yaml.safe_load(open(path, "rt").read())
        if key:
            return ret[key]
        else:
            return ret

    @classmethod
    def old_load_secrets_file(cls, root, fn) -> None:
        path = os.path.join(root, fn + ".yaml")
        #cls.yaml_tag = "!" + fn
        if os.path.exists(path):
            cls.secrets = yaml.safe_load(open(path, "rt").read())
            print("***", cls.yaml_tag, cls.secrets)
        else:
            raise Exception()


#############


class Config():
    """loads the main config file, find the ws_root. Does _not_ connect to server etc"""
    def __init__(self, root_path:Optional[str]=None, args:Optional[object]=None) -> None:
        """Finds ws_root, loads it config file. if root_path is defined, it overrides args"""

        logging.debug(f"Config {root_path}, {str(args)}")

        self.ws_root: str
        self.cfg_file_fn: str = ""
        self.secret_fn: str
        #self.main_connector: Optional[ServerConnectorBase] = None
        self.data: dict
        #self.cache:Optional[TotoalCache] = None # TotalCache() # :Optional[dict] = None
        self.ws_rules: WorkspaceRules

        if root_path:
            self.ws_root = root_path
        elif args:
            if args.cfg:
                self.cfg_file_fn = args.cfg

            if args.root:
                self.ws_root = args.root
            else:
                if args.cfg:
                    self.ws_root = os.path.split(args.cfg)[0]
                else:
                    self.ws_root = os.getcwd()
        else:
            raise Exception("Needs either args or root_path")

        self.ws_root = os.path.abspath(self.ws_root)
        self.ws_root = self.ws_root.replace("\\","/")
        orig_ws_root = self.ws_root
        while not os.path.exists(os.path.join(self.ws_root,"gcln.yaml")):
            logging.debug(f"Config {self.ws_root}")
            new_path = os.path.abspath(self.ws_root+"/..").replace("\\","/")
            new_path = new_path.replace("//","/")
            if new_path==self.ws_root:
                self.ws_root=orig_ws_root
                break
            self.ws_root = new_path
            if not "/" in self.ws_root:
                break

        if not self.cfg_file_fn:
            self.cfg_file_fn = os.path.join(self.ws_root, "gcln.yaml")
        with open(self.cfg_file_fn, "rt") as fh:
            data = fh.read()
        #sfn = os.path.join(self.ws_root, "secrets.yaml")
        #sfn = os.path.join(self.ws_root, "ribbe-secrets.yaml")

        #Secrets.load_secrets_file(self.ws_root, "ribbe-secrets")
        Secrets.root = self.ws_root

        self.data = yaml.safe_load(data)
        if not isinstance(self.data, dict):
            raise UserError(f"gitlab cfg file {self.cfg_file_fn} must be a dict")

        if "workspace" not in self.data:
            self.data["workspace"] = {}
        self.cfg_workspace = self.data["workspace"]
        if "repo_rules" not in self.cfg_workspace:
            self.cfg_workspace["repo_rules"] = []
        if "ws_rules" not in self.cfg_workspace:
            self.cfg_workspace["ws_rules"] = []


        self.ws_gitconfig: dict = self.cfg_workspace.get("config", {})
        # print (self.ws_gitconfig)

        self.ws_branches = self.cfg_workspace.get("branches", True)
        self.ws_sub_tree = self.cfg_workspace.get("sub_tree", "")
        self.ws_home_prefix = self.cfg_workspace.get("home_prefix", "home").replace("\\", "/")
        if self.ws_home_prefix and not self.ws_home_prefix[-1] == "/":
            self.ws_home_prefix += "/"

        self.ws_rules = WorkspaceRules(self.cfg_workspace["repo_rules"], self.cfg_workspace["ws_rules"])

