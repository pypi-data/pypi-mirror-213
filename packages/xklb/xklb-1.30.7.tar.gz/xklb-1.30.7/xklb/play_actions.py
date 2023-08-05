import argparse, shlex, shutil, sys, time
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from random import random
from typing import Dict, Tuple

from xklb import consts, db, player, subtitle, tube_backend, usage, utils
from xklb.consts import SC
from xklb.playback import now_playing
from xklb.player import mark_media_deleted, override_sort
from xklb.scripts.bigdirs import process_bigdirs
from xklb.utils import cmd_interactive, log, random_filename, safe_unpack


def parse_args_sort(args) -> None:
    if args.sort:
        args.sort = " ".join(args.sort)
    elif not args.sort and hasattr(args, "defaults"):
        args.defaults.append("sort")

    m_columns = args.db["media"].columns_dict

    # switching between videos with and without subs is annoying
    subtitle_count = "=0"
    if random() < getattr(args, "subtitle_mix", consts.DEFAULT_SUBTITLE_MIX):
        # bias slightly toward videos without subtitles
        subtitle_count = ">0"

    sorts = [
        "random" if getattr(args, "random", False) else None,
        "rank" if args.sort and "rank" in args.sort else None,
        "video_count > 0 desc" if "video_count" in m_columns and args.action == SC.watch else None,
        "audio_count > 0 desc" if "audio_count" in m_columns else None,
        "time_downloaded > 0 desc"
        if "time_downloaded" in m_columns and "time_downloaded" not in " ".join(sys.argv)
        else None,
        'm.path like "http%"',
        "width < height desc" if "width" in m_columns and hasattr(args, "portrait") and args.portrait else None,
        f"subtitle_count {subtitle_count} desc"
        if "subtitle_count" in m_columns
        and args.action == SC.watch
        and not any(
            [
                args.print,
                consts.PYTEST_RUNNING,
                "subtitle_count" in args.where,
                args.limit != consts.DEFAULT_PLAY_QUEUE,
            ],
        )
        else None,
        args.sort,
        "duration desc" if args.action in (SC.listen, SC.watch) and args.include else None,
        "size desc" if args.action in (SC.listen, SC.watch) and args.include else None,
        "play_count" if args.action in (SC.listen, SC.watch) and "play_count" in m_columns else None,
        "size desc, duration"
        if args.action in (SC.listen, SC.watch) and "size" in m_columns and "duration" in m_columns
        else None,
        "sparseness" if args.action == SC.filesystem else None,
        "size" if args.action == SC.filesystem else None,
        "m.path",
        "random",
    ]

    sort = list(filter(bool, sorts))
    sort = [override_sort(s) for s in sort]
    sort = "\n        , ".join(sort)
    args.sort = sort.replace(",,", ",")


def parse_args(action, default_chromecast=None) -> argparse.Namespace:
    DEFAULT_PLAYER_ARGS_SUB = ["--speed=1"]
    DEFAULT_PLAYER_ARGS_NO_SUB = ["--speed=1.46"]

    parser = argparse.ArgumentParser(prog="library " + action, usage=usage.play(action))

    parser.add_argument("--sort", "-u", nargs="+", help=argparse.SUPPRESS)
    parser.add_argument("--random", "-r", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--big-dirs", "-B", action="count", default=0, help=argparse.SUPPRESS)
    parser.add_argument("--related", "-R", action="count", default=0, help=argparse.SUPPRESS)
    parser.add_argument("--cluster", "-C", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--play-in-order", "-O", action="count", default=0, help=argparse.SUPPRESS)

    parser.add_argument("--where", "-w", nargs="+", action="extend", default=[], help=argparse.SUPPRESS)
    parser.add_argument("--include", "-s", nargs="+", action="extend", default=[], help=argparse.SUPPRESS)
    parser.add_argument("--exclude", "-E", "-e", nargs="+", action="extend", default=[], help=argparse.SUPPRESS)
    parser.add_argument("--no-fts", action="store_true")

    parser.add_argument("--created-within", help=argparse.SUPPRESS)
    parser.add_argument("--created-before", help=argparse.SUPPRESS)
    parser.add_argument("--changed-within", "--modified-within", help=argparse.SUPPRESS)
    parser.add_argument("--changed-before", "--modified-before", help=argparse.SUPPRESS)
    parser.add_argument("--played-within", help=argparse.SUPPRESS)
    parser.add_argument("--played-before", help=argparse.SUPPRESS)
    parser.add_argument("--deleted-within", help=argparse.SUPPRESS)
    parser.add_argument("--deleted-before", help=argparse.SUPPRESS)

    parser.add_argument(
        "--chromecast-device",
        "--cast-to",
        "-t",
        default=default_chromecast or "",
        help=argparse.SUPPRESS,
    )
    parser.add_argument("--chromecast", "--cast", "-c", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--cast-with-local", "-wl", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--loop", action="store_true", help=argparse.SUPPRESS)

    parser.add_argument("--interdimensional-cable", "-4dtv", type=int, help=argparse.SUPPRESS)
    parser.add_argument(
        "--multiple-playback",
        "-m",
        default=False,
        nargs="?",
        const=consts.DEFAULT_MULTIPLE_PLAYBACK,
        type=int,
        help=argparse.SUPPRESS,
    )
    parser.add_argument("--screen-name", help=argparse.SUPPRESS)
    parser.add_argument("--crop", "--zoom", "--stretch", "--fit", "--fill", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--hstack", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--vstack", action="store_true", help=argparse.SUPPRESS)

    parser.add_argument("--portrait", "-portrait", action="store_true", help=argparse.SUPPRESS)

    parser.add_argument("--duration", "-d", action="append", help=argparse.SUPPRESS)
    parser.add_argument("--size", "-S", action="append", help=argparse.SUPPRESS)
    parser.add_argument("--duration-from-size", action="append", help=argparse.SUPPRESS)

    parser.add_argument("--print", "-p", default=False, const="p", nargs="?", help=argparse.SUPPRESS)
    parser.add_argument("--moved", nargs=2, help=argparse.SUPPRESS)

    parser.add_argument("--cols", "-cols", "-col", nargs="*", help=argparse.SUPPRESS)
    parser.add_argument("--limit", "-L", "-l", "-queue", "--queue", help=argparse.SUPPRESS)
    parser.add_argument("--skip", "--offset", help=argparse.SUPPRESS)
    parser.add_argument(
        "--partial",
        "-P",
        "--previous",
        "--recent",
        default=False,
        const="n",
        nargs="?",
        help=argparse.SUPPRESS,
    )

    parser.add_argument("--start", "-vs", help=argparse.SUPPRESS)
    parser.add_argument("--end", "-ve", help=argparse.SUPPRESS)
    parser.add_argument("--mpv-socket", default=consts.DEFAULT_MPV_SOCKET, help=argparse.SUPPRESS)
    parser.add_argument("--watch-later-directory", default=consts.DEFAULT_MPV_WATCH_LATER, help=argparse.SUPPRESS)
    parser.add_argument("--subtitle-mix", default=consts.DEFAULT_SUBTITLE_MIX, help=argparse.SUPPRESS)

    parser.add_argument("--override-player", "--player", "-player", help=argparse.SUPPRESS)
    parser.add_argument("--player-args-sub", "-player-sub", nargs="*", default=DEFAULT_PLAYER_ARGS_SUB)
    parser.add_argument("--player-args-no-sub", "-player-no-sub", nargs="*", default=DEFAULT_PLAYER_ARGS_NO_SUB)
    parser.add_argument("--transcode", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--transcode-audio", action="store_true", help=argparse.SUPPRESS)

    parser.add_argument("--post-action", "--action", "-k", default="keep", help=argparse.SUPPRESS)
    parser.add_argument("--keep-dir", "--keepdir", default="keep", help=argparse.SUPPRESS)
    parser.add_argument("--keep-cmd", "--keepcmd", help=argparse.SUPPRESS)
    parser.add_argument("--gui", action="store_true")
    parser.add_argument("--shallow-organize", default="/mnt/d/", help=argparse.SUPPRESS)

    parser.add_argument("--online-media-only", "--online-only", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--local-media-only", "--local-only", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--safe", "-safe", action="store_true", help="Skip generic URLs")

    parser.add_argument("--sibling", "--episode", action="store_true")
    parser.add_argument("--solo", action="store_true")

    parser.add_argument("--sort-by")
    parser.add_argument("--depth", "-D", default=0, type=int, help="Depth of folders")
    parser.add_argument("--lower", type=int, help="Number of files per folder lower limit")
    parser.add_argument("--upper", type=int, help="Number of files per folder upper limit")

    parser.add_argument("--prefetch", type=int, default=1)
    parser.add_argument("--prefix", default="", help=argparse.SUPPRESS)
    parser.add_argument(
        "--folder",
        action="store_true",
        help="Experimental escape hatch to open folder; breaks a lot of features like post-actions",
    )
    parser.add_argument(
        "--folder-glob",
        "--folderglob",
        type=int,
        default=False,
        const=10,
        nargs="?",
        help="Experimental escape hatch to open a folder glob limited to x number of files; breaks a lot of features like post-actions",
    )

    parser.add_argument("--timeout", "-T", help="Quit after x minutes")
    parser.add_argument("--db", "-db", help="Override the positional argument database location")
    parser.add_argument("--ignore-errors", "--ignoreerrors", "-i", action="store_true")
    parser.add_argument("--verbose", "-v", action="count", default=0)

    parser.add_argument("database")
    parser.add_argument("search", nargs="*")
    args = parser.parse_intermixed_args()
    args.action = action
    args.defaults = []

    args.include += args.search
    if args.include == ["."]:
        args.include = [str(Path().cwd().resolve())]

    if args.db:
        args.database = args.db
    args.db = db.connect(args)

    if args.big_dirs:
        args.local_media_only = True

    if not args.limit:
        args.defaults.append("limit")
        if not any([args.print and len(args.print.replace("p", "")) > 0, args.partial, args.lower, args.upper]):
            if args.action in (SC.listen, SC.watch, SC.read):
                args.limit = consts.DEFAULT_PLAY_QUEUE
            elif args.action in (SC.view):
                args.limit = consts.DEFAULT_PLAY_QUEUE * 4
    elif args.limit in ("inf", "all"):
        args.limit = None

    parse_args_sort(args)

    if args.cols:
        args.cols = list(utils.flatten([s.split(",") for s in args.cols]))

    if args.duration:
        args.duration = utils.parse_human_to_sql(utils.human_to_seconds, "duration", args.duration)

    if args.size:
        args.size = utils.parse_human_to_sql(utils.human_to_bytes, "size", args.size)

    if args.duration_from_size:
        args.duration_from_size = utils.parse_human_to_sql(utils.human_to_bytes, "size", args.duration_from_size)

    if args.chromecast:
        from catt.api import CattDevice

        args.cc = CattDevice(args.chromecast_device, lazy=True)
        args.cc_ip = utils.get_ip_of_chromecast(args.chromecast_device)

    if args.override_player:
        args.override_player = shlex.split(args.override_player)

    log.info(utils.dict_filter_bool(args.__dict__))

    if args.keep_dir:
        args.keep_dir = Path(args.keep_dir).expanduser().resolve()

    if args.solo:
        args.upper = 1
    if args.sibling:
        args.lower = 2

    if args.post_action:
        args.post_action = args.post_action.replace("-", "_")

    utils.timeout(args.timeout)

    args.sock = None
    return args


def construct_query(args) -> Tuple[str, dict]:
    m_columns = args.db["media"].columns_dict
    args.filter_sql = []
    args.filter_bindings = {}

    if args.duration:
        args.filter_sql.append(" and duration IS NOT NULL " + args.duration)
    if args.size:
        args.filter_sql.append(" and size IS NOT NULL " + args.size)
    if args.duration_from_size:
        args.filter_sql.append(
            " and size IS NOT NULL and duration in (select distinct duration from m where 1=1 "
            + args.duration_from_size
            + ")",
        )

    args.filter_sql.extend([" and " + w for w in args.where])

    def ii(string):
        if string.isdigit():
            return string + " minutes"
        return string.replace("mins", "minutes").replace("secs", "seconds")

    if args.created_within:
        args.filter_sql.append(
            f"and time_created > cast(STRFTIME('%s', datetime( 'now', '-{ii(args.created_within)}')) as int)",
        )
    if args.created_before:
        args.filter_sql.append(
            f"and time_created < cast(STRFTIME('%s', datetime( 'now', '-{ii(args.created_before)}')) as int)",
        )
    if args.changed_within:
        args.filter_sql.append(
            f"and time_modified > cast(STRFTIME('%s', datetime( 'now', '-{ii(args.changed_within)}')) as int)",
        )
    if args.changed_before:
        args.filter_sql.append(
            f"and time_modified < cast(STRFTIME('%s', datetime( 'now', '-{ii(args.changed_before)}')) as int)",
        )
    if args.played_within:
        args.filter_sql.append(
            f"and time_played > cast(STRFTIME('%s', datetime( 'now', '-{ii(args.played_within)}')) as int)",
        )
    if args.played_before:
        args.filter_sql.append(
            f"and time_played < cast(STRFTIME('%s', datetime( 'now', '-{ii(args.played_before)}')) as int)",
        )
    if args.deleted_within:
        args.filter_sql.append(
            f"and time_deleted > cast(STRFTIME('%s', datetime( 'now', '-{ii(args.deleted_within)}')) as int)",
        )
    if args.deleted_before:
        args.filter_sql.append(
            f"and time_deleted < cast(STRFTIME('%s', datetime( 'now', '-{ii(args.deleted_before)}')) as int)",
        )

    args.table = "media"
    if args.db["media"].detect_fts() and not args.no_fts:
        if args.include:
            args.table = db.fts_flexible_search(args)
            m_columns = {**m_columns, "rank": int}
        elif args.exclude:
            db.construct_search_bindings(args, m_columns)
    else:
        db.construct_search_bindings(args, m_columns)

    if args.table == "media" and not any(
        [
            args.filter_sql,
            args.where,
            args.print,
            args.partial,
            args.lower,
            args.upper,
            args.limit not in args.defaults,
            args.duration_from_size,
        ],
    ):
        limit = 60_000
        if args.random:
            limit = consts.DEFAULT_PLAY_QUEUE * 16

        where_not_deleted = (
            "where COALESCE(time_deleted,0) = 0"
            if "time_deleted" in m_columns and "time_deleted" not in " ".join(sys.argv)
            else ""
        )
        args.filter_sql.append(
            f"and m.rowid in (select rowid from media {where_not_deleted} order by random() limit {limit})",
        )

    cols = args.cols or ["path", "title", "duration", "size", "subtitle_count", "is_dir", "rank"]
    args.select = [c for c in cols if c in m_columns or c in ["*"]]
    if args.action == SC.read and "tags" in m_columns:
        args.select += "cast(length(tags) / 4.2 / 220 * 60 as INT) + 10 duration"
    args.select_sql = "\n        , ".join(args.select)
    args.limit_sql = "LIMIT " + str(args.limit) if args.limit else ""
    args.offset_sql = f"OFFSET {args.skip}" if args.skip and args.limit else ""
    query = f"""WITH m as (
    SELECT rowid, * FROM {args.table}
    WHERE 1=1
        {player.filter_args_sql(args, m_columns)}
    )
    SELECT
        {args.select_sql}
    FROM m
    WHERE 1=1
        {" ".join(args.filter_sql)}
    ORDER BY 1=1
        , {args.sort}
    {args.limit_sql} {args.offset_sql}
    """

    args.filter_sql = [
        s for s in args.filter_sql if "rowid" not in s
    ]  # only use random rowid constraint in first query

    return query, args.filter_bindings


def chromecast_play(args, m) -> None:
    if args.action in (SC.watch):
        catt_log = player.watch_chromecast(args, m, subtitles_file=safe_unpack(subtitle.get_subtitle_paths(m["path"])))
    elif args.action in (SC.listen):
        catt_log = player.listen_chromecast(args, m)
    else:
        raise NotImplementedError

    if catt_log:
        if catt_log.stderr is None or catt_log.stderr == "":
            if not args.cast_with_local:
                raise RuntimeError("catt does not exit nonzero? but something might have gone wrong")
        elif "Heartbeat timeout, resetting connection" in catt_log.stderr:
            raise RuntimeError("Media is possibly partially unwatched")


def transcode(args, path) -> str:
    log.debug(path)
    sub_index = subtitle.get_sub_index(args, path)

    transcode_dest = str(Path(path).with_suffix(".mkv"))
    temp_video = random_filename(transcode_dest)

    maps = ["-map", "0"]
    if sub_index:
        maps = ["-map", "0:v", "-map", "0:a", "-map", "0:" + str(sub_index), "-scodec", "webvtt"]

    video_settings = [
        "-vcodec",
        "h264",
        "-preset",
        "fast",
        "-profile:v",
        "high",
        "-level",
        "4.1",
        "-crf",
        "17",
        "-pix_fmt",
        "yuv420p",
    ]
    if args.transcode_audio:
        video_settings = ["-c:v", "copy"]

    print("Transcoding", temp_video)
    cmd_interactive(
        "ffmpeg",
        "-nostdin",
        "-loglevel",
        "error",
        "-stats",
        "-i",
        path,
        *maps,
        *video_settings,
        "-acodec",
        "libopus",
        "-ac",
        "2",
        "-b:a",
        "128k",
        "-filter:a",
        "loudnorm=i=-18:lra=17",
        temp_video,
    )

    Path(path).unlink()
    shutil.move(temp_video, transcode_dest)
    with args.db.conn:
        args.db.conn.execute("UPDATE media SET path = ? where path = ?", [transcode_dest, path])
    return transcode_dest


def prep_media(args, m: Dict, ignore_paths):
    t = utils.Timer()
    args.db = db.connect(args)
    log.debug("db.connect: %s", t.elapsed())

    if (args.play_in_order >= consts.SIMILAR) or (args.action == SC.listen and "audiobook" in m["path"].lower()):
        m = player.get_ordinal_media(args, m, ignore_paths)
        log.debug("player.get_ordinal_media: %s", t.elapsed())

    m["original_path"] = m["path"]
    if not m["path"].startswith("http"):
        media_path = Path(args.prefix + m["path"]).resolve() if args.prefix else Path(m["path"])
        m["path"] = str(media_path)

        if not media_path.exists():
            log.debug("media_path exists: %s", t.elapsed())
            log.warning("[%s]: Does not exist. Skipping...", m["path"])
            mark_media_deleted(args, m["original_path"])
            log.debug("mark_media_deleted: %s", t.elapsed())
            return None

        if args.transcode or args.transcode_audio:
            m["path"] = m["original_path"] = transcode(args, m["path"])
            log.debug("transcode: %s", t.elapsed())

    m["now_playing"] = now_playing(m["path"])

    return m


def save_playhead(args, m, start_time):
    m_columns = args.db["media"].columns_dict
    if "playhead" in m_columns:
        playhead = utils.get_playhead(
            args,
            m["original_path"],
            start_time,
            existing_playhead=m.get("playhead"),
            media_duration=m.get("duration"),
        )
        if playhead:
            player.set_playhead(args, m["original_path"], playhead)


def play(args, m) -> None:
    t = utils.Timer()
    print(m["now_playing"])
    log.debug("now_playing: %s", t.elapsed())

    args.player = player.parse(args, m)
    log.debug("player.parse: %s", t.elapsed())

    if args.interdimensional_cable:
        player.socket_play(args, m)
        return

    start_time = time.time()
    try:
        if args.chromecast:
            try:
                chromecast_play(args, m)
                t.reset()
                player.post_act(args, m["original_path"])
                log.debug("player.post_act: %s", t.elapsed())
            except Exception:
                if args.ignore_errors:
                    return
                else:
                    raise
        else:
            r = player.local_player(args, m)
            if r.returncode == 0:
                t.reset()
                player.post_act(args, m["original_path"])
                log.debug("player.post_act: %s", t.elapsed())
            else:
                log.warning("Player exited with code %s", r.returncode)
                if args.ignore_errors:
                    return
                else:
                    raise SystemExit(r.returncode)
    finally:
        save_playhead(args, m, start_time)


def process_playqueue(args) -> None:
    t = utils.Timer()
    query, bindings = construct_query(args)
    log.debug("construct_query: %s", t.elapsed())

    if args.print and not any(
        [
            args.partial,
            args.lower,
            args.upper,
            args.safe,
            args.play_in_order >= consts.SIMILAR,
            args.related >= consts.RELATED,
            args.cluster,
        ],
    ):
        player.printer(args, query, bindings)
        return

    media = list(args.db.query(query, bindings))
    log.debug("query: %s", t.elapsed())

    if args.partial and Path(args.watch_later_directory).exists():
        media = utils.mpv_enrich2(args, media)
        log.debug("utils.mpv_enrich2: %s", t.elapsed())

    if args.lower is not None or args.upper is not None:
        media = utils.filter_episodic(args, media)
        log.debug("utils.filter_episodic: %s", t.elapsed())

    if not media:
        utils.no_media_found()

    if all(
        [
            Path(args.watch_later_directory).exists(),
            args.play_in_order == 0,
            args.related == 0,
            not args.cluster,
            "sort" in args.defaults,
            not args.partial,
            not args.random,
        ],
    ):
        media = utils.mpv_enrich(args, media)
        log.debug("utils.mpv_enrich: %s", t.elapsed())

    if args.safe:
        media = [d for d in media if tube_backend.is_supported(d["path"]) or Path(d["path"]).exists()]
        log.debug("tube_backend.is_supported: %s", t.elapsed())

    if args.big_dirs:
        media_keyed = {d["path"]: d for d in media}
        dirs = process_bigdirs(args, media)
        dirs = list(reversed(list(d["path"] for d in dirs)))
        if "limit" in args.defaults:
            media = player.get_dir_media(args, dirs)
        else:
            media = [media_keyed[key] for dir in dirs for key in media_keyed.keys() if key.startswith(dir)]
        log.debug("big_dirs: %s", t.elapsed())

    if args.related >= consts.RELATED:
        media = player.get_related_media(args, media[0])
        log.debug("player.get_related_media: %s", t.elapsed())

    if args.cluster:
        media = utils.cluster_dicts(media)
        log.debug("cluster: %s", t.elapsed())

    if args.print:
        if args.play_in_order >= consts.SIMILAR:
            media = [player.get_ordinal_media(args, d) for d in media]
        player.media_printer(args, media)
    elif args.multiple_playback:
        args.gui = True
        player.multiple_player(args, media)
    else:
        try:
            mp_args = argparse.Namespace(**{k: v for k, v in args.__dict__.items() if k not in {"db"}})
            media.reverse()  # because media.pop()
            ignore_paths = []
            futures = deque()
            with ThreadPoolExecutor(max_workers=1) as executor:
                while media or futures:
                    while media and len(futures) < args.prefetch:
                        m = media.pop()
                        if m["path"] in ignore_paths:
                            continue
                        future = executor.submit(prep_media, mp_args, m, ignore_paths)
                        ignore_paths.append(m["path"])
                        futures.append(future)

                    if futures:
                        future = futures.popleft()
                        m = future.result()
                        if m is not None and (m["path"].startswith("http") or Path(m["path"]).exists()):
                            play(args, m)
        finally:
            if args.interdimensional_cable:
                args.sock.send(b"raw quit \n")
            Path(args.mpv_socket).unlink(missing_ok=True)
            if args.chromecast:
                Path(consts.CAST_NOW_PLAYING).unlink(missing_ok=True)


def watch() -> None:
    args = parse_args(SC.watch, default_chromecast="Living Room TV")
    process_playqueue(args)


def listen() -> None:
    args = parse_args(SC.listen, default_chromecast="Xylo and Orchestra")
    process_playqueue(args)


def filesystem() -> None:
    args = parse_args(SC.filesystem)
    process_playqueue(args)


def read() -> None:
    args = parse_args(SC.read)
    process_playqueue(args)


def view() -> None:
    args = parse_args(SC.view)
    process_playqueue(args)
