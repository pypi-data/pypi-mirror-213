# Database

# py38 support:
from __future__ import annotations


import base64
import typing
import logging

import yaml
import pydantic
import gitlab
import gitlab.v4.objects



# data in cache:
# per repository (gitlab project):
# * project nr
# * branches we care about
# * full_name and full_path
# * workspace path (normally full_name, but there are substitution possibilities)
# * UID

# * for every branch:
#   * name
#   * latest known commit ID
#   * gitmodules

# per workspace:
# * path
# * project uid and path


#@dataclasses.dataclass
class Branch(pydantic.BaseModel):
    name: str
    commit: str
    submodules: typing.Dict[str, str]        # submodule UIDs to path. TODO: record if we track a branch?



#@dataclasses.dataclass
class Project(pydantic.BaseModel):
    project_id: int         # gitlab project number
    main_branch: str        # empty str if no main_branch
    full_path: str      # https path without the https
    full_name: str      # group/project names, ie, should be used for workspace etc.
    #ws_full_name: str
    branches: typing.Dict[str, Branch]
    tags: typing.Dict[str, str]        # tag => commit-id
    uid: str
    alt_uids: typing.List[str]
    is_home: bool

    @classmethod
    def from_gl(cls, gl_project, update_context: "UpdateContext"):
        logging.debug(str(gl_project))
        return project_from_gl(gl_project, update_context)

class Cache(pydantic.BaseModel):
    projects: typing.Dict[int, Project] = {}       # mapping form GL project ID to project
    timestamp: float = 0.0

    def build_uid_map(self) -> typing.Dict[str, Project]:
        ret = {}
        for p in self.projects.values():
            if p.uid:
                if p.uid in ret:
                    raise Exception("duplicate uid %s" % p.uid)
                ret[p.uid] = p
        return ret


#################

def project_from_gl(gl_project: gitlab.v4.objects.Project,
                    update_context: "main.UpdateContext") -> typing.Optional[Project]:
    """returns NULL if cannot retrieve information for the project (permisison issues). We cannot trust the permission attribute :-("""
    full_name = gl_project.name_with_namespace.replace(" / ", "/").strip()

    my_branches = {}
    try:
        for b in gl_project.branches.list(iterator=True):
            if b.name != "_config" and not update_context.re_valid_branches.fullmatch(b.name) and b.name != gl_project.default_branch:
                continue

            # TODO: optional, but should check for submodules. Optimization: if cache already points to the same commit for this branch, then no need to retrieve it again
            if 0:
                for item in gl_project.repository_tree(path="", recursive=False, ref=b.name, iterator=True):
                    if item["name"] == ".gitmodules":
                        file_info = gl_project.repository_blob(item["id"])
                        content = base64.b64decode(file_info["content"])
                        # content is binary data from git, file .gitmodules. Need to parse it to understand submodules
                        #print (content)

            b2 = Branch(name=b.name, commit=b.attributes["commit"]["id"], submodules=set())
            my_branches[b.name] = b2
    except gitlab.exceptions.GitlabListError:
        # probably don't have access to this project.
        return None


    # optional to check for tags?
    tags = {}
    for tag in gl_project.tags.list(iterator=True):
        if 0: # TODO: check if valid tag
            continue
        #print (tag.attributes)
        tags[tag.attributes["name"]] =  tag.attributes["commit"]["id"]
    #print(tags)

    # optional to check for uid. If cache already has it, don't bother? Or at least (most common), if the _config branch hasn't changed, no need to check.
    uid = ""
    alt_uids = []
    if "_config" in my_branches:
        for item in gl_project.repository_tree(path="", recursive=False, ref="_config", iterator=True):
            if item["name"] == "attributes.yaml":
                file_info = gl_project.repository_blob(item["id"])
                content = base64.b64decode(file_info["content"])
                cfg = yaml.safe_load(content.decode("utf8"))
                uid = cfg.get("uid", "")
                alt_uids = cfg.get("alt_uids", [])
                break
    else:
        #print ("*** no _config", gl_project.path_with_namespace)
        pass

    # note that we try to retrieve information about projects, even if they're in the black list. This way, we can use the .cache.yaml file to find UIDs.

    if gl_project.default_branch and gl_project.default_branch in my_branches:
        main_branch = gl_project.default_branch
    else:
        main_branch = ""

#    if gl_project.namespace["kind"] == "group":
#        ws_full_name = full_name
#    else:
#        cfg.
#        ws_full_name = "home/" + full_name

    ret = Project(
        project_id=gl_project.get_id(),
        main_branch=main_branch,
        full_path=gl_project.path_with_namespace,
        full_name=full_name,
 #       ws_full_name=ws_full_name,
        branches=my_branches,
        tags=tags,
        uid=uid,
        alt_uids=alt_uids,
        is_home=gl_project.namespace["kind"]!="group",
    )

#    if ret.is_home:
#        print(ret)

    return ret
