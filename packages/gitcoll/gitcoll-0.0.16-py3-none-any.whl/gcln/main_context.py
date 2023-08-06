from __future__ import annotations

import os
import sys
import time
import pickle
import logging
import subprocess
import collections
import configparser

from typing import Optional

import yaml
import pygit2
import filelock

from gcln import cfg_file
from gcln import records
from gcln import srv_connector
from gcln.exceptions import UserError
from gcln import helpers







class LocalInfo:
    def __init__(self, ws_root: str, co_cache:list[records.GitCheckout], skip_ws_scan=False):  # , check_status=True, cb_chk_status=None):
        self.ws_root: str = ws_root
        self.co_cache: list[records.GitCheckout] = co_cache     # note that this points to the same object as total_cache.checkouts normally.

        if not skip_ws_scan:
            self.scan_local_fs()

    def scan_local_fs(self) -> None:
        t0 = time.time()
        logging.debug("scanning local filesystem for workspaces")

        old_cache_commits = { co.path:co for co in self.co_cache }
        self.co_cache[:] = []

        def get_rel_path(root:str, full:str) -> str:
            ret = full[len(root):].replace("\\","/")
            # depending whether there is a slash end of self.ws_root or not, we might need to remove excessive slash(es):
            while ret[0]=="/":
                ret = ret[1:]
            return ret

        for p, d, f in os.walk(self.ws_root):
            if ".git" in f:
                raise Exception(f"orphan submodule in {p}")
            if not ".git" in d:
                continue

            # found a checkout
            # print(p)
            d[:]=[] # don't recurse further down

            main_co = records.GitCheckout()
            main_co.path = get_rel_path(self.ws_root, p) #p[len(self.ws_root):].replace("\\", "/")
            if main_co.path in old_cache_commits:
                main_co.head = old_cache_commits[main_co.path].head
                main_co.branch = old_cache_commits[main_co.path].branch

            self.co_cache.append(main_co)

            def handle_submodule(sub_path, lvl=1) -> records.GitCheckout:
                # print ("Submodule",sub_path, lvl)
                sub_co = records.GitCheckout(level=lvl)
                sub_co.path = get_rel_path(self.ws_root, sub_path)

                if sub_co.path in old_cache_commits:
                    sub_co.head = old_cache_commits[sub_co.path].head
                    sub_co.branch = old_cache_commits[sub_co.path].branch

                for sub_p, d, f in os.walk(sub_path):
                    if sub_p == sub_path:
                        continue
                    if ".git" in f:
                        d[:] = [] # no need to recurse more
                        sub_co.submodules.append(handle_submodule(sub_p, lvl+1))

                return sub_co

            for sub_p, d, f in os.walk(p):
                if ".git" in d:
                    # optimize a little, no need to recurse into .git directory
                    d.remove(".git")
                elif ".git" in f:
                    d[:] = [] # no need to recurse more
                    main_co.submodules.append(handle_submodule(sub_p))

        t = time.time()-t0
        logging.debug(f"scanning took {t:.2f} seconds")
        return t


    def check_status_one(self, co:records.GitCheckout) -> None:
        logging.debug(f"status in {self.ws_root}:{co.path}")

        try:
            # print (self.ws_root)
            # print (co.path)
            repo = pygit2.Repository(os.path.join(self.ws_root,co.path))
        except OSError as err:
            co.status = [f"OSError {err} when open {co.path}"]
            logging.error(f"OSError couldn't open repo via pygit2.Repository: '{co.path}' ({err})")
            return
        except:
            err = sys.exc_info()[1]
            co.status = [f"General error {err} when open {co.path}"]
            logging.error(f"General error, couldn't open repo via pygit2.Repository: '{co.path}' ({err})")
            return

        try:
            try:
                logging.debug(f"status repo {co.path}")
                if 0:
                    # TODO: config parameter if we should get status. It takes a lot of time, so good to avoid it normally.
                    co.status = repo.status()
                logging.debug(f"Done repo {co.path}")
            except OSError as err:
                logging.error(f"Couldn't get repo status: '{co.path}' ({err})")
                return

            if repo.head_is_unborn:
                logging.warning(f"no head for {co.path}")
                co.head = ""
                co.status_no_head = True
                return

            try:
                co_branch = repo.head.name.split("/")[-1]
                if co_branch in repo.branches.local:
                    # print ("local branch", co_branch)
                    co.branch = co_branch
            except pygit2.GitError:
                print ("probably no remote in:", co.path)
                print (repo)
            except:
                print ("probably no remote in", co.path)
                raise

            try:
                co.head = str(repo.head.target).upper()
                if not co.head:
                    raise Exception()
            except:
                logging.warning(f"no head for {co.path}")
                co.head = ""
                co.status_no_head = True
        finally:
            repo.free() # important to free resource


    def check_status(self) -> float:    # returns how long time it took
        t0 = time.time()
        for co in self:
            self.check_status_one(co)

        t = time.time()-t0
        logging.debug(f"status took {t:.2f} seconds")
        return t


    def __iter__(self, recursive:bool=True):
        for co in self.co_cache:
            yield co
            if recursive:
                yield from co


#############################


class WSCollectionCache:
    """handler for the cache on the client, ie the workspace collection"""
    def __init__(self, cache_fn:str) -> None:
        logging.debug("WSCollectionCache")
        self.cache_fn = cache_fn
        self.total_cache: records.TotalCache
        self.map_uid_repos: dict[str, records.RepoInfo]         # mapping only for uid => repo
        self.map_all_uid_repos: dict[str, records.RepoInfo]     # mapping which includes both uid and alt_uids
        self.lock_handle = filelock.FileLock(self.lock_fn, timeout=1)

        try:
            self.lock_handle.acquire()
            logging.info("Acquired cache lock")
        except filelock.Timeout:
            raise UserError(f"cannot acquire lock file {self.lock_fn}. If you are sure there is no other gcln process running, delete the file and retry")

        if os.path.exists(self.cache_fn ):
            logging.debug(f"Read cache {self.cache_fn}")
            self.read_cache()
        else:
            logging.debug(f"no cache {self.cache_fn}")
            self.total_cache = records.TotalCache()
            self.write_cache()

    def update_map_uids_repos(self):
        self.map_uid_repos = {proj.uid:proj for proj in self.total_cache.main_server.repos if proj.uid}
        self.map_all_uid_repos = {}
        for repo in self.map_uid_repos.values():
            if repo.uid:
                self.map_all_uid_repos[repo.uid] = repo
            for alt_uid in repo.alt_uids:
                if alt_uid and alt_uid not in self.map_uid_repos:
                    self.map_all_uid_repos[alt_uid] = repo

    def clear(self) -> None:
        self.total_cache = records.TotalCache()

    def update_from_servers(self, main_connector: srv_connector.ConnectorBase, aux_connectors: srv_connector.ConnectorBase, update_all = False, update_groups=False) -> float:
        """returns how long time it took"""
        t0 = time.time()
        logging.debug("Updating cache from server(s)")

        if update_all:
            update_groups=True

        self.map_uid_repos = main_connector.update_cache(self.total_cache.main_server, update_groups)
        self.map_all_uid_repos = {}
        for repo in self.map_uid_repos.values():
            self.map_all_uid_repos[repo.uid] = repo
            for alt_uid in repo.alt_uids:
                self.map_all_uid_repos[alt_uid] = repo

        if aux_connectors:
            raise Exception("TODO")

        t = time.time()-t0
        logging.debug(f"Updating cache took {t:.2f} seconds")

        self.write_cache()

        return t

    @property
    def pickle_fn(self):
        return self.cache_fn.replace(".yaml","")+".pickle"

    @property
    def lock_fn(self):
        return self.cache_fn.replace(".yaml","")+".lock"

    def read_cache(self) -> None:
        try:
            st1 = os.stat(self.cache_fn)
            st2 = os.stat(self.pickle_fn)
            # print (st2.st_mtime - st1.st_mtime)
            if st2.st_mtime >= st1.st_mtime:
                self.total_cache = pickle.load(open(self.pickle_fn,"rb"))
                return
        except:
            pass
        cache_dict = yaml.safe_load(open(self.cache_fn, "rt").read())
        if not isinstance(cache_dict, dict):
            raise Exception(f"Corrupt cache file {self.cache_fn}, please remove it")

        self.total_cache = records.TotalCache.from_dict(cache_dict)
        pickle.dump(self.total_cache, open(self.pickle_fn,"wb"))

    def write_cache(self) -> None:
        if not self.lock_handle.is_locked:

            try:
                self.lock_handle.acquire()
                logging.info("Acquired cache lock")
            except filelock.Timeout:
                raise UserError(f"cannot acquire lock file {self.lock_fn}. If you are sure there is no other gcln process running, delete the file and retry")

#            logging.warning("Cannot write cache as we do not have the lock")
#            return
        with open(os.path.join(self.cache_fn), "wt") as fh:
            fh.write(yaml.safe_dump(self.total_cache.as_dict()))
        pickle.dump(self.total_cache, open(self.pickle_fn,"wb"))


    def write_and_release_lock(self) -> None:
        self.write_cache()
        if self.lock_handle.is_locked:
            self.lock_handle.release()



#############################

class LocalContext:
    def __init__(self, args, srv_name=""):
        logging.debug("LocalContext")
        if srv_name:
            srv_name += "."
        self.cfg = cfg_file.Config(args=args)
        self.cache = WSCollectionCache(os.path.join(self.cfg.ws_root, f".{srv_name}cache.yaml"))


    def submodule_init(self: LocalContext, ws_path: str, no_update: bool, no_init: bool, no_recursive: bool) -> int:
        logging.debug("submodule_init in %s" % ws_path)

        rw = helpers.WorkspaceWrapper(ws_path)
        rw.open()
        index = rw.repo.index
        index.read()
        fn_gitmod = os.path.join(rw.ws_path, ".gitmodules")
        if not os.path.exists(fn_gitmod):
            logging.debug("Skip, no %s" % fn_gitmod)
            return 0
        gitmod = open(fn_gitmod, "rt").read()
        gitmod = gitmod.replace("\t", "        ")
        cfg = configparser.RawConfigParser()
        cfg.optionxform = lambda option: option
        cfg.read_string(gitmod)

        my_remote_url = rw.repo.config["remote.origin.url"]
        if not my_remote_url:
            print("Error, do now have my own remote url")
            return -1

        sub_paths = []
        for section in cfg:
            if section=="DEFAULT":
                continue
            if section.startswith("submodule \""):
                section_name = section[11:-1]
                logging.debug("section: %s (%s), items:%s" % (section, section_name, str(list(cfg[section].items()))))
                sub_paths.append(cfg[section]["path"])
                uid = ""
                if "uid" in cfg[section]:
                    uid = cfg[section]["uid"]
                elif cfg[section]["url"].startswith("../"):
                    uid = cfg[section]["url"].split("/")[-1]
                    if uid.endswith(".git"):
                        uid = uid[:-4]
                if not uid:
                    logging.debug("not relative nor uid for %s" % section)
                    continue

                if not uid in self.cache.map_all_uid_repos:
                    logging.debug("couldn't find uid %s in cache" % uid)
                    continue

                repo = self.cache.map_all_uid_repos[uid]
                key = f"submodule.{section_name}.url"
                val = helpers.uid_get_url_from_abs_path(repo.server_full_path, my_remote_url)
                if not val:
                    logging.debug("couldn't calc value for uid=%s key=%s" % (uid, key))
                    continue

                rw.repo.config[key] = val
                logging.debug("set config %s = %s" % (key, val))
            else:
                raise Exception("Bad section %s" % section)

        if no_update:
            return 0

        arg_list = ["git", "submodule", "update"]
        if not no_init:
            arg_list.append("--init")

        print(" ".join(arg_list), "@", rw.ws_path)
        helpers.cmd(arg_list, work_dir=rw.ws_path)

        if not no_recursive:
            for p in sub_paths:
                ap = os.path.join(rw.ws_path, p)
                if not os.path.exists(ap):
                    continue
                self.submodule_init(ap, no_update, no_init, no_recursive)

        return 0



#############################


class WSContext(LocalContext):
    """connects config, main server, aux servers, repos, workspaces etc. Not used on the server end!"""
    def __init__(self, args: object, srv_name="", skip_ws_scan=False, main_branches: optional[list[str]]=None) -> None:
        # which branches are considered main, and in what order:
        if main_branches:
            self.main_branches:list[str] = main_branches
        else:
            self.main_branches = ["main", "master"]
        self.main_branches_set = set(self.main_branches)
        logging.debug("WSContext")
        super().__init__(args, srv_name)
        self.main_connector: Optional[srv_connector.ConnectorBase] = None
        self.aux_connectors: list[srv_connector.ConnectorBase] = []

        if args.all:
            self.cache.clear()
            args.groups = True

        self.local_info = LocalInfo(self.cfg.ws_root, self.cache.total_cache.checkouts, skip_ws_scan=skip_ws_scan)  # TODO args

        # TODO: probably separate member function for this!
        if args.status or args.all:
            self.local_info.check_status()

        if "main_server" in self.cfg.data:
            self.main_connector = srv_connector.ConnectorBase.create("main_server", self.cfg.data["main_server"])

        self.cache.update_from_servers(self.main_connector, self.aux_connectors, update_all=args.all, update_groups=args.groups)

        # TODO: can check if the ws has correct branch also


    def check_if_local_bare_repo_diffs(self, repos: dict[str, tuple[str, set[str]]], ignorer: Optional[object]) -> list:
        # arg is dict, key=disk-path, value=[str repo uid, set of branches]
        ret = collections.defaultdict(set)  # key=repo_uid, value=set(branches)
        for repo_path, (uid, branches) in repos.items():
            srv_repo = self.cache.map_all_uid_repos[uid]
            srv_branches = {b.name: b for b in srv_repo.branches}
            if not os.path.exists(repo_path):
                ret[uid] = set(srv_branches.keys())    # doesn't exist locally, then checkout all
                continue
            repo = pygit2.Repository(repo_path)
            for branch in srv_branches.keys():
                if ignorer and ignorer.is_branch_ignored(uid, branch):
                    continue
                try:
                    ref = str(repo.references["refs/heads/" + branch].target).upper()
                except KeyError:
                    # server branch does not exist locally. Then add it.
                    ret[uid].add(branch)
                    continue
                if branch in branches:
                    if ref != srv_branches[branch].commit_id.upper():
                        ret[uid].add(branch)
                else:
                    ret[uid].add(branch)

            repo.free()
        return ret



    def _calc_co_paths_etc(self) -> tuple(dict,dict,dict):
        co_paths_from_fs: tuple[str, "checkout"] = {co.path: co for co in self.cache.total_cache.checkouts if co.path}

        for co in co_paths_from_fs.values():
            if not co.head:
                self.local_info.check_status_one(co)

        calced_co_paths = {}

        srv_id_to_repos = {r.srv_id: r for r in self.cache.total_cache.main_server.repos}

        bad_paths: dict[str,set(str)] = collections.defaultdict(set)   # if projects are shared with groups, there is a risk of duplicate paths.

        def repo_handle_branches(repo:pygit2.Repository, grp_full_name:str) -> None:
            if repo.branches:
                main_branches = {b.name for b in repo.branches} & self.main_branches_set
                if not main_branches:
                    logging.error (f"no main branch in {repo.server_name} in {grp_full_name}")
                    main_branch = ""
                else:
                    # at least one main branch. Pick the first/priority one:
                    for mb in self.main_branches:
                        if mb in main_branches:
                            main_branch = mb
                            break
                    if len(main_branches) > 1:
                        logging.error (f"several main branches in {repo.server_name} in {grp_full_name}: {main_branches}. Using the first/priority one. Total branches are {[b.name for b in repo.branches]}")
                        raise Exception("Maybe just remove this?")
                for branch in repo.branches:
                    # TODO: more general ignore rule
                    if branch.name in "_config" or branch.name[0] == "#":
                        continue
                    if branch.name == main_branch:
                        repo_name = repo.server_name
                    else:
                        repo_name = "_branches/" + repo.server_name + "-" + branch.name
                    wsp = helpers.name_to_ws_path(grp_full_name + "/" + repo_name)
                    if wsp in calced_co_paths:
                        # will be removed later on
                        r2 = calced_co_paths[wsp][0]
                        bad_paths[wsp].add(f"{r2.server_full_path}")
                        bad_paths[wsp].add(f"{repo.server_full_path}")
                    calced_co_paths[wsp] = (repo, records.GitCheckout(path=wsp, branch=branch.name, head=branch.commit_id))
            else:
                # empty project, create master branch
                repo_name = repo.server_name
                wsp = helpers.name_to_ws_path(grp_full_name + "/" + repo_name)
                if wsp in calced_co_paths:
                    # will be removed later on
                    r2 = calced_co_paths[wsp][0]
                    bad_paths[wsp].add(f"{r2.server_full_path}")
                    bad_paths[wsp].add(f"{repo.server_full_path}")
                calced_co_paths[wsp] = (repo, records.GitCheckout(path=wsp, branch=""))
        # end def repo_handle_branches()

        # handle user repos
        for repo in self.cache.total_cache.main_server.repos:
            if repo.owner_kind != "group":  # ie, user
                if repo.owner_kind != "user":
                    raise Exception("Unkown owner to repo")
                # print(repo)
                grp_full_name = self.cfg.ws_home_prefix + repo.server_full_path.split("/")[0]
                if self.cfg.ws_sub_tree:
                    if not grp_full_name.startswith(self.cfg.ws_sub_tree):
                        continue  # doesn't belong to sub-tree, skip it
                    grp_full_name = grp_full_name[len(self.cfg.ws_sub_tree) + 1:]
                repo_handle_branches(repo, grp_full_name)

        # handle all repos belonging to a group:
        for grp in self.cache.total_cache.main_server.groups:
            grp_full_name = helpers.name_to_ws_path(grp.full_name)
            if self.cfg.ws_sub_tree:
                if not grp_full_name.startswith(self.cfg.ws_sub_tree):
                    logging.debug(f"skip grp {grp_full_name} as it doesn't start with {self.cfg.ws_sub_tree}")
                    continue  # doesn't belong to sub-tree, skip it
                grp_full_name = grp_full_name[len(self.cfg.ws_sub_tree) + 1:]
            if grp_full_name:
                grp_full_name += "/"

            logging.debug(f"grp {grp.full_name}  --  {grp_full_name}")
            for uid, repo_srvid in grp.project_uids:
                if not uid:
                    repo = srv_id_to_repos[repo_srvid]
                elif uid not in self.cache.map_uid_repos:
                    logging.error("Unknown uid %s. Skipping it" % uid)
                    continue
                else:
                    repo = self.cache.map_uid_repos[uid]
                if repo.branches:
                    main_branches = {b.name for b in repo.branches} & self.main_branches_set
                    if not main_branches:
                        logging.error (f"no main branch in {repo.server_name} in {grp.full_name}")
                        main_branch = ""
                    else:
                        # at least one main branch. Pick the first/priority one:
                        for mb in self.main_branches:
                            if mb in main_branches:
                                main_branch = mb
                                break
                        if len(main_branches) > 1:
                            logging.error (f"several main branches in {repo.server_name} in {grp.full_name}: {main_branches}. Using the first/priority one. Total branches are {[b.name for b in repo.branches]}")
                            raise Exception()
                    for branch in repo.branches:
                        # TODO: more general ignore rule
                        if branch.name in "_config" or branch.name[0] == "#":
                            continue
                        if branch.name == main_branch:
                            repo_name = repo.server_name
                        elif self.cfg.ws_branches:
                            repo_name = "_branches/" + repo.server_name + "-" + branch.name
                        else:
                            # ignore this branch, as cfg variable doesn't want branches.
                            continue
                        wsp = helpers.name_to_ws_path(grp_full_name + repo_name)
                        if wsp in calced_co_paths:
                            # will be removed later on
                            r2 = calced_co_paths[wsp][0]
                            bad_paths[wsp].add(f"{r2.server_full_path}")
                            bad_paths[wsp].add(f"{repo.server_full_path}")
                        calced_co_paths[wsp] = (repo, records.GitCheckout(path=wsp, branch=branch.name, head=branch.commit_id))
                else:
                    # empty project, create master branch
                    repo_name = repo.server_name
                    wsp = helpers.name_to_ws_path(grp_full_name + repo_name)
                    if wsp in calced_co_paths:
                        # will be removed later on
                        r2 = calced_co_paths[wsp][0]
                        bad_paths[wsp].add(f"{r2.server_full_path}")
                        bad_paths[wsp].add(f"{repo.server_full_path}")
                    calced_co_paths[wsp] = (repo, records.GitCheckout(path=wsp, branch=""))
        if bad_paths:
            logging.error("Due to share projects with groups, the following paths are in conflict and ignored:")
            for bp,repo_strs in bad_paths.items():
                logging.error(f"* {bp} : {repo_strs}")
                del calced_co_paths[bp]

        self.cache.write_cache()

        print("srv has %d workspaces" % len(calced_co_paths))
        print("disk has %d workspaces" % len(co_paths_from_fs))
        print ("on srv, but not on disk", set(calced_co_paths.keys()) - set(co_paths_from_fs.keys()))
        paths_to_print = list(sorted(set(co_paths_from_fs.keys()) - set(calced_co_paths.keys())))
        print ("on disk, but not in server:") # , set(co_paths_from_fs.keys()) - set(calced_co_paths.keys()))
        for p in paths_to_print:
            print ("  ",p)

        return (co_paths_from_fs, calced_co_paths, bad_paths)


    def status(self):
        """report status for all workspaces"""
        print ("Status...")

        self.local_info.check_status()
        for gc in self.local_info.co_cache:
            stats = { k:v for k,v in gc.status.items() if v!=pygit2.GIT_STATUS_IGNORED }
            if stats:
                print (f"{gc.path}:")
                for n,stat in stats.items():
                    print (f"  {n}:{stat}")

        print ("---")
        co_paths_from_fs, calced_co_paths, bad_paths = self._calc_co_paths_etc()
        # TODO!


    def update(self):
        """git update/clone for the workspace"""
        print("Updating")

        if len(self.cache.total_cache.main_server.groups) == 0:
            print("No groups in cache. Explicitly check this from server")
            self.cache.update_from_servers(self.main_connector, self.aux_connectors, update_all=False, update_groups=True)


        co_paths_from_fs, calced_co_paths, __bad_paths = self._calc_co_paths_etc()

        paths_to_handle = set()

        for repo, co in calced_co_paths.values():
            logging.debug(f"check {co.path}")
            # moved to when we calculate paths
            # if self.cfg.ws_sub_tree and not co.path.startswith(self.cfg.sub_tree):
                #logging.debug(f"Ignoring co {repo.uid}: {co.path}, as it doesn't start with {self.cfg.sub_tree}")
                # continue
            if not self.cfg.ws_rules.include_repo(repo):
                logging.debug(f"Ignoring repo {repo.uid}: {co.path}")
                continue
            if not self.cfg.ws_rules.include_ws(repo,co):
                logging.debug(f"Ignoring workspace {repo.uid}: {co.path}")
                continue

            if co.path in co_paths_from_fs:
                if co.head != co_paths_from_fs[co.path].head:
                    logging.debug(f"head {co.head} != {co_paths_from_fs[co.path].head} for {str(co)}")
                    #print (co.head, "::",co_paths_from_fs[co.path].head,"::",co.path)
                    paths_to_handle.add(co.path)
                else:
                    # match!
                    pass
            else:
                paths_to_handle.add(co.path)

        self.cache.write_and_release_lock()     # important to release lock, as submodule update will call gcln again. However, with new update, this is not important any-more - but still good to save cache.

        for wsp in paths_to_handle:
            repo, calced = calced_co_paths[wsp]
            logging.debug(f"path calcs:\n  self.cfg.ws_root='{self.cfg.ws_root}'\n  wsp='{wsp}'")
            abs_wsp = os.path.abspath(os.path.join(self.cfg.ws_root, wsp))
            logging.debug(abs_wsp)
            if wsp in co_paths_from_fs:
                print("* Update", abs_wsp)
                filesys = co_paths_from_fs[wsp]     # note that co_paths_from_fw objects point into cache.
                if not filesys.branch:
                    self.local_info.check_status_one(filesys)

                if calced.branch == filesys.branch:
                    try:
                        helpers.cmd(["git", "pull"], work_dir=abs_wsp, retries=2)
                        #helpers.cmd(["git", "submodule", "update", "--init", "--recursive"], work_dir=abs_wsp, retries=2)
                        self.submodule_init(abs_wsp, False, False, False)
                    except:
                        logging.error(f"Failed pull/submodule update of repo {co.path}.")
                        # raise
                    # as we updated the local checkout, make sure the cache is updated with latest info
                    self.local_info.check_status_one(filesys)
                else:
                    print(f"  => different branches {calced.branch}!={filesys.branch}, ignoring")
            else:
                path, ws_path = os.path.split(abs_wsp)
                url = self.main_connector.url_root + "/" + repo.server_full_path + ".git"

                print (f"* clone {url} into {abs_wsp}")

                os.makedirs(path,exist_ok=True)
                try:
                    if calced.branch:
                        helpers.cmd(["git", "clone", "-b", calced.branch, url, ws_path], work_dir=path, retries=4)
                    else:
                        helpers.cmd(["git", "clone", url, ws_path], work_dir=path, retries=4)
                    #helpers.cmd(["git", "submodule", "update", "--init", "--recursive"], work_dir=abs_wsp, retries=4)
                    self.submodule_init(abs_wsp, False, False, False)
                    # set local config in the newly updated workspace
                    for key, val in self.cfg.ws_gitconfig.items():
                        helpers.cmd(["git", "config", key, val], work_dir=os.path.join(path, ws_path))
                    #TODO: create a new Checkout object into cache.
                    #self.local_info.check_status_one(filesys)
                except:
                    logging.error(f"Failed clone/submodule update of repo {ws_path}.")
                    # raise

