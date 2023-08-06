# gcln2 - simplified gitlab only connector.

# py38 support:
from __future__ import annotations

#std packages
import os
import re
import sys
import time
import shutil
import typing
import logging
import secrets
import argparse
import dataclasses
import configparser
import concurrent.futures

#non-std packages (requirement.txt)
import yaml
import gitlab   # pip3 install python-gitlab
import pygit2   # pip3 install pygit2

#local modules
try:
    from gcln2 import db
    from gcln2 import schema
    from gcln2 import helpers
    from gcln2 import exceptions
    from gcln2 import yaml_loader
    from . import __version__
except:
    import db
    import schema
    import helpers
    import exceptions
    import yaml_loader
    from __init__ import __version__


if os.name == "nt":
    import win32file



############

@dataclasses.dataclass
class MainConfig:
    cfg_fn: str = "gcln2.yaml"
    root: str = "."
    cfg: schema.MainConfig = dataclasses.field(default=schema.MainConfig)

    def search_root(self, args: argparse.Namespace):
        self.root = os.path.abspath(args.root)
        old = self.root
        while 1:
            fn =  os.path.join(self.root, self.cfg_fn)
            if os.path.isfile(fn):
                break
            old = self.root
            self.root = os.path.abspath(os.path.join(self.root, ".."))
            if old == self.root:
                raise Exception("Couldn't find git collection root")

        # found root.

        cfg_tmp = yaml.load(open(fn, "rt"), Loader=yaml_loader.IncludeLoader)
        self.cfg = schema.MainConfig(**cfg_tmp)


############

class ServerConnector:
    def __init__(self, args, mc: MainConfig):
        self.gl: gitlab.Gitlab = gitlab.Gitlab(mc.cfg.general.server.api_url, private_token=mc.cfg.general.server.api_key)


#################

class UpdateContext:
    """Class that collects data needed for the various functions that update information from the server"""
    def __init__(self, args, sc: "ServerConnector" = None, cache: db.Cache= None):
        self.mc = MainConfig()
        self.mc.search_root(args)

        if sc:
            self.sc = sc
        else:
            self.sc = ServerConnector(args, self.mc)

        cache: db.Cache
        if cache:
            self.cache = cache
        else:
            self.cache = db.Cache()

        # TODO: add parameter for this offset
        self.start_timestamp = time.time() - 30 *60     # when we started. Used when save cache. As gitlab caches the statitics, we add 30 minutes margin.

        if not args.all:
            self.load_cache()

        self.map_uid2project = {}   # maps to project inside the cache structure after cache is updated
        self.args = args
        self.ws_paths = {}  # key is ws path, value is (project, branch:str). This is from server info.
        #self.root_path = os.getcwd()
        self.workspaces:dict[str, tuple[str, str]] = {}     # keys are paths (forward slashed). value is (branch, commit). This is from workspace scanning

        #self.re_valid_tags = re.compile(self.mc.cfg.rules.valid_tags)
        self.re_valid_branches = re.compile(self.mc.cfg.rules.valid_branches)
        self.re_blacklist_branches = [re.compile(s) for s in self.mc.cfg.rules.blacklist_branches]

        self.re_valid_paths = []
        for vp in self.mc.cfg.workspace.valid_paths:
            if " => " in vp:
                a, b = vp.split()
            else:
                a = vp
                b = ""
            self.re_valid_paths.append((a, b))

    def update_cache_from_server(self):
        SINCE = helpers.timestamp2isotime(self.cache.timestamp)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            #for gl_proj in self.sc.gl.projects.list(iterator=True, last_repository_updated_at=SINCE):    # note that iterator=True and as_list=False has the same meaning, different versions of the connector
            for gl_proj in self.sc.gl.projects.list(iterator=True, last_activity_after=SINCE):    # note that iterator=True and as_list=False has the same meaning, different versions of the connector
                futures.append(executor.submit(db.Project.from_gl, gl_proj, self))
                print("Got %d projects " % len(futures), end="\r")
            print("Got %d projects " % len(futures))
            i = 0
            for future in concurrent.futures.as_completed(futures):
                if future.result() is None:
                    continue
                i += 1
                print ("Got detailed info for %d/%d projects " % (i, len(futures)), end="\r")
                p: db.Project = future.result() # to trigger exceptions
                self.cache.projects[p.project_id] = p
            print()

        self.map_uid2project = {}
        for proj in self.cache.projects.values():
            if not proj.uid:
                continue
            if proj.uid in self.map_uid2project:
                raise Exception("Duplicate uid: %s" % proj.uid)
            self.map_uid2project[proj.uid] = proj
        logging.debug("mapped %d uids to projects. Total nr of projects=%d" % (len(self.map_uid2project), len(self.cache.projects)))


    def calculate_ws_paths_from_projects(self):
        # calculate workspace paths from repos. Sets the self.ws_paths.

        # a more efficient list of replace key/values. Sort it in reverse length order, as more specific should have precedence of less specific
        _replace_list = [(len(k), k, v) for (k, v) in self.mc.cfg.workspace.replace.items()]
        replace_list = [(k, v) for (l, k, v) in sorted(_replace_list, reverse=True)]

        for p_id, p in self.cache.projects.items():
            # handle home dirs:
            if p.is_home:
                login_name = p.full_path.split("/")[0]
                sub_path = "/".join(p.full_name.split("/")[1:])
                if self.mc.cfg.workspace.home_dir_as_login_name:
                    main_ws_path = self.mc.cfg.workspace.home_dir_prefix + "/" + login_name + "/" + sub_path
                else:
                    main_ws_path = self.mc.cfg.workspace.home_dir_prefix + "/" + p.full_name
#                print (main_ws_path)
#                raise Exception()
            else:
                main_ws_path = p.full_name
#                print (main_ws_path)
#                raise Exception()

            # replace logic:
            for k, v in replace_list:
                if  main_ws_path.startswith(k):
                    main_ws_path = v + main_ws_path[len(k):]
                    break

            # remove slash in the beginning, as we don't want to push out things in the root
            while main_ws_path[0] in "/\\":
                main_ws_path =  main_ws_path[1:]

            s =  main_ws_path.split("/")
            branches_path = "/".join(s[:-1]) + "/_branches"
            p_name = s[-1]

            self.ws_paths[main_ws_path] = (p, p.main_branch)

            if self.mc.cfg.workspace.only_main:
                # config set to only handle main, ie, do not create _branches
                continue
            for b in p.branches.values():
                if not p.main_branch:
                    raise Exception(f"project {p_name} has branches, but no main branch")
                if b.name == p.main_branch:
                    continue
                path = branches_path + "/" + p_name + "-" + b.name
                self.ws_paths[path] = (p, b.name)


    def clone_or_update_ws_paths(self):
        self.fatal_error:str = ""

        def do_update(abs_wsp):
            info = f"update {abs_wsp}"
            print ("*", info)
            try:
                helpers.cmd(["git", "pull"], work_dir=abs_wsp, retries=self.mc.cfg.general.retries)
            except:
                print(f"********* Got error when '{info}' *******")
                self.fatal_error= info
            submodule_init(self, abs_wsp)
            do_git_config(abs_wsp, self.mc.cfg.workspace.config, do_print=False)

        def do_clone(project, url, abs_wsp, branch_name):
            info = f"clone {url} into {abs_wsp}, branch {branch_name}"
            print ("*", info)
            try:
                path, ws_path = os.path.split(abs_wsp)
                os.makedirs(path, exist_ok=True)
                if project.main_branch == branch_name:
                    helpers.cmd(["git", "clone", url, ws_path], work_dir=path, retries=self.mc.cfg.general.retries)
                else:
                    helpers.cmd(["git", "clone", "-b", branch_name, url, ws_path], work_dir=path, retries=self.mc.cfg.general.retries)
                submodule_init(self, abs_wsp)
                do_git_config(abs_wsp, self.mc.cfg.workspace.config, do_print=False)
            except:
                print(f"********* Got error when '{info}' *******")
                self.fatal_error= info

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = {}

            for path, (project, branch_name) in self.ws_paths.items():
                project: db.Project
                if project.uid in self.mc.cfg.rules.blacklist_repo_uids:
                    continue # blacklisted

                url = self.mc.cfg.general.server.git_url + "/" + project.full_path + ".git"
                if branch_name == "_config":
                    continue
                abs_wsp = os.path.join(self.mc.root, path)
                if os.path.exists(abs_wsp):
                    if not branch_name:
                        continue # empty repo
                    if path not in self.workspaces:
                        print ("path %s exists, but seems to be bad. Remove it?" % path)
                        continue
                    if project.branches[branch_name].commit == self.workspaces[path][1]:
                        # no change compared to server
                        continue

                    if self.mc.cfg.general.worker_threads:
                        futures[executor.submit(do_update, abs_wsp)] = abs_wsp
                    else:
                        do_update(abs_wsp)
                else:
                    # clone
                    if self.mc.cfg.general.worker_threads:
                        futures[executor.submit(do_clone, project, url, abs_wsp, branch_name)] = abs_wsp
                    else:
                        do_clone (project, url, abs_wsp, branch_name)

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except:
                    print ("**Error in", futures[future])
                    raise
                if self.fatal_error:
                    raise Exception(f"Got Fatal error from thread when {self.fatal_error}")



    def scan_workspace(self):
        # scan workspace. TODO: should be able to run this in a separate thread, while quering server.
        self.workspaces = {}

        num_scan = 0
        len_ws_root = len(self.mc.root)
        if self.mc.root[-1] not in "\\/":
            len_ws_root += 1
        last_time = 0
        for p, d, f in os.walk(self.mc.root):
            if ".git" in f:
                raise Exception(f"orphan submodule in {p}")
            if not ".git" in d:
                continue

            # found a checkout
            d[:]=[] # don't recurse further down

            num_scan += 1
            t_now = time.time()
            if t_now - last_time > 0.3:
                print("Checked %d workspaces " % num_scan, end="\r")
                last_time = t_now
            try:
                repo = pygit2.Repository(p)
            except:
                print("\nWARNING: Bad repository at", p)
                continue
            try:
                if repo.head_is_unborn:
                    head = branch = ""
                else:
                    head = str(repo.head.target)
                    branch =  repo.head.name.split("/")[-1]
                ws_path = p[len_ws_root:].replace("\\", "/")
                self.workspaces[ws_path] = (branch, head)
            finally:
                repo.free() # important to free resource
        print("Checked %d workspaces  " % num_scan)

    def save_cache(self):
        self.cache.timestamp = self.start_timestamp
        data = self.cache.dict()
        with open(os.path.join(self.mc.root, ".cache.yaml"), "wt") as fh:
            yaml.dump(data, fh)

    def load_cache(self):
        try:
            with open(os.path.join(self.mc.root, ".cache.yaml"), "rt") as fh:
                data = yaml.safe_load(fh)
                self.cache = db.Cache(**data)
        except FileNotFoundError:
            # just skip recreate cache
            pass








#################
#submodule_init(self, url, path)
def submodule_init(uc: UpdateContext, ws_path: str) -> bool:
    """set submodule reference to correct path, based on uid, returns True if updated modules, or False if no modules"""
    logging.debug("submodule_init in %s" % ws_path)
    fn = os.path.join(ws_path, ".gitmodules")
    if not os.path.exists(fn):
        return False    # nothing to do - no submodules
    with open(fn, "rt") as fh:
        gitmodules = fh.read().replace("\t", " "*4)     # TODO: config for tab size?

    cfg = configparser.RawConfigParser()
    cfg.optionxform = lambda option: option
    cfg.read_string(gitmodules)

    sub_paths = []
    for section in cfg:
        if section=="DEFAULT":
            continue
        if section.startswith("submodule \""):
            section_name = section[11:-1]
            logging.debug("section: %s (%s), items:%s" % (section, section_name, str(list(cfg[section].items()))))
            sub_paths.append(cfg[section]["path"])
            uid = ""
            logging.debug(f"Section {section} = {cfg[section]}")
            if "uid" in cfg[section]:
                uid = cfg[section]["uid"]
            elif "url" in cfg[section] and cfg[section]["url"].startswith("../"):
                uid = cfg[section]["url"].split("/")[-1]
                if uid.endswith(".git"):
                    uid = uid[:-4]
            if not uid:
                logging.debug("not relative nor uid for %s" % section)
                continue

            if not uid in uc.map_uid2project:
                logging.debug("couldn't find uid %s in cache" % uid)
                continue

            # change git "config", so submodules point to correct url. Example url:
            # submodule.src/utils.url=ssh://git.allgon.dev/rd/src/common/C_/utils.git

            submodule_project: db.Project = uc.map_uid2project[uid]
            logging.debug("submodule path=%s" % submodule_project.full_path)

            key = f"submodule.{section_name}.url"
            val = uc.mc.cfg.general.server.git_url + "/" + submodule_project.full_path
            logging.debug("set config %s = %s" % (key, val))

            rw = helpers.WorkspaceWrapper(ws_path)
            rw.open()
            rw.repo.config[key] = val
        else:
            raise Exception("Bad section %s" % section)

    arg_list = ["git", "submodule", "update"]
    arg_list.append("--init")

    helpers.cmd(arg_list, work_dir=ws_path, retries=uc.mc.cfg.general.retries)

    for p in sub_paths:
        ap = os.path.join(ws_path, p)
        if not os.path.exists(ap):
            continue
        submodule_init(uc, ap)

    return True



#################


def main_update(args):
    uc = UpdateContext(args)

    uc.scan_workspace()
    uc.update_cache_from_server()

    uc.save_cache()

    uc.calculate_ws_paths_from_projects()

    ws_from_srv = set(uc.ws_paths.keys())
    ws_from_scan = set(uc.workspaces.keys())
    #ws_only_srv = ws_from_srv - ws_from_scan
    ws_only_scan = ws_from_scan - ws_from_srv
    if ws_only_scan:
        print (f"{len(ws_only_scan)} workspaces locally that the server doesn't have:")
        for ws in sorted(ws_only_scan):
            print (ws)

    uc.clone_or_update_ws_paths()

    uc.save_cache()     # save again. Might have updates ws info


##################

def main_test1(args):
    sc = ServerConnector(args)
    cache = db.Cache(projects={})
    uc = UpdateContext(args, sc, cache)
    print ("-"*40)
    uc.scan_workspace()
    print ("-"*40)

    return

    time_start = time.time()
    try:
        calculate_ws_paths_from_projects()
        old_cwd = os.getcwd()
        os.chdir("c:/dev2")
        main_test1_work(args)
    finally:
        time_elapsed = time.time() - time_start
        os.chdir(old_cwd)
        print ("Took", time_elapsed)


def main_test1_work(args):
    t0 = time.time()

    SINCE = "2023-05-20T12:22:33Z"
    #SINCE = "2023-05-01T12:22:33Z"
    #SINCE = "2023-04-01T12:22:33Z"
    #SINCE = "2023-03-01T12:22:33Z"
    #SINCE = ""
    sc =  ServerConnector(None)
    cache = db.Cache(projects={})
    uc =  UpdateContext(args, sc, cache)
    if 0:
        groups = sc.gl.groups.list(get_all=True)
        print ("nr of groups:", len(groups))
        for g in groups[:2]:
            #print(g)
            print(g.id, g.web_url, g.name)
            # name is visible name
            # path is last part of url
            # full_path is complete path (but without server url)

    if 0:
        # clearly slower than the thread pool
        t0 = time.time()

        projects = []
        for gl_proj in sc.gl.projects.list(iterator=True, as_list=False, last_activity_after=SINCE):    # note that iterator=True and as_list=False has the same meaning, different versions of the connector
            projects.append(gl_proj)
        #projects = sc.gl.projects.list(get_all=True, last_activity_after="")
        print ("nr of projects:", len(projects), time.time() - t0)

        for glp in projects:
            #print (glp)
            p = db.Project.from_gl(glp, uc)
            #print (p)
        #print (glp)
        print ("Checked projects:", len(projects), time.time() - t0)

    if 0:
        i = 0
        for ps in sc.gl.projects.list(iterator=True, as_list=False, last_activity_after=SINCE):    # note that iterator=True and as_list=False has the same meaning, different versions of the connector
            print (i)
            i += 1

    print ("-"*30)
    if 1:
        # as gettings branches is a separate call, this setup seems to be more than twice as fast as the simple way. Probably more speedups if need to get UID
        t0 = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for gl_proj in sc.gl.projects.list(iterator=True, last_activity_after=SINCE):    # note that iterator=True and as_list=False has the same meaning, different versions of the connector
                futures.append(executor.submit(db.Project.from_gl, gl_proj, uc))
                print("Got %d projects " % len(futures), end="\r")
            print()
            print ("nr of projects:", len(futures), time.time() - t0)
            i = 0
            for future in concurrent.futures.as_completed(futures):
                i += 1
                print ("Got detailed info for %d/%d projects " % (i, len(futures)), end="\r")
                _ = future.result() # to trigger exceptions
                #print (future.result())
            print()
            print ("Got result for %d project" % i, time.time() - t0)

class WSStatus:
    def __init__(self, repo: pygit2.Repository):
        self.branch_name = "" # default, set below
        self.workdir = repo.workdir     # always points to main repo (no submodule)
        self.gitctrl_path = repo.path
        self.is_pushed = True  # default, but check below
        self.head_is_detached:bool = repo.head_is_detached
        self.is_empty:bool = repo.is_empty
        self.status :dict = repo.status(untracked_files="normal")

        # detailed status:
        self.st_untracked = set()
        self.st_modified = set()
        self.st_new_file = set()
        self.st_unknown = dict()

        if self.status:
            self.is_pushed = False

        if self.is_empty:
            return

        branches = list(repo.branches)
        if not branches:
            if not self.status:
                # seems like some empty repos are not reported as empty. Assume it is empty if no branches and status is empty:
                self.is_empty = True
                return

        for fn, code in self.status.items():
            if code & 1:
                self.st_new_file.add(fn)
                code &= ~1
            if code & 128:
                self.st_untracked.add(fn)
                code &= ~128
            if code & 256:
                self.st_modified.add(fn)
                code &= ~256
            if code:
                self.st_unknown[fn] = code

        if self.head_is_detached:
            head: pygit2.Reference = repo.head

            for b_name in branches:
                if not b_name.startswith("origin/"):
                    continue
                remote_ref = repo.resolve_refish(b_name)[1]
                if head.target == remote_ref.target:
                    break   # points to a remote branch
                if repo.descendant_of(repo.get(remote_ref.target).oid, repo.get(head.target).oid):
                    break   # remote branch is a descendant of local commit (ie, newer, ie pushed)
            else:
                self.is_pushed = False
        else:
            # normal:

            n_local = branches[0]
            self.branch_name = n_local
            b_local = repo.lookup_branch(n_local)
            b_remote = b_local.upstream
            if not b_remote:
                # seems like upstream is not always set, this is a work-around:
                n_remote = "origin/"+n_local
                b_remote = repo.resolve_refish(n_remote)[1]
            if not b_remote:
                print (f"\n** strange, {self.workdir}, branch {n_local} doesn't have a remote")
                print ("  ",branches)
                self.is_pushed = False
            else:
                r_local = repo.lookup_reference(b_local.name)
                r_remote= repo.lookup_reference(b_remote.name)

                if r_local.target != r_remote.target:
                    self.is_pushed = False

    def __str__(self):
        return f"""workdir: {self.workdir}
path: {self.gitctrl_path}
branch: {self.branch_name}
is_pushed: {self.is_pushed}
"""

    def check_submodules(self) -> set[str]:
        not_pushed = set()
        for p, d, f in os.walk(self.workdir):
            if p == self.workdir:
                continue # skip top directory, submodules always reside in a sub-directory
            if ".git" in f:
                repo = pygit2.Repository(p)
                try:
                    wss = WSStatus(repo)
                finally:
                    repo.free()
                wss.check_submodules()
                if not wss.is_pushed:
                    not_pushed.add(p)
        return not_pushed





def main_clean_ws(args):
    uc = UpdateContext(args)

    uc.scan_workspace()
    uc.update_cache_from_server()

    uc.save_cache()

    uc.calculate_ws_paths_from_projects()

    ws_from_srv = set(uc.ws_paths.keys())
    ws_from_scan = set(uc.workspaces.keys())
    #ws_only_srv = ws_from_srv - ws_from_scan
    ws_only_scan = ws_from_scan - ws_from_srv
    if ws_only_scan:
        print (f"{len(ws_only_scan)} workspaces locally that the server doesn't have:")
        for ws in sorted(ws_only_scan):
            #print (ws)
            ws_path =  os.path.join(uc.mc.root, ws)
            repo = pygit2.Repository(ws_path)
            try:
                wss = WSStatus(repo)
            finally:
                repo.free()
                del repo
            not_pushed = wss.check_submodules()
            if not_pushed or not wss.is_pushed:
                print ("skipping repo (not pushed)", ws_path)
                if not_pushed:
                    for p in sorted(not_pushed):
                        print("* Submodule not pushed:", p)
            else:
                if args.yes:
                    print ("remove path", ws_path)
                    def set_rw(func, path, exc_info):
                        # git sets a lot of files to read-only, so assume this is why we cannot remove it and set to read/write
                        if os.name == "nt":
                            win32file.SetFileAttributes(path, win32file.FILE_ATTRIBUTE_NORMAL)
                        else:
                            os.chmod(path, os.stat.S_IWRITE)
                        os.unlink(path)
                    shutil.rmtree(ws_path, onerror=set_rw)

                else:
                    print ("should remove path (no --yes)", ws_path)

    uc.save_cache()     # save again. Might have updates ws info



def main_status(args):
    for p, d, f in os.walk(args.root):
        if ".git" in f:
            raise Exception(f"orphan submodule in {p}")
        if not ".git" in d:
            continue

        # found a checkout
        d[:]=[] # don't recurse further down

        p_space = p + " "*(78-len(p))+" "
        print (p_space, end="\r")

        repo = pygit2.Repository(p)
        try:
            has_print_lf = False
            wss = WSStatus(repo)

            if wss.status or not wss.is_pushed:
                has_print_lf = True
                print("*", p_space)
                if not wss.is_pushed:
                    print ("Not pushed!")
                if wss.st_new_file:
                    print ("new_file", sorted(wss.st_new_file))
                if wss.st_modified:
                    print ("modified", sorted(wss.st_modified))
                if wss.st_untracked:
                    print ("untracked", sorted(wss.st_untracked))
                if wss.st_unknown:
                    print ("misc", wss.st_unknown)

            if args.submodules:
                for p2, d2, f2 in os.walk(p):
                    if ".git" in f2:
                        repo2 = pygit2.Repository(p2)
                        try:
                            wss2 = WSStatus(repo2)
                            if not wss2.is_pushed:
                                if not has_print_lf:
                                    print("*", p_space)
                                    has_print_lf = True
                                print ("submodule not pushed:", p2)
                        finally:
                            repo2.free()
            if has_print_lf:
                print()

        finally:
            repo.free() # important to free resource
    print(" "*80)   # erase last dbg print




def get_user(repo_path, user_fatal=False) -> typing.Optional[tuple[str, str]]:
    r = pygit2.Repository(repo_path)
    try:
        return (r.config["user.name"], r.config["user.email"])
    except:
        if user_fatal:
            raise Exception("""You need to set user, either locally, or globally with
    git config --global user.name "Your Name"
    git config --global user.email you@example.com
""")
        else:
            return None



def main_set_uid (args):
    # helper function:
    def create_random_uid(uidlen=32, force=False) -> None:
        # make lower case + digit str (5 bits/char):
        uid_str = ""
        for _ in range(uidlen):
            v = secrets.randbits(5)
            if v < 26:
                c = chr(ord('a') + v)
            else:
                c = chr(ord('0') + v - 26)
            uid_str += c
        return uid_str

    def commit_and_push(repo_path: str, cfg_data, no_push: bool):
        person = get_user(repo_path, user_fatal=True)
        r = pygit2.Repository(repo_path)
        branches_list = list(r.branches)
        for b in ["_config", "origin/_config"]:
            if b in branches_list:
                raise Exception("Repo already has branch %s" % b)
        #raise Exception()
        tree = r.TreeBuilder()
        attr_oid = r.create_blob(yaml.safe_dump(cfg_data).encode("utf8"))
        tree.insert("attributes.yaml", attr_oid, pygit2.GIT_FILEMODE_BLOB)
        tree_oid = tree.write()
        signature = pygit2.Signature(*person)   # "system","system@none")
        parents = []
        comm_oid = r.create_commit("refs/heads/_config", signature, signature, "create _config", tree_oid, parents)

        if not no_push:
            print("Pushing change to origin:")
            helpers.cmd(["git", "push", "origin", "_config"], work_dir=repo_path, allow_nonzero=True)


    uid = create_random_uid()
    cfg_data = {
        "uid": uid,
    }
    print ("UID:", uid)
    commit_and_push (".", cfg_data , no_push=args.nopush)



def uid_get_relative_path(proj, rem_url: str) -> str:
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
    s_srv = proj.full_path.split("/")
    while s_rem[0] == s_srv[0]:
        s_rem = s_rem[1:]
        s_srv = s_srv[1:]
    rem = "/".join(s_rem)
    srv = "/".join(s_srv)
    if not srv.endswith(".git"):
        srv += ".git"
    logging.debug("rem_url: %s => %s" % (rem_url, rem))
    logging.debug("proj.server_full_path: %s => %s" % (proj.full_path, srv))
    return "../" * (rem.count("/") + 1) + srv



def main_uid_clean_gitmodules(args):
    uc = UpdateContext(args)

    rw = helpers.WorkspaceWrapper(args.root)
    rw.open()
    index = rw.repo.index
    index.read()
    subs = [idx_entry for idx_entry in index if (idx_entry.mode & pygit2.GIT_FILEMODE_TREE)]
    fn_gitmod = os.path.join(rw.ws_path, ".gitmodules")
    print ("clean gitmodules in", rw.repo_path)
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

    uid_map = uc.cache.build_uid_map()

    new_gitmod = ""
    for path, defs in sm_path_to_section.items():
        if path in all_subm_found:
            proj = None
            if "uid" in defs:
                proj = uid_map.get(defs["uid"],None)
            elif defs["url"].startswith("../") or defs["url"].startswith("..\\"):
                # logging.debug("submodule %s url=%s" % (path, defs["url"]))
                url_fix = defs["url"].replace("\\","/")
                if url_fix.endswith(".git"):
                    url_fix = url_fix[:-4]
                url_uid = url_fix.split("/")[-1]
                if url_uid in uid_map:
                    proj = uid_map[url_uid]
                else:
                    root_repo_abspath = helpers.remove_protocol_host_from_url(rw.repo.config["remote.origin.url"])
                    apath = helpers.url_make_absolut(root_repo_abspath, url_fix)
                    logging.debug("try to find uid for '%s' root_path='%s' url_fix='%s' => '%s'" % (path, root_repo_abspath, url_fix, apath))

                    print (apath)
                    for p in uc.cache.projects.values():
                        if p.full_path==apath or p.full_path==apath+".git":
                            proj = p
                            break
                    else:
                        logging.debug("=> couldn't find relative path. Just keep it")

            if proj:
                if proj.uid:
                    defs["uid"] = proj.uid

                remote_url = rw.repo.config["remote.origin.url"]
                if remote_url:
                    defs["url"] = uid_get_relative_path(proj, remote_url)

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



def do_git_config(root: str, config: dict, do_print=True):
    for p, d, f in os.walk(root):
        if not (".git" in d or ".git" in f):
            continue

        # found a checkout
        if do_print:
            print (p, " "*(70-len(p)), end="\r")
        for k,v in config.items():
            helpers.cmd(f'git config --local --unset-all "{k}"', work_dir=p, allow_nonzero=True)
            helpers.cmd(f'git config --local --add "{k}" "{v}"', work_dir=p, allow_nonzero=True)

def main_git_config(args):
    uc = UpdateContext(args)
    config =uc.mc.cfg.workspace.config

    print ("Applying to local repos:")

    for k,v in config.items():
        print(k, v)

    do_git_config(args.root, config, do_print=True)

    print("\nDone")



def main(in_args):
    time_start = time.time()

    if gitlab.__version__ < "3.14.0":
        print ("Warning: mainly tested with python-gitlab 3.14.0. Running with older version %s" % gitlab.__version__)

    parser = argparse.ArgumentParser(prog="gcln2", description="Git Collection 2 - tool to manage many repositories in gitlab")
    parser.add_argument("--root", type=str, default=".", help="parent directory for all the workspaces. Default is to search for gcln2.yaml")
    parser.add_argument("--run_dir", type=str, help="if set, the working directory will be changed to this at st1artup")
    parser.add_argument("--all", action="store_true", help="do a full update, ignore cache")
    parser.add_argument("--log", choices=["DEBUG", "INFO", "WARNING"], type=str.upper, default="WARNING", help="logging level")
    parser.add_argument("--version", action="version", version="%(prog)s " + __version__ + ", python=" + sys.version + ", exec: " + sys.argv[0])

    if sys.version_info.minor <= 8:  #py3.8
        subparsers = parser.add_subparsers(help="sub-command help")
    else:
        subparsers = parser.add_subparsers(help='sub-command help', required=True)

    p_update = subparsers.add_parser("update", help="optimized update")
    p_update.set_defaults(func=main_update)

    p_status = subparsers.add_parser("status", help="do a git status in all git. Doesn't need a gitcoll tree")
    p_status.add_argument("-s", "--submodules", action="store_true", help="explicit check in submodules")
    p_status.set_defaults(func=main_status)

    p_clean_ws = subparsers.add_parser("clean_ws", help="Remove all local workspaces that do not match server _if_ they've pushed everything and are clean")
    p_clean_ws.add_argument("--yes", action="store_true", help="actually remove the directories")
    p_clean_ws.set_defaults(func=main_clean_ws )

    p_set_uid = subparsers.add_parser("set_uid", help="set uid in repo, ie, create _config branch and yaml file in that")
    p_set_uid .add_argument("--uid", default="", help="use this as uid instead of random value")
    p_set_uid .add_argument("--nopush", action="store_true", help="do not push the result to the server")
    p_set_uid.set_defaults(func=main_set_uid )

    p_uid_clean_gitmodules = subparsers.add_parser("clean_gitmodules", help="rewrite .gitmodules with uid lookup etc")
    p_uid_clean_gitmodules.set_defaults(func=main_uid_clean_gitmodules)

    p_uid_clean_gitmodules = subparsers.add_parser("git_config", help="apply git config in all repos")
    p_uid_clean_gitmodules.set_defaults(func=main_git_config)

    p_test1 = subparsers.add_parser("test1", help="Testing #1")
    p_test1.set_defaults(func=main_test1)

    args = parser.parse_args(in_args)

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
            except exceptions.UserError as err:
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


def main_no_args():
    main(sys.argv[1:])


if __name__ == "__main__":
    main_no_args()
