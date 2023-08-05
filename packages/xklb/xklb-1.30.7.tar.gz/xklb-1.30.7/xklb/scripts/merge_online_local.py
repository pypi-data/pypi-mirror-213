import argparse
from copy import deepcopy
from typing import List, Optional

from tabulate import tabulate

from xklb import consts, db, usage, utils
from xklb.utils import log


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="library merge-online-local", usage=usage.merge_online_local)
    parser.add_argument("database")
    parser.add_argument("--limit", "-L", "-l", "-queue", "--queue", default=100)
    parser.add_argument("--verbose", "-v", action="count", default=0)
    args = parser.parse_args()
    args.db = db.connect(args)
    log.info(utils.dict_filter_bool(args.__dict__))
    return args


def get_duplicates(args) -> List[dict]:
    query = """
    WITH m1 as (
        SELECT
            *
        FROM
            media
        WHERE 1=1
            and id is not null
            and id != ""
            and ie_key != 'Local'
            and time_deleted = 0
    )
    SELECT
        m2.path keep_path
        , m1.path duplicate_path
        , m1.title
    FROM m1, (
        SELECT
            rowid,
            *
        FROM
            media
        WHERE 1=1
            and time_deleted = 0
            and id is null
            and title is null
    ) m2
    JOIN media_fts on m2.rowid = media_fts.rowid
    WHERE m2.ie_key = 'Local'
        AND m1.ie_key NOT IN ('NBCStations', 'TedTalk', 'ThisAmericanLife', 'InfoQ', 'NFB', 'KickStarter')
        AND media_fts.path MATCH '"'||m1.tube_id||'"'
        AND m2.PATH LIKE '%['||m1.tube_id||']%'
    ORDER BY 1=1
        , length(m2.path)-length(REPLACE(m2.path, '/', '')) desc
        , length(m2.path)-length(REPLACE(m2.path, '.', ''))
        , length(m2.path)
        , m2.time_modified desc
        , m2.time_created desc
        , m2.duration desc
        , m2.path desc
    """

    media = list(args.db.query(query))
    return media


def get_dict(args, path) -> Optional[dict]:
    known = list(args.db.query("select * from media where path=?", [path]))[0]
    return utils.dict_filter_bool(known, keep_0=False)


def merge_online_local() -> None:
    args = parse_args()
    args.db["media"].rebuild_fts()
    duplicates = get_duplicates(args)
    duplicates_count = len(duplicates)

    tbl = deepcopy(duplicates)
    tbl = tbl[: int(args.limit)]
    tbl = utils.col_resize(tbl, "keep_path", 30)
    tbl = utils.col_resize(tbl, "duplicate_path", 30)
    tbl = utils.col_naturalsize(tbl, "duplicate_size")
    print(tabulate(tbl, tablefmt="fancy_grid", headers="keys", showindex=False))

    print(f"{duplicates_count} duplicates found (showing first {args.limit})")
    if duplicates and utils.confirm("Merge duplicates?"):  # type: ignore
        log.info("Merging...")

        merged = []
        for d in duplicates:
            fspath = d["keep_path"]
            webpath = d["duplicate_path"]
            if webpath in merged or fspath == webpath:
                continue

            tube_entry = get_dict(args, webpath)
            fs_tags = get_dict(args, fspath)

            if not tube_entry or not fs_tags or tube_entry["tube_id"] not in fs_tags["path"]:
                continue

            if fs_tags["time_modified"] is None or fs_tags["time_modified"] == 0:
                fs_tags["time_modified"] = consts.now()
            if fs_tags["time_downloaded"] is None or fs_tags["time_downloaded"] == 0:
                fs_tags["time_downloaded"] = consts.APPLICATION_START

            entry = {**tube_entry, **fs_tags, "webpath": webpath}
            args.db["media"].insert(utils.dict_filter_bool(entry), pk="id", alter=True, replace=True)  # type: ignore
            args.db["media"].delete(webpath)
            merged.append(webpath)

        print(len(merged), "merged")


if __name__ == "__main__":
    merge_online_local()
