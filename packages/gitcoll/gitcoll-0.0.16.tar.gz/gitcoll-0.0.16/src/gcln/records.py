# records - define data holding structures, ie, not much logic here.

from __future__ import annotations

import dataclasses
from typing import Optional

import pygit2



@dataclasses.dataclass
class DataClassBase:
    def as_dict(self):
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, d:dict):
        return cls(**d)

###############################


@dataclasses.dataclass(order=True)
class BranchInfo(DataClassBase):
    name: str = ""
    # checkout path for the branch
    #checkout: str = ""
    commit_id: str = b""

    @classmethod
    def from_dict(cls, d:dict):
        return cls(**d)

@dataclasses.dataclass(order=True)
class RepoInfo(DataClassBase):
    server_name: str = ""   # repo name on server
    #server_path: str = ""
    server_full_path: str = ""  # path/url to the server
    #ws_path: str = ""       # path in workspace for master branch
    uid: str = ""
    srv_id: str = ""        # if the server has an ID
    branches: list[BranchInfo] = dataclasses.field(default_factory=list)
    srv_last_activity: str = ""  # if server has info about when was latest activity, it is stored here.
    alt_uids: list[str] = dataclasses.field(default_factory=list)
    owner_kind: str=""      # normally group or user

    @classmethod
    def from_dict(cls, d:dict):
        d["branches"] = [BranchInfo.from_dict(b) for b in d["branches"]]
        d["alt_uids"] = [str(u) for u in d.get("alt_uids", [])]
        return cls(**d)

@dataclasses.dataclass
class GroupInfo(DataClassBase):
    srv_id: str
    name:str
    full_name:str
    server_full_path: str = ""
    project_uids:list[tuple[str,str]] =  dataclasses.field(default_factory=list)    # (uid, srv_id) tuple for all projects.

@dataclasses.dataclass
class ServerCacheInfo(DataClassBase):
    last_check: float = 0       # when was the last query to the server (seconds since epoch/utc)?
    server_name: str = ""       # name of the server
    server_type: str = ""

    repos: list[RepoInfo] = dataclasses.field(default_factory=dict) # projects/repos on the servers. key is uid
    groups: list[GroupInfo] = dataclasses.field(default_factory=list)   # list of all groups on the server. Ie, containers of projects.

    # links/refs to projects from other structures. Ie, in gitlab, this is all shared projects with a group.
    #repo_aliases: list[RepoInfo] = dataclasses.field(default_factory=list)

    @classmethod
    def from_dict(cls, d:dict):
        d["repos"] = [ RepoInfo.from_dict(r) for r in d["repos"] ]
        d["groups"] = [ GroupInfo.from_dict(r) for r in d["groups"] ]
        #d["repos"] = [ RepoInfo.from_dict(r) for r in d["repos"] ]
        #d["repo_aliases"] = [ RepoInfo.from_dict(r) for r in d["repo_aliases"] ]
        return cls(**d)

@dataclasses.dataclass
class GitCheckout(DataClassBase):
    path: str = ""
    branch: str = ""
    status: dict[str, int] = dataclasses.field(default_factory=dict)
    head: str = ""  # either empty string if undefined/empty git rep, or commit-ID as str for the head.
    # repo: Optional[pygit2.Repository] = None
    submodules:list["SubmoduleCheckout"] = dataclasses.field(default_factory=list)
    status_no_head: bool = False        # an explicit check gave error
    level: int = 0  # 0 for main checkout, 1 for submodules directly under MainCheckout, one more for every sub-module lvl

    def __iter__(self):
        for co in self.submodules:
            yield co
            for s in co:
                yield s


@dataclasses.dataclass
class TotalCache(DataClassBase):
    main_server: ServerCacheInfo = dataclasses.field(default_factory=ServerCacheInfo)
    aux_servers: list[ServerCacheInfo] = dataclasses.field(default_factory=list)
    checkouts: list[GitCheckout] = dataclasses.field(default_factory=list)

    @classmethod
    def from_dict(cls, d:dict):
        try:
            d["main_server"] = ServerCacheInfo.from_dict(d["main_server"])
            d["aux_servers"] = [ ServerCacheInfo.from_dict(s) for s in d.get("aux_servers",[]) ]
            d["checkouts"] = [ GitCheckout.from_dict(s) for s in d.get("checkouts",[]) ]
            return cls(**d)
        except:
            print (d)
            raise
