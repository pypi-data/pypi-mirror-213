from __future__ import annotations

import os
import pygit2
import logging
import subprocess
import datetime
from typing import Optional

import yaml

import secrets

# pip install python-dateutil
import dateutil.parser

def date_str_to_utc(s: str) -> float:
    dt: datetime.datetime = dateutil.parser.parse(s)
    return dt.timestamp()

def name_to_ws_path(name: str) -> str:
    parts = name.split("/")
    parts = [p.strip() for p in parts]
    parts = [p for p in parts if p]    # remove empty parts
    parts = [p[:-1] if p[-1] == "_" else p for p in parts]        # remove trailing _
    res = "/".join(parts)
    return res

def cmd(args: list[str], allow_nonzero: bool = False, work_dir=None, retries=0, dry_run=False, raise_exception=True):
    retry = 0
    try:
        if work_dir:
            old_dir = os.getcwd()
            os.chdir(work_dir)

        while 1:
            logging.debug(f"CMD ({os.getcwd()}):{args}")
            if dry_run:
                logging.debug(f"  => dry run")
                return 0
            else:
                cp = subprocess.run(args)
                logging.debug(f"  => {cp}")
                if cp.returncode and not allow_nonzero:
                    if retry >= retries:
                        if raise_exception:
                            raise Exception("Got return code %d" % cp.returncode)
                        else:
                            logging.error(f"Error: give up after {retry} tries. Got return code {cp.returncode}")
                            return cp.returncode
                    else:
                        retry += 1
                        logging.error(f"Error: got return code {cp.returncode}, retry {retry}/{retries}")
                else:
                    return cp.returncode
    finally:
        if work_dir:
            os.chdir(old_dir)




#def uid_get_abs_from_relpath(relative_url:str, parent_rem_url: str, remove_protocol=False) -> str:
def remove_protocol_host_from_url(url: str) -> str:
    for pre in ("ssh://", "http://", "https://"):
        if url.startswith(pre):
            t = url[len(pre):]
            return t[t.index("/") + 1:]
    return url


def url_make_absolut(pre, post):
    pre = pre.replace("\\", "/")
    post = post.replace("\\", "/")
    while pre.endswith("/"):
        pre = pre[:-1]
    while post.startswith("../"):
        post = post[3:]
        if "/" in pre:
            pre = pre[:pre.rfind("/")]
        else:
            pre = ""
    if pre:
        return pre + "/" + post
    else:
        return post


def uid_get_url_from_abs_path(repo_abs_url:str, parent_rem_url: str) -> Optional[str]:
    """return absolute url from absolute path, ie, add protocl/hostname. Or None if cannot be found"""
    logging.debug("uid_get_url_from_abs_path: %s : %s" % (repo_abs_url, parent_rem_url))
    for pre in ("ssh://", "http://", "https://"):
        if parent_rem_url.startswith(pre):
            t = parent_rem_url[len(pre):]
            hostname = t[:t.index("/") + 1]
            ret = pre + hostname + repo_abs_url
            if not ret.endswith(".git"):
                ret += ".git"
            return ret
    return None


def get_user(repo_path, user_fatal=False) -> Optional[tuple(str, str)]:
    r = pygit2.Repository(repo_path)
    try:
        return (r.config["user.name"], r.config["user.email"])
    except:
        if userfatal:
            raise Exception("""You need to set user, either locally, or globally with
    git config --global user.name "Your Name"
    git config --global user.email you@example.com
""")
        else:
            return None



class RepoWrapper:
    def __init__(self, repo_path: str):
        self.repo:Optional[pygit2.Repository] = None

        repo_path = pygit2.discover_repository(repo_path)   # actually workspace path
        if not repo_path:
            raise Exception()
        repo_path = repo_path.replace("\\","/")
        while repo_path.endswith("/"):
            repo_path = repo_path[:-1]
        if repo_path.endswith("/.git"):
            repo_path = repo_path[:-5]
        # print (repo_path)
        self.repo_path = os.path.abspath(repo_path)
        # print (repo_path)

    def open(self):
        self.repo = pygit2.Repository(self.repo_path)

class WorkspaceWrapper(RepoWrapper):
    """repo wrapper, but assumes there is a local workspace"""
    def __init__(self, ws_path: str):
        self.ws_path: str = os.path.abspath(ws_path)

        while 1:
            if os.path.exists(self.ws_path + "/.git"):
                super().__init__(self.ws_path)
                return
            self.ws_path = os.path.abspath(os.path.join(self.ws_path, ".."))




class RepoCfg(RepoWrapper):
    """Encapsulated cfg variable for a repo/workspace"""
    def __init__(self, repo_path: str, no_fetch = False):
        super().__init__(repo_path)
        self.cfg_data: dict = {}
        self.commit_sha: str = ""

        if not no_fetch:
            cmd(["git", "fetch", "origin", "_config:_config"], work_dir=self.repo_path, allow_nonzero=True)

        r = pygit2.Repository(self.repo_path)

        def get_cfg_data(ref: str) -> Optional[tuple[dict, str]]:
            if ref not in r.references:
                return None
            commit = r.references[ref].peel()
            tree = commit.tree
            obj_id = tree["attributes.yaml"]
            return (yaml.safe_load(obj_id.read_raw().decode("utf8")), commit.id)

        local = get_cfg_data("refs/heads/_config")
        origin = get_cfg_data("refs/remotes/origin/_config")

        if local and origin:
            if local[1] != origin[1]:
                raise Exception("TODO: local and origin _config branches points to different commits")
        if local:
            self.cfg_data, self.commit_sha = local
        elif origin:
            self.cfg_data, self.commit_sha = origin



    def create_random_uid(self, uidlen=32, force=False) -> None:
        if self.cfg_data and not force:
            raise Exception("Need --force to overwrite existing uid. Be careful with that!")

        # make lower case + digit str (5 bits/char):
        uid_str = ""
        for _ in range(uidlen):
            v = secrets.randbits(5)
            if v < 26:
                c = chr(ord('a') + v)
            else:
                c = chr(ord('0') + v - 26)
            uid_str += c
        self.cfg_data["uid"] = uid_str



    def commit_and_push(self, no_push):
        person = get_user(self.repo_path, user_fatal=True)
        r = pygit2.Repository(self.repo_path)
        tree = r.TreeBuilder()
        attr_oid = r.create_blob(yaml.safe_dump(self.cfg_data).encode("utf8"))
        tree.insert("attributes.yaml", attr_oid, pygit2.GIT_FILEMODE_BLOB)
        tree_oid = tree.write()
        signature = pygit2.Signature(*person)   # "system","system@none")
        if self.commit_sha:
            parents = [self.commit_sha]
        else:
            parents = []
        comm_oid = r.create_commit("refs/heads/_config", signature, signature, "create _config", tree_oid, parents)

        if not no_push:
            print("Pushing change to origin:")
            cmd(["git", "push", "origin", "_config"], work_dir=self.repo_path, allow_nonzero=True)


