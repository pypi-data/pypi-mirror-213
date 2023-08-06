# server connectors, ie, handles communication with different kind of servers

from __future__ import annotations

import yaml
import time
import base64
import logging
import datetime
from typing import Optional

import gitlab
#import pygit2

from gcln import records

class ConnectorBase:
    def __init__(self, srv_name: str, spec: dict):
        self.srv_name = srv_name
        self.spec = spec
        self.server_type: str = spec["type"]

    @classmethod
    def create(cls, srv_name, spec: dict, root: Optional[str] = None) -> "ServerConnectorBase":
        if spec["type"]=="gitlab":
            return GitlabConnector(srv_name, spec)
        if spec["type"]=="raw":
            return RawConnector(srv_name, spec, root)
        raise Exception("Unknown git server type:" + spec["type"])


class GitlabConnector(ConnectorBase):
    def __init__(self, srv_name: str, spec: dict):  # connector: gitlab.Gitlab):
        super().__init__(srv_name, spec)
        self.gl: gitlab.Gitlab = gitlab.Gitlab(self.spec["api_url"], private_token=self.spec["private_token"])
        self.per_page = 20      # for list apis, use this per_page

        self.url_root = spec.get("git_url", "")

        # TODO: is probably not needed:
        self.updated_projects: set[tuple[str,str]] = set()    # set of all project [uid, srv_id] that were updated in update_cache



    def update_cache(self, cache:records.ServerCacheInfo, update_groups:bool) -> dict[str,records.RepoInfo]:  # returns uuid to project map
        """connects to server, and updates the cache with current data. If update_groups, then also retrieve group hierarchy. Uses timestamp in old cache top optimize the update."""
        update_time = time.time()

        project_map = self.gl_get_changed_projects_with_uid(changed_after=cache.last_check)

        if update_groups:
            groups = self.gl_get_all_groups_w_projid(project_map)
            cache.groups = [records.GroupInfo(srv_id=str(gid),
                                              name=grp.name,
                                              full_name=grp.full_name,
                                              project_uids = [("",str(p)) for p in projs],
                                              server_full_path=grp.full_path)
                            for gid,(grp,projs) in groups.items()]

        # if a group refers to an unknown project, then fetch it.
        known_projs = {int(r.srv_id) for r in cache.repos}
        fetch_pids = set()
        for grp in cache.groups:
            for uid, srvid in grp.project_uids:
                pid = int(srvid)
                if pid not in known_projs and pid not in project_map:
                    fetch_pids.add(pid)
        for pid in fetch_pids:
            proj = self.gl.projects.get(pid)
            if proj.archived:
                continue  # skip archived projects
            project_map[pid] = self.gl_get_one_project_with_branches(proj)

        # TODO: make a group for home/<name>?

        # copy all cached repos that have not been updated.
        new_repos = [r for r in cache.repos if int(r.srv_id) not in project_map]

        # then add all newly updated projects to the cache
        for proj_id,(project, gl_branches, uid, alt_uids) in project_map.items():
            r = records.RepoInfo(
                server_name = project.name,                     # no slash
                server_full_path=project.path_with_namespace,   # full path, _not_ name
                uid=uid,
                srv_id = str(proj_id),
                branches=[records.BranchInfo(name=b.name, commit_id=commit) for b,commit in gl_branches],
                srv_last_activity="",
                alt_uids=alt_uids,
                owner_kind=project.namespace["kind"]
            )
            # if r.owner_kind != "group":
                # print ("***", r)

            #print(proj_id, project.name)
            new_repos.append(r)

        cache.repos = new_repos
        cache.last_check = update_time

        # calculate maps which points directly into a cache object. Ie, when altering objects through these maps, the cache data is updated directly.
        map_srvid_project:dict[str,records.RepoInfo] = {proj.srv_id:proj for proj in cache.repos}       # TODO: skip if srv_id is ""?
        map_uid_project:dict[str,records.RepoInfo] = {proj.uid:proj for proj in cache.repos}            # TODO: skip if proj_id is ""?
        map_all_uid_project: dict[str, records.RepoInfo] = {}

        for proj in cache.repos:
            if proj.uid in map_all_uid_project:
                p2 = map_all_uid_project[proj.uid]
                raise Exception(f"project at {proj.server_full_path}, name {proj.server_name}, id {proj.uid} is duplicate of {p2.server_full_path}/{p2.server_name}")
            if proj.uid:
                map_all_uid_project[proj.uid] = proj
            for au in proj.alt_uids:
                if not au:
                    raise Exception()
                if au in map_all_uid_project:
                    p2 = map_all_uid_project[proj.uid]
                    raise Exception(f"project at {proj.server_full_path}, name {proj.server_name}, alt-uid {au} is duplicate of {p2.server_full_path}/{p2.server_name}")
                map_all_uid_project[au] = proj
        # Also, set uid for projects in grp
        for grp in cache.groups:
            # check if srvid in map, if not - it is probably an archived project
            # then check if we have a uid, then use it. But for newly added projects in a group, this is "", then use the map_srvid_project to look it up
            grp.project_uids = [(uid, srvid) if uid else (map_srvid_project[srvid].uid, srvid) for uid, srvid in grp.project_uids if srvid in map_srvid_project]

        # now all repos and groups are updated from server. TODO: personal repos???

        self.updated_projects = { (map_srvid_project[str(srv_id)].uid,str(srv_id)) for srv_id in project_map.keys() }

        return map_uid_project



    @classmethod
    def _changed_after_to_arg(cls, changed_after:Optional[float]) -> Optional[str]:
        """helper function to get isoformat which is compatible with gitlab API"""
        if changed_after:
            dt = datetime.datetime.utcfromtimestamp(int(changed_after-3600))    # TODO: timezone? Or is this just to get some extra margin?
            ret = dt.isoformat()
            if not ret[-1]=="Z":
                ret += "Z"
            return ret
        else:
            return None

    def gl_get_group(self, full_path: str) -> Optional[gitlab.group]:
        try:
            return self.gl.groups.get(full_path)
        except:
            return None
        # for g in r:
        #    if g.attributes["full_path"] == full_path:
        #        return g
        # return None

    def gl_get_project(self, full_path: str) -> Optional[gitlab.project]:
        try:
            return self.gl.projects.get(full_path)
        except:
            return None
        #r = self.gl.projects.list(search=full_path)
        # for p in r:
        #   if p.attributes["path_with_namespace"] == full_path:
        #        return p
        #return None

    def gl_create_group(self, parent: Optional[int], name: str, path: str) -> gitlab.group:
        return self.gl.groups.create({"parent_id": parent, "name": name, "path": path})

    def gl_create_project(self, parent: Optional[int], name: str, path: str) -> gitlab.project:
        return self.gl.projects.create({"namespace_id": parent, "name": name, "path": path})

    def gl_gencall_paginated(self, func, changed_after:Optional[float], **args) -> list:
        ret = []
        page = 1
        last_activitity = GitlabConnector._changed_after_to_arg(changed_after)
        while 1:
            try:
                next_list = func(per_page=self.per_page, page=page, last_activity_after=last_activitity, **args)
            except gitlab.exceptions.GitlabListError as e:
                print ("Warning,", e)
                if isinstance(func.__self__, gitlab.v4.objects.branches.ProjectBranchManager):
                    # seems like it is possible to create a project with read access to wiki, but not repository. Then we get a access error when check for branches.
                    print ("path:", func.__self__.path)
                # print("func=", func)
                # print (func.__self__)
                # print (func.__self__.gitlab)
                # print (dir(func.__self__))
                # print (dir(func))
                # print("page=", page)
                # print("args=", args)
                next_list = []
                # raise
            except:
                print("func=", func)
                print("page=", page)
                print("args=", args)
                raise
            if next_list:
                ret += next_list
            if not next_list or len(next_list)<self.per_page:
                logging.debug(f"Got {len(ret)} results from {page} pages")
                return ret
            page += 1

    def gl_get_all_projects(self, changed_after: Optional[float]) -> list["gitlab.Project"]:
        return self.gl_gencall_paginated(self.gl.projects.list, changed_after, archived=False)

    def gl_get_all_branches_in_project(self, project:"gitlab.project") -> list["gitlab.branch"]:
        return self.gl_gencall_paginated(project.branches.list, None)

    def gl_get_all_projects_in_group(self, group, changed_after: Optional[float], simple=False) -> list["gitlab.Project"]:
        return self.gl_gencall_paginated(group.projects.list, changed_after, simple=simple)

    def gl_get_all_groups(self, changed_after) -> list:
        return self.gl_gencall_paginated(self.gl.groups.list, changed_after)

    def gl_get_one_project_with_branches(self, project:"gitlab.Project") -> tuple["gitlab.project", list[tuple["gitlab.branch",str]], str, list[str]]:
        #project = self.gl.projects.get(pid)

        # if project.namespace["kind"] != "group":
            # print ("******", project.path_with_namespace, ":::", project.namespace)
            # print ("  ", project)
        gl_branches = []
        for b in self.gl_get_all_branches_in_project(project):
            gl_branches.append( (b, b.commit["id"].upper()) )
        uid, alt_uids = "",[] #= get_uids(project, gl_branches)
        if "_config" in [b.name for b,c in gl_branches]:
            items = project.repository_tree(path="", ref="_config")
            items = [item for item in items if item["name"]=="attributes.yaml"]
            if len(items)==1:
                file_info = project.repository_blob(items[0]["id"])
                content = base64.b64decode(file_info["content"])
                cfg = yaml.safe_load(content.decode("utf8"))
                uid = cfg.get("uid", "")
                alt_uids = cfg.get("alt_uids", [])
        return (project, gl_branches, uid, alt_uids)

    def gl_get_changed_projects_with_uid(self, changed_after=None) -> dict[int, tuple["gitlab.Project", list[tuple["gitlab.v4.objects.ProjectBranch", str]], str, list[str]]]:
        proj_map = {}

        for project in self.gl_get_all_projects(changed_after):
            if project.archived:
                continue  # don't care about archived projects

            if project.id in proj_map:
                raise Exception("id collision")

            #gl_branches = []
            #for b in self.gl_get_all_branches_in_project(project):
                #gl_branches.append( (b, b.commit["id"]) )
            #uid, alt_uids = get_uids(project, gl_branches)

            (project, gl_branches, uid, alt_uids) = self.gl_get_one_project_with_branches(project)
            for au in alt_uids:
                if au in proj_map:
                    raise Exception("id collision")
            proj_map[project.id] = (project, gl_branches, uid, alt_uids)

        return proj_map

    def gl_get_all_groups_w_projid(self, project_map) -> dict[int, tuple["gitlab.Group", list[int]]]:
        # note that this function might include project refs in a group that are archived
        groups_with_projs:dict[int,tuple] = {}
        for g in self.gl_get_all_groups(None): # changed_after doesn't seem to work, gets all groups anyway
            if g.id in groups_with_projs:
                raise Exception()

            proj_ids = []
            for p in self.gl_get_all_projects_in_group(g, None, simple=True):  # g.projects.list(all=True):
                # if cached, we might get a project which is not in the map
                proj_ids.append(p.id)

            groups_with_projs[g.id] = (g, proj_ids)
        return groups_with_projs





class RawConnector(ConnectorBase):
    pass
