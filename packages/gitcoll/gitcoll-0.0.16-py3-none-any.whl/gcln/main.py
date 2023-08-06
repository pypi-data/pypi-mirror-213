#!/usr/bin/env python3

# hopefully works on py3.8 too:
from __future__ import annotations

import os
import re
import sys
import time
import stat
import shlex
import base64
import pickle
import secrets
import logging
import argparse
import datetime
#import binascii
import itertools
import subprocess
import collections
import configparser

import yaml
import dataclasses

import gitlab   # pip3 install python-gitlab
import pygit2   # pip3 install pygit2

from gcln import helpers
from gcln import cfg_file
from gcln import main_context
from gcln.exceptions import UserError

__version__ = "0.0.12pre"





####################################################################################
####################################################################################
####################################################################################


def main_interactive(args) -> None:
    raise Exception("TODO")

def main_update(args) -> None:
    t0 = time.time()
    mc = main_context.WSContext(args=args, skip_ws_scan=False)
    #print (dir(mc))
    t1 = time.time()

    mc.update()
    mc.cache.write_cache()
    t2 = time.time()

    #raise Exception("TODO")

####################################################################################

def main_update_cache(args) -> None:
    args.status = True  # force check local status
    main_context.WSContext(args=args, skip_ws_scan=True)


####################################################################################

def main_check(args) -> None:
    raise Exception("TODO")

####################################################################################

def main_status(args) -> None:
    mc = main_context.WSContext(args=args, skip_ws_scan=False)
    mc.status()

####################################################################################

def main_git_config(args) -> None:
    mc = main_context.WSContext(args=args, skip_ws_scan=False)
    print ("Git config", mc.cfg.ws_gitconfig)
    for co in mc.cache.total_cache.checkouts:
        if os.path.isdir(co.path):
            print (co.path)
            for key, val in mc.cfg.ws_gitconfig.items():
                helpers.cmd(["git", "config", key, val], work_dir = co.path)
        else:
            print ("****ERROR", co.path)

####################################################################################
def main_conv_ssh_auth(args) -> None:
    raise Exception("TODO")
def main_ssh_proxy(args) -> None:
    raise Exception("TODO")
def main_set_aux_remote(args) -> None:
    raise Exception("TODO")

####################################################################################

def main_dbg(args) -> None:
    raise Exception("TODO")

####################################################################################

def main_test1(args) -> None:
    t0 = time.time()
    mc = main_context.WSContext(args=args, skip_ws_scan=False)
    #print (dir(mc))
    t1 = time.time()
    print("time", t1 - t0)

    raise Exception("TODO")

####################################################################################

def main_test2(args) -> None:
    #raise Exception("TODO")
    #os.system("ssh git-jt@jobby.job-tech.se -C ls")
    print ("Running: test2")
    t0 = time.time()
    mc = main_context.WSContext(args=args, skip_ws_scan=True)
    t1 = time.time()
    print("*****time1:", t1 - t0)

    import srv_connector
    gc: srv_connector.GitlabConnector = mc.main_connector

    t0 = time.time()
    x = gc.gl_get_all_groups(0)
    print (len(x))
    x = gc.gl_get_all_projects(0)
    print (len(x))
    t1 = time.time()
    print("*****time2:", t1 - t0)


####################################################################################





def main_cfg(args) -> None:
    rc = helpers.RepoCfg(".", args.nofetch)
    #print(rc.cfg_data, rc.commit_sha)

    if args.show:
        print("Commit:", rc.commit_sha)
        print("cfg data:", rc.cfg_data)

    if args.set_rnd_uid:
        if rc.cfg_data:
            raise Exception("Need --force to overwrite existing uid. Be careful with that!")
        rc.create_random_uid()

        print("new cfg data:", rc.cfg_data)

        rc.commit_and_push(args.nopush)

        return


    raise Exception("TODO")


####################################################################################

def main_pull_bare_worker(args, uid_url_map:dict[str,str]) -> None:
    existing_repos_ids:set = {name[:-4] for name in os.listdir(args.directory) if name.endswith(".git")}

    if 1:
        for uid, url in uid_url_map.items():
            dst_path = os.path.join(args.directory, uid+".git")
            print (f"* {uid} @ {url}")
            if os.path.exists(dst_path):
                helpers.cmd(["git", "fetch", url, "*:*"], work_dir=dst_path, allow_nonzero=True)
            else:
                if args.no_clone:
                    print (f"No local repo for uid {uid} @ {url}")
                else:
                    helpers.cmd(["git", "clone", "--bare", url, dst_path], allow_nonzero=True)

    repos_not_on_server = existing_repos_ids - set(uid_url_map.keys())
    if repos_not_on_server:
        print ("The following uids on local disk does not exist on the server:")
        for uid in repos_not_on_server:
            print (uid)

def main_pull_bare_repo_list(args, repo_list:dict) -> None:
    id_url_map = {}
    for repo_id, repo_path in repo_list["repos"].items():
        dst_path = os.path.join(args.directory, repo_id+".git")
        dst_path = os.path.abspath(dst_path)
        url = repo_list["server"]["git_url"]+"/"+repo_path

        id_url_map[repo_id] = url
    main_pull_bare_worker(args, id_url_map)

def main_pull_bare_gitlab(args) -> None:
    mc = main_context.WSContext(args=args)
    id_url_map = {}

    for r in mc.cache.total_cache.main_server.repos:
        if not r.uid:
            print (f"Skipping due to no uid: {r.server_full_path}")
            continue

        url = mc.main_connector.url_root + "/" + r.server_full_path + ".git"
        id_url_map[r.uid] = url

    main_pull_bare_worker (args, id_url_map)


def main_pull_bare(args) -> None:
    if not os.path.isdir(args.directory):
        print (f"{args.directory} is not a directory")
        return -1

    if args.repo_list:
        repo_list = yaml.safe_load(open(args.repo_list, "rt").read())
        main_pull_bare_repo_list(args, repo_list)
    else:
        main_pull_bare_gitlab(args)

####################################################################################

def main_push_bare_worker(args, uid_url_map:dict[str,str]) -> None:
    existing_repos_ids:set = {name[:-4] for name in os.listdir(args.directory) if name.endswith(".git")}

    if 1:
        for uid, url in uid_url_map.items():
            dst_path = os.path.join(args.directory, uid+".git")
            if not os.path.exists(dst_path):
                print (f"Missing uid {uid} in {args.directory}")
                continue
            else:
                helpers.cmd(["git", "push", "--all", url], work_dir=dst_path, allow_nonzero=True)

    repos_not_on_server = existing_repos_ids - set(uid_url_map.keys())
    if repos_not_on_server:
        print ("The following uids on local disk does not exist on the server:")
        for uid in repos_not_on_server:
            print (uid)


def main_push_bare_repo_list(args, repo_list:dict) -> None:
    id_url_map = {}
    for repo_id, repo_path in repo_list["repos"].items():
        dst_path = os.path.join(args.directory, repo_id+".git")
        dst_path = os.path.abspath(dst_path)
        url = repo_list["server"]["git_url"]+"/"+repo_path

        id_url_map[repo_id] = url
    main_push_bare_worker (args, id_url_map)



def main_push_bare_gitlab(args) -> None:
    mc = main_context.WSContext(args=args)
    id_url_map = {}

    for r in mc.cache.total_cache.main_server.repos:
        if not r.uid:
            print (f"Skipping due to no uid: {r.server_full_path}")
            continue

        url = mc.main_connector.url_root + "/" + r.server_full_path + ".git"
        id_url_map[r.uid] = url

    main_push_bare_worker (args, id_url_map)

def main_push_bare(args) -> None:
    if not os.path.isdir(args.directory):
        print (f"{args.directory} is not a directory")
        return -1

    if args.repo_list:
        repo_list = yaml.safe_load(open(args.repo_list, "rt").read())
        main_push_bare_repo_list(args, repo_list)
    else:
        main_push_bare_gitlab(args)

####################################################################################

@dataclasses.dataclass
class SyncServer:
    name: str = ""
    path: str = ""
    ignore_repos: set[str] = dataclasses.field(default_factory=set)
    repo_list: str = ""
    cfg_file: str = ""
    repos2branches: dict[str, set[str]] = dataclasses.field(default_factory=dict)        # normally not defined in the yaml-file, but calculated
    repo_list_obj: Optional[dict] = None
    cfg_obj: Optional[str] = None
    repos_root_group: str = ""

    @classmethod
    def from_dict(cls, d: dict, root: str, name="", args_all=False, args_groups=False):
        d["ignore_repos"] = {str(r) for r in d.get("ignore_repos", [])}
        allowed_keys = set(cls.__dataclass_fields__.keys())
        for k in d.keys():
            if k not in allowed_keys:
                raise UserError(f"server definition key '{k}' not one of {allowed_keys}")

        ret = cls(**d)

        if not ret.path:
            ret.path = ret.name
            logging.debug("Path not defined, so setting server path to server name")

        ret.path = os.path.abspath(os.path.join(root, ret.path))
        if ret.repo_list:
            logging.debug("SyncServer.from_dict repo_list=%s" % ret.repo_list)
            # TODO: if container dir doesn't exist, create it (or somewhere else!)
            fn = os.path.abspath(os.path.join(ret.path, "..", ret.repo_list))
            ret.repo_list_obj = yaml.safe_load(open(fn, "rt").read())
            if not isinstance(ret.repo_list_obj, dict):
                raise UserError(f"repo list file {fn} for server {ret.name} is not a dict")
        if ret.cfg_file:
            logging.debug("SyncServer.from_dict cfg_file=%s" % ret.cfg_file)
            @dataclasses.dataclass
            class Arg:
                root: str = ""
                cfg: str = ""
                all: bool = args_all
                status: bool = False
                groups: bool = args_groups
            arg = Arg(cfg=os.path.abspath(os.path.join(ret.path, "..", ret.cfg_file)))
            logging.debug("SyncServer.from_dict cfg_file2: %s" % str(arg))
            ret.cfg_obj = main_context.WSContext(args=arg, srv_name=name)
        if ret.repos_root_group:
            while ret.repos_root_group.endswith("/"):
                ret.repos_root_group = ret.repos_root_group[:-1]
            if ret.repos_root_group:
                ret.repos_root_group += "/"

        if name:
            ret.name = name
        return ret


    def populate_repos_from_local(self, ss:"SyncSettings") -> None:
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        repo_ids = os.listdir(self.path)
        repo_ids = [rid[:-4] for rid in repo_ids if rid.endswith(".git")]
        repo_ids = [rid for rid in repo_ids if (not ss.ignorer.is_repo_id_ignored(rid)) and (rid not in self.ignore_repos)]
        for rid in repo_ids:
            repo = pygit2.Repository(os.path.join(self.path, rid+".git"))
            branches = {b for b in repo.branches.local if not ss.ignorer.is_branch_ignored(rid, b)}
            self.repos2branches[rid] = branches



def main_pull_bare_worker2(srv: SyncServer, uid_url_map: dict[str, str], no_clone=False) -> None:
    existing_repos_ids: set = {name[:-4] for name in os.listdir(srv.path) if name.endswith(".git")}

    if 1:
        for uid, url in uid_url_map.items():
            dst_path = os.path.join(srv.path, uid + ".git")
            print(f"* {uid} @ {url}")
            if os.path.exists(dst_path):
                helpers.cmd(["git", "fetch", url, "*:*", "--force"], work_dir=dst_path, allow_nonzero=True)
            else:
                if no_clone:
                    print(f"No local repo for uid {uid} @ {url}")
                else:
                    helpers.cmd(["git", "clone", "--bare", url, dst_path], allow_nonzero=True)

    repos_not_on_server = existing_repos_ids - set(uid_url_map.keys())
    if repos_not_on_server:
        print("The following uids on local disk does not exist on the server:")
        for uid in repos_not_on_server:
            print(uid)


class IgnoreBranchesAndRepos:
    def __init__(self, src_ignore_branches:Optional[list]):
        self.ignore_branches = collections.defaultdict(list)
        self.ignore_repos = set()

        if not src_ignore_branches:
            src_ignore_branches = []
        ibs1 = set(src_ignore_branches)

        for ib in ibs1:
            if ":" not in ib:
                rid = ""
                branch = ib
            else:
                rid = ib.split(":", maxsplit=1)[0]
                branch = ib[len(rid)+1:]
            if not branch:
                self.ignore_repos.add(rid)
            else:
                self.ignore_branches[rid].append(re.compile(branch))

    def is_branch_ignored(self, repo_id: str, branch_name: str) -> bool:
        for ignore in self.ignore_branches[""] + self.ignore_branches[repo_id]:
            if ignore.match(branch_name):
                return True
        return False

    def is_repo_id_ignored(self, repo_id: str) -> bool:
        return repo_id in self.ignore_repos



class SyncSettings:
    def __init__(self, control_file:str, args_all:bool, args_group:bool):
        if os.path.isdir(control_file):
            control_file = os.path.join(control_file, "sync.yaml")
        self.control_filename = os.path.abspath(control_file)
        self.main_dir = os.path.split(self.control_filename)[0]
        self.control_file: dict = yaml.safe_load(open(self.control_filename, "rt").read())
        self.ignorer = IgnoreBranchesAndRepos(self.control_file.get("ignore_branches"))
        self.servers: dict[str, SyncServer] = {}
        logging.debug("SyncSetting, about to go through servers and items")

        if not "servers" in self.control_file:
            raise UserError(f"control file {self.control_filename} must have a dict 'servers'")

        for name, server_dict in self.control_file["servers"].items():
            if not isinstance(server_dict, dict):
                raise UserError(f"control file {self.control_filename}, item servers[{name}] must be a dict")
            logging.debug(f"SyncSetting {name} with {len(server_dict)} servers")
            self.servers[name] = SyncServer.from_dict(server_dict, self.main_dir, name, args_all=args_all, args_groups=args_group)

    def populate_servers(self):
        for srv in self.servers.values():
            srv.populate_repos_from_local(self)



def main_sync(args) -> None:
    if args.server:
        print ("Should only operate on that server, but not implemented yet")
        return -1

    logging.debug("about to get SyncSetting")
    ss = SyncSettings(args.control_file, args.all, args.groups)

    logging.debug("got SyncSetting")

    if args.pull:
        for name, srv in ss.servers.items():
            logging.debug(f"{name} from {srv}")
            if not os.path.exists(srv.path):
                os.mkdir(srv.path)
            if srv.cfg_obj:
                repos_dict = {}
                for r in srv.cfg_obj.cache.total_cache.main_server.repos:
                    if not r.uid:
                        logging.warning(f"Skipping due to no uid: {r.server_full_path}")
                        continue
                    if ss.ignorer.is_repo_id_ignored(r.uid):
                        logging.debug(f"Skipping due it should be ignored {r.uid} / {r.server_full_path}")
                        continue

                    branches = {b.name for b in r.branches if not ss.ignorer.is_branch_ignored(r.uid, b.name)}

                    local_path = os.path.join(srv.path, r.uid + ".git")
                    repos_dict[local_path] = (r.uid, branches)
                    for auid in r.alt_uids:
                        local_path = os.path.join(srv.path, auid + ".git")
                        repos_dict[local_path] = (auid, branches)


                updates = srv.cfg_obj.check_if_local_bare_repo_diffs(repos_dict, ss.ignorer)  # dict, keys=repo_uid, value=set(branch_names)

                repos = [ (uid,srv.cfg_obj.cache.map_all_uid_repos[uid]) for uid in updates.keys()]

                # note that we ignore branches here - just pull all
                id_url_map = {uid: srv.cfg_obj.main_connector.url_root + "/" + repo.server_full_path + ".git" for uid, repo in repos}
                main_pull_bare_worker2(srv, id_url_map)
            elif srv.repo_list_obj:

                id_url_map = {}
                if "repos" not in srv.repo_list_obj:
                    raise UserError(f"repo list file for server {srv.name} doesn't contain the repos member")
                for repo_id, repo_path in srv.repo_list_obj["repos"].items():
                    url = srv.repo_list_obj["server"]["git_url"] + "/" + repo_path

                    id_url_map[repo_id] = url
                main_pull_bare_worker2(srv, id_url_map)
            else:
                raise UserError(f"Server {srv.name} has neither gitlab nor raw git server. Ie, supply either repo_list or cfg_file")

    #######################
    # create missing repos:
    if 1:
        repos_map = collections.defaultdict(collections.defaultdict)
        for srv_name, srv in ss.servers.items():
            if not srv.cfg_obj:
                logging.warning(f"srv {srv_name} is probably not a gitlab server. Ignoring")
                continue
            logging.debug(f"check srv {srv_name}")
            for r in srv.cfg_obj.cache.total_cache.main_server.repos:
                if not r.server_full_path.startswith(srv.repos_root_group):
                    logging.warning(f"Skipping due to srv repo path {r.server_full_path} does not begin with grp {srv.repos_root_group}")
                    continue
                if not r.uid:
                    logging.warning(f"Skipping due to no uid: {r.server_full_path}")
                    continue
                repo_info = repos_map[r.uid]
                if "#sub-path" not in repo_info:
                    repo_info["#sub-path"] = r.server_full_path[len(srv.repos_root_group):]
                if "#name" not in repo_info:
                    repo_info["#name"] = r.server_name      # repo name
                repo_info[srv_name] = r

        # print(yaml.dump(repos_map))

        for r_uid, repo_info in repos_map.items():
            group_map = collections.defaultdict(collections.defaultdict)
            for srv_name, srv in ss.servers.items():
                if not srv.cfg_obj:
                    continue
                gm = group_map[srv_name]
                if srv_name not in repo_info:
                    dst_full_path = srv.repos_root_group + repo_info['#sub-path']
                    x = dst_full_path.split("/")
                    dst_groups = x[:-1]
                    if not dst_groups:
                        logging.warning("Not implemented to create root projects/or private?")
                        continue
                    dst_name = x[-1]
                    logging.debug(f"Should create repo {r_uid} - {repo_info['#sub-path']} on server {srv_name} as {dst_full_path}, ie {dst_name} in {dst_groups}")
                    srv.cfg_obj: main_context.WSContext
                    gl_connector = srv.cfg_obj.main_connector

                    # first find/create the containing group:
                    parent_grp = None
                    for i in range(len(dst_groups)):
                        grp_path = "/".join(dst_groups[:i + 1])
                        if grp_path not in gm:
                            g = gl_connector.gl_get_group(grp_path)
                            if not g:
                                # need to create group
                                g = gl_connector.gl_create_group(parent=parent_grp.id, name=dst_groups[i], path=dst_groups[i])
                            gm[grp_path] = g
                        parent_grp = gm[grp_path]
                    if not parent_grp:
                        raise Exception()

                    # have parent group, now create project:
                    p = gl_connector.gl_get_project(full_path = dst_full_path)
                    if not p:
                        p = gl_connector.gl_create_project(parent=parent_grp.id, name=repo_info["#name"], path=dst_name)
                        logging.debug("Created on srv")
                    # print(p)

                    dst_path = os.path.join(srv.path, r_uid + ".git")
                    url = srv.cfg_obj.main_connector.url_root + "/" + dst_full_path
                    #print(dst_path)
                    # print(url)
                    helpers.cmd(["git", "clone", "--bare", url, dst_path], allow_nonzero=True)
                    logging.debug("cloned")

        # print(repo_info)

    #######################
    # sync
    if 1:   # sync
        ss.populate_servers()

        for name, srv1 in ss.servers.items():
            print("**", name)
            for rid, branches in srv1.repos2branches.items():
                #print(rid, branches)
                for srv2 in ss.servers.values():
                    if srv2 == srv1:
                        continue
                    if rid not in srv2.repos2branches:
                        if args.report_missing_rid:
                            print("missing repo-id", rid, "in", srv2.path)
                        continue

                    try:
                        repo1_path = os.path.join(srv1.path, rid + ".git")
                        repo2_path = os.path.join(srv2.path, rid + ".git")
                        repo1 = pygit2.Repository(repo1_path)
                        repo2 = pygit2.Repository(repo2_path)

                        for branch in srv2.repos2branches[rid]:
                            if branch not in srv1.repos2branches[rid]:
                                print("Missing branch", branch, "in", rid, srv1.path)
                                helpers.cmd(["git", "fetch", repo2_path, f"{branch}:{branch}"], work_dir=repo1_path, retries=2, dry_run=False)
                                helpers.cmd(["git", "push", "origin", f"{branch}:{branch}"], work_dir=repo1_path, retries=2, dry_run=False)
                                continue
                            #ref1 = repo1.references["refs/heads/" + branch]
                            ref2 = repo2.references["refs/heads/" + branch]
                            if not repo1.odb.exists(ref2.target):
                                # repo1 doesn't have commit from repo2.
                                helpers.cmd(["git", "fetch", repo2_path, f"{branch}:{branch}"], work_dir=repo1_path, retries=2, dry_run=False, raise_exception=False)
                                helpers.cmd(["git", "push", "origin", f"{branch}:{branch}"], work_dir=repo1_path, retries=2, dry_run=False)

                    finally:
                        repo1.free()
                        repo2.free()


    if args.push_all:
        for name, srv in ss.servers.items():
            print("TODO: push", name)


####################################################################################
def main_synccheck(args) -> None:
    # TODO: check tags!

    # TODO: check gitlab server for repos without uid?
    # TODO: check local dir that _config/uid matches directory name? Or alt-uid?
    ss = SyncSettings(args.control_file, args.groups)
    ss.populate_servers()

    for name, srv1 in ss.servers.items():
        print("**", name)
        for rid, branches in srv1.repos2branches.items():
            for srv2 in ss.servers.values():
                if srv2 == srv1:
                    continue
                if rid not in srv2.repos2branches:
                    if not args.ignore_missing_repos:
                        print("missing repo-id", rid, "in", srv2.path)
                    continue

                try:
                    repo1_path = os.path.join(srv1.path, rid + ".git")
                    repo2_path = os.path.join(srv2.path, rid + ".git")
                    repo1 = pygit2.Repository(repo1_path)
                    repo2 = pygit2.Repository(repo2_path)

                    for branch in srv2.repos2branches[rid]:
                        if branch not in srv1.repos2branches[rid]:
                            print("Missing branch", branch, "in", rid, srv1.path)
                            continue
                        ref2 = repo2.references["refs/heads/" + branch]
                        if not repo1.odb.exists(ref2.target):
                            print("branch", branch, "in", rid, srv1.path,"doesn't have commit", ref2.target)

                finally:
                    repo1.free()
                    repo2.free()


####################################################################################

def main_check_raw_git(args) -> None:
    result = {}
    for n in os.listdir(args.directory):
        fp = os.path.join(args.directory, n)

        try:
            repo = pygit2.Repository(os.path.join(fp))

            # print (n)
            if n.lower().endswith(".git"):
                uid = n[:-4]
            else:
                uid = n

            result[uid] = {}
            for b in repo.branches.local:
                if b[0]=="#":
                    continue
                commit_id = repo.references["refs/heads/"+b].target
                result[uid][b] = str(commit_id)
                #print ("  ",b, commit_id)
            repo.free()
        except:
            raise

    # TODO: send out as yaml
    print (yaml.dump(result))


####################################################################################

# uid hooks from git

def uid_get_cache(args) -> main_context.LocalContext:
    # get local path
    # if args.ws_path:
    #    ws = args.ws_path
    # else:
    #    ws = os.getcwd()
    # TODO: use ws?

    t1 = time.time()
    lc = main_context.LocalContext(args=args)
    lc.cache.update_map_uids_repos()
    t2 = time.time()
    logging.debug("get LocalContext took %.1f secs" % (t2 - t1))
    # print ("Reading cache took: %.3f secs" % (t2-t1), file=sys.stderr)

    return lc



def uid_get_relative_path(repo, rem_url: str) -> str:
    logging.debug("uid_get_relative_path: %s" % rem_url)
    for pre in ("ssh://", "http://", "https://"):
        if rem_url.startswith(pre):
            t = rem_url[len(pre):]          # skip ssh:// etc
            rem_url = t[t.index("/") + 1:]  # then skip dns part
            break
    else:
        if ":" in rem_url:
            rem_url = rem_url[rem_url.index(":") + 1:]
    s_rem = rem_url.split("/")
    s_srv = repo.server_full_path.split("/")
    while s_rem[0] == s_srv[0]:
        s_rem = s_rem[1:]
        s_srv = s_srv[1:]
    rem = "/".join(s_rem)
    srv = "/".join(s_srv)
    if not srv.endswith(".git"):
        srv += ".git"
    logging.debug("rem_url: %s => %s" % (rem_url, rem))
    logging.debug("repo.server_full_path: %s => %s" % (repo.server_full_path, srv))
    return "../" * (rem.count("/") + 1) + srv

def uid_lookup(lc, uid:str, rem_url:str) -> bool:
    if uid in lc.cache.map_all_uid_repos:
        repo = lc.cache.map_all_uid_repos[uid]
        # for pre in ("ssh://", "http://", "https://"):
            # if rem_url.startswith(pre):
                # rem_url = rem_url[len(pre):]

        # rel_path = "../"*(rem_url.count("/")) + repo.server_full_path

        # git wants to see this on stdout:
        print (uid_get_relative_path(repo, rem_url))
        print (uid)
        return True
    else:
        return False


def main_uidhook_sfrp(args) -> None:
    try:
        lc = uid_get_cache(args)
    except FileNotFoundError:
        return -2   # no cache file

    url = args.sub_relative_url.split("/")[-1]
    if url.endswith(".git"):
        url = url[:-4]
    if uid_lookup(lc, url, args.remoteurl):
        return 0 # OK!
    else:
        # print ("**failed to lookup", url, ws, file=sys.stderr)
        return -1 # couldn't find it!


def main_uidhook_sfru(args) -> None:
    try:
        lc = uid_get_cache(args)
    except FileNotFoundError:
        return -2   # no cache file

    if uid_lookup(lc, args.uid, args.remoteurl):
        return 0 # OK!
    else:
        return -1 # couldn't find it!

####

def main_uid_clean_gitmodules(args) -> None:
    mc = main_context.WSContext(args=args, skip_ws_scan=True)
    # mc.update()   # TODO: enable with option?

    rw = helpers.WorkspaceWrapper(".")
    rw.open()
    index = rw.repo.index
    index.read()
    subs = [idx_entry for idx_entry in index if (idx_entry.mode & pygit2.GIT_FILEMODE_TREE)]
    fn_gitmod = os.path.join(rw.ws_path, ".gitmodules")
    print (rw.repo_path)
    gitmod = open(fn_gitmod, "rt").read()
    gitmod = gitmod.replace("\t", "        ")
    cfg = configparser.RawConfigParser()
    cfg.optionxform = lambda option: option
    cfg.read_string(gitmod)
    sm_path_to_section = {}
    sm_path_to_section_name = {}
    for section in cfg:
        if section=="DEFAULT":
            continue
        if section.startswith("submodule \""):
            logging.debug("section: %s" % section)
            logging.debug("cfg[section]: %s" % cfg[section])
            sm = section.strip()[11:-1]
            logging.debug("sm: %s" % sm)
            logging.debug("items: %s" % str(list(cfg[section].items())))
            sm_path_to_section[cfg[section]["path"]] = { k:v for k,v in cfg[section].items() }
            sm_path_to_section_name[cfg[section]["path"]] = sm
        else:
            raise Exception("Bad section %s" % section)
    all_subm_found = set()
    for x in subs:
        all_subm_found.add(x.path)
        if x.path not in sm_path_to_section:
            logging.debug(str(x))
            logging.debug(str(sm_path_to_section))
            raise Exception(f"Submodule {repr(x.path)} doesn't exist in .gitmodules")

    new_gitmod = ""
    for path, defs in sm_path_to_section.items():
        if path in all_subm_found:
            repo = None
            if "uid" in defs:
                repo = mc.cache.map_all_uid_repos.get(defs["uid"],None)
            elif defs["url"].startswith("../") or defs["url"].startswith("..\\"):
                # logging.debug("submodule %s url=%s" % (path, defs["url"]))
                url_fix = defs["url"].replace("\\","/")
                if url_fix.endswith(".git"):
                    url_fix = url_fix[:-4]
                url = url_fix.split("/")[-1]
                if url in mc.cache.map_all_uid_repos:
                    repo = mc.cache.map_all_uid_repos[url]
                else:
                    root_repo_abspath = helpers.remove_protocol_host_from_url(rw.repo.config["remote.origin.url"])
                    apath = helpers.url_make_absolut(root_repo_abspath, url_fix)
                    logging.debug("try to find uid for '%s' root_path='%s' url_fix='%s' => '%s'" % (path, root_repo_abspath, url_fix, apath))

                    for r in mc.cache.total_cache.main_server.repos:
                        if r.server_full_path==apath or r.server_full_path==apath+".git":
                            repo = r
                            break
                    else:
                        logging.debug("=> couldn't find relative path. Just keep it")

            if repo:
                if repo.uid:
                   defs["uid"] = repo.uid

                remote_url = rw.repo.config["remote.origin.url"]
                if remote_url:
                    defs["url"] = uid_get_relative_path(repo, remote_url)

            new_gitmod += f"[submodule \"{sm_path_to_section_name[path]}\"]\n"
            for k,v in defs.items():
                new_gitmod += f"\t{k} = {v}\n"
        else:
            print ("Removing submodule path %s" % path)

    if new_gitmod:
        with open(fn_gitmod,"wt",newline="\n") as fh:
            fh.write(new_gitmod)
    else:
        print ("New .gitmodules is empty. TODO: just remove it")

    print ("Done updating .gitmodules")




####################################################################################

def main_submodule_init(args) -> int:
    lc = uid_get_cache(args)
    return lc.submodule_init(".", args.no_update, args.no_init, args.no_recursive)


####################################################################################
####################################################################################
####################################################################################

def add_common_args(parser):
    parser.add_argument("--cfg", type=str, help="the gcln config file in yaml format")



def main():
    time_start = time.time()

    parser = argparse.ArgumentParser(prog="gcln", description="Git Collections - tool to manage many repositories")
    parser.add_argument("--root", type=str, help="parent directory for all the workspaces.")
    #parser.add_argument("--cfg", type=str, help="the gcln config file in yaml format")
    parser.add_argument("--run_dir", type=str, help="if set, the working directory will be changed to this at startup")
    parser.add_argument("--version", action="version", version="%(prog)s " + __version__ + ", python=" + sys.version + ", exec: " + sys.argv[0])
    parser.add_argument("--log", choices=["DEBUG", "INFO", "WARNING"], type=str.upper, default="WARNING", help="logging level")
    parser.add_argument("--status", action="store_true", help="check status of all workspaces, ignore cache")
    parser.add_argument("--all", action="store_true", help="do a full update, ignore cache")
    parser.add_argument("--groups", action="store_true", help="read all groups from server, ignore cache")
    parser.add_argument("--verbose", action="store_true", help="more verbose output")
    add_common_args(parser)

    subparsers = parser.add_subparsers(help='sub-command help')

    p_interactive = subparsers.add_parser("interactive", aliases=["tui"], help="start text based interactive mode")
    p_interactive.set_defaults(func=main_interactive)

    #p_update_all = subparsers.add_parser("update_all", help="get all info from server, clone and update all repos locally")
    #p_update_all.set_defaults(func=main_update_all)

    p_update = subparsers.add_parser("update", help="optimized update")
    p_update.set_defaults(func=main_update)

    p_update = subparsers.add_parser("update_cache", help="just update the cache, do not clone/pull to workspace")
    p_update.set_defaults(func=main_update_cache)

    p_check = subparsers.add_parser("check", help="check workspace, currently mainly if there are duplicates/bad configs")
    p_check.set_defaults(func=main_check)

    p_status = subparsers.add_parser("status", help="workspace status")
    p_status.set_defaults(func=main_status)

    p_git_config = subparsers.add_parser("git_config", help="apply git config variables to all workspaces")
    p_git_config.set_defaults(func=main_git_config)

    p_conv_ssh_auth = subparsers.add_parser("conv_ssh_auth", help="read gitlab auth file, and generate a new one for the ssh proxy. TODO: remove!")
    p_conv_ssh_auth.add_argument("--output", help="dst, should be copied to ~git/.ssh/authorized_keys")
    p_conv_ssh_auth.add_argument("--cmd", help="gcln command to use inside the auth file, default is to use the one that is running. Run gcln with ~/... if not in path")
    p_conv_ssh_auth.add_argument("--root", help="root argument in generated file. Typicall ~/<cfgdir>")
    p_conv_ssh_auth.add_argument("input", help="gitlab auth file, normally /srv/gitlab/data/.ssh/authorized_keys")
    p_conv_ssh_auth.set_defaults(func=main_conv_ssh_auth)

    p_ssh_proxy = subparsers.add_parser("ssh_proxy", help="ssh proxy to redirect git requests into gitlab")
    p_ssh_proxy.add_argument("args", type=str, nargs="*", help="normally the key")
    p_ssh_proxy.set_defaults(func=main_ssh_proxy)

    p_set_aux_remote = subparsers.add_parser("set_aux_remote", help="set remote for the aux servers")
    p_set_aux_remote.set_defaults(func=main_set_aux_remote)

    p_dbg = subparsers.add_parser("dbg", help="debugging/testing")
    p_dbg.add_argument("cmd", type=str, help="what to test")
    p_dbg.set_defaults(func=main_dbg)

    p_cfg = subparsers.add_parser("cfg", help="check/modify repos _config settings")
    p_cfg.add_argument("--repo", default=".", help="path to the repository/workspace")
    #p_cfg.add_argument("--local", action="store_true", help="don't care about origin branch")
    p_cfg.add_argument("--show", action="store_true", help="show current cfg variables")
    p_cfg.add_argument("--set_id_name", type=str, help="set the id_name of the repo")
    p_cfg.add_argument("--set_rnd_uid", action="store_true", help="create a new (random) uid, and set it")
    p_cfg.add_argument("--set_uid", type=str, help="set a new named uid")
    p_cfg.add_argument("--add_alt_uid", type=str, help="add an alternative uid")
    p_cfg.add_argument("--del_alt_uid", type=str, help="delete/remove an alternative uid")
    p_cfg.add_argument("--force", action="store_true", help="overwrite")
    p_cfg.add_argument("--nofetch", action="store_true", help="do not fetch the latest version from server before modifying")
    p_cfg.add_argument("--nopush", action="store_true", help="do not push changes to config branch")
    p_cfg.set_defaults(func=main_cfg)

    p_pull_bare = subparsers.add_parser("pull_bare", help="pull from a server to a directory with bare repositories")
    p_pull_bare.add_argument("directory", type=str, help="directory containing the bare repos")
    p_pull_bare.add_argument("--repo_list", type=str, help="yaml file which list remote repos, this overrides the normal cfg file")
    p_pull_bare.add_argument("--no_clone", action="store_true", help="do not clone from server, only fetch existing repos")
    p_pull_bare.set_defaults(func=main_pull_bare)

    p_push_bare = subparsers.add_parser("push_bare", help="push to a server from a directory with bare repositories")
    p_push_bare.add_argument("directory", type=str, help="directory containing the bare repos")
    p_push_bare.add_argument("--repo_list", type=str, help="yaml file which list remote repos, this overrides the normal cfg file")
    p_push_bare.set_defaults(func=main_push_bare)

    p_sync = subparsers.add_parser("sync", help="push to a server from a directory with bare repositories")
    p_sync.add_argument("control_file", type=str, help="control file for syncing")
    p_sync.add_argument("--server", type=str, help="if defined, only work with this server. Otherwise, run with all")
    p_sync.add_argument("--push", action="store_true", help="push changed repo to server(s)")
    p_sync.add_argument("--push_all", action="store_true", help="explicit run to push all repos")
    p_sync.add_argument("--pull", action="store_true", help="pull from all or selected server")
    p_sync.add_argument("--no_sync", action="store_true", help="do not sync the local repositories")
    p_sync.add_argument("--report_missing_rid", action="store_true", help="report missing repo-ids on a server")
    p_sync.set_defaults(func=main_sync)

    p_synccheck = subparsers.add_parser("sync_check", help="check the local sync data if there are differences")
    p_synccheck.add_argument("control_file", type=str, help="control file for syncing")
    p_synccheck.add_argument("--ignore_missing_repos", action="store_true", help="do not report missing repositories")
    p_synccheck.set_defaults(func=main_synccheck)

    p_check_raw_git = subparsers.add_parser("check_raw_git", help="check a directory of raw git repos, return branches/repo with latest commit ID")
    p_check_raw_git.add_argument("directory", type=str, help="directory containing the git repos")
    p_check_raw_git.set_defaults(func=main_check_raw_git)

    p_uidhook = subparsers.add_parser("uidhook", help="git hook for uid lookup")
    sub2p = p_uidhook.add_subparsers(help="sub2-command help")

    p_uidhook_sfrp = sub2p.add_parser("resolve_subm_from_relative_path", help="get proper submodule url from relative url")
    p_uidhook_sfrp.add_argument("remoteurl", type=str, help="")
    p_uidhook_sfrp.add_argument("sub_relative_url", type=str, help="")
    p_uidhook_sfrp.add_argument("ws_path", type=str, help="")
    p_uidhook_sfrp.add_argument("up_path", type=str, help="")
    p_uidhook_sfrp.set_defaults(func=main_uidhook_sfrp)

    p_uidhook_sfru = sub2p.add_parser("resolve_subm_from_uid", help="get proper submodule url from relative uid")
    p_uidhook_sfru.add_argument("remoteurl", type=str, help="")
    p_uidhook_sfru.add_argument("sub_relative_url", type=str, help="")
    p_uidhook_sfru.add_argument("ws_path", type=str, help="")
    p_uidhook_sfru.add_argument("up_path", type=str, help="")
    p_uidhook_sfru.add_argument("uid", type=str, help="")
    p_uidhook_sfru.set_defaults(func=main_uidhook_sfru)

    p_uid_clean_gitmodules = subparsers.add_parser("clean_gitmodules", help="rewrite .gitmodules with uid lookup etc")
    p_uid_clean_gitmodules.set_defaults(func=main_uid_clean_gitmodules)

    p_submodule_init = subparsers.add_parser("submodule_init", help="git submodule init --recursive with uid lookup")
    p_submodule_init.add_argument("--no_recursive", action="store_true", help="do not add --recursive to submodule update")
    p_submodule_init.add_argument("--no_init", action="store_true", help="do not add --init to submodule update")
    p_submodule_init.add_argument("--no_update", action="store_true", help="skip git submodule update after init submodule paths")
    p_submodule_init.set_defaults(func=main_submodule_init)

    p_test1 = subparsers.add_parser("test1", help="test - undefined")
    add_common_args(p_test1)
    # p_test1.add_argument("srv")
    p_test1.set_defaults(func=main_test1)

    p_test2 = subparsers.add_parser("test2", help="test - undefined")
    p_test2.set_defaults(func=main_test2)

    args = parser.parse_args()

    num_lvl = getattr(logging, args.log)
    logging.basicConfig(level=num_lvl)
    logging.debug("Started")

    try:
        old_dir = os.getcwd()
        if args.run_dir:
            logging.debug(f"Change current dir from {old_dir} to {args.run_dir}")
            os.chdir(args.run_dir)

        if "func" in args:
            try:
                ret = args.func(args)
            except UserError as err:
                print(err)
                if args.verbose:
                    raise
                else:
                    sys.exit(-100)

            t = time.time() - time_start
            logging.debug(f"Execution took {t:.2f} seconds")
            if isinstance(ret, int):
                sys.exit(ret)
        else:
            print("-h to get help")
            # main_interactive(args)
    finally:
        os.chdir(old_dir)



if __name__ == '__main__':
    main()
