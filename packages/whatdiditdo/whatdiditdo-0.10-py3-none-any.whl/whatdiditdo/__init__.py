import os
import re
import tempfile
from typing import Union

from a_pandas_ex_df_to_string import pd_add_to_string
from getregdf import reg_query2df
from subprocesskiller import kill_subprocs

pd_add_to_string()
import numpy as np
from copytool import copyfile, conf
from flatten_everything import flatten_everything
from gethandledf import get_handle_list
from time import time
from list_all_files_recursively import get_folder_file_complete_path
import pandas as pd
from kthread_sleep import sleep
from touchtouch import touch
import psutil
from a_pandas_ex_fast_string import pd_add_fast_string

pd_add_fast_string()
from a_pandas_ex_apply_ignore_exceptions import pd_add_apply_ignore_exceptions

pd_add_apply_ignore_exceptions()
from a_pandas_ex_horizontal_explode import pd_add_horizontal_explode

pd_add_horizontal_explode()


def get_df_with_all_interessting_processes(
    partial_process_string, use_regex, pidlist=()
):
    df = get_handle_list(partial_process_string="")
    finpro = df.loc[
        df.Process.str.contains(partial_process_string, regex=use_regex, na=False)
    ]
    pidtochecks = list(flatten_everything(finpro.PID.unique().tolist()))
    allpids = pidtochecks + list(pidlist)
    allpids2 = []
    try:
        allpids2 = list(
            flatten_everything(
                [
                    [x.pid for x in psutil.Process(pidtocheck).children()]
                    for pidtocheck in allpids
                ]
            )
        )
    except psutil.NoSuchProcess as ba:
        print(ba)
        return -1
    except Exception:
        pass
    allpids = allpids + allpids2
    return df.loc[df.PID.isin(allpids)].reset_index(drop=True)


def get_tmpfile(suffix=".reg"):
    tfp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    filename = tfp.name
    filename = os.path.normpath(filename)
    tfp.close()
    touch(filename)
    return filename


def get_all_exe_files_from_folders(folders):
    fila = (
        "(?:"
        + "|".join(
            set(
                [
                    "(?:" + x.file + ")"
                    for x in get_folder_file_complete_path(folders)
                    if x.ext in [".exe", ".com"]
                ]
            )
        ).strip("|")
        + ")"
    )
    return fila


def filter_reg_keys(df, regex_reg_filter, mindepth=5):
    mindeothkey_list = [r"[^\\]+\\"] * mindepth
    mindeothkey = "^" + "".join(mindeothkey_list)[:-2]
    df2 = df.loc[
        (df.Type == "Key") & (df.Name.str.contains(mindeothkey, regex=True, na=False))
    ]
    for regexfil in regex_reg_filter:
        df2 = df2.loc[
            ~df2["Name"].str.contains(
                regexfil[1], na=False, regex=regexfil[0], flags=regexfil[2]
            )
        ]
    return df2


def get_complete_reg_df(df, regex_reg_filter, mindepth=3):
    tsta = time()
    dfregfilter = filter_reg_keys(df, regex_reg_filter, mindepth=mindepth)  # .copy()

    dfregfilter = dfregfilter.reset_index(drop=True)
    dfquery = reg_query2df(dfregfilter.Name.to_list())

    return dfregfilter.merge(dfquery, left_index=True, right_on="aa_id").assign(
        aa_time=tsta
    )


def filter_files(
    df,
    forbiddenfolders=(
        r"C:\program files (x86)",
        r"C:\programdata",
        r"C:\program files",
        os.path.normpath(os.environ.get("USERPROFILE")).lower(),
    ),
    exclude_folders_with_string=r"c:\\windows|nvidia",
):
    return df.loc[
        df.Type.str.contains("Directory|File", regex=True, na=False)
        & (~df.ShareFlags.str.contains(r"(?:---)|(?:^\s*$)", regex=True, na=False))
        & (~df.Name.str.lower().isin(forbiddenfolders))
        & (
            ~df.Name.str.lower().str.contains(
                exclude_folders_with_string, regex=True, na=False
            )
        )
    ]


def get_stats_from_files(list_or_series):
    if isinstance(list_or_series, list):
        list_or_series = pd.Series(list_or_series)
    filtervar = ""
    statdf = list_or_series.ds_apply_ignore(
        filtervar,
        lambda f: (
            ossta := os.stat(f),
            tuple(
                (x, getattr(ossta, x))
                for x in sorted(dir(ossta))
                if str(x).startswith("st_")
            ),
        )[1:],
    )
    statdf = statdf.ds_apply_ignore(
        pd.NA, lambda q: ("NAN", pd.NA) if isinstance(q, str) else q
    )

    statdfexploded = statdf.ds_horizontal_explode(
        0, concat=False
    ).ds_horizontal_explode("0_0", concat=False)
    statdf = pd.concat(
        [
            statdfexploded[co]
            .str[-1]
            .to_frame(
                statdfexploded[co]
                .str[0]
                .value_counts()
                .sort_values(ascending=False)
                .index[0]
            )
            for co in statdfexploded.columns
        ],
        axis=1,
    )
    dt = {
        "st_atime": np.dtype("float64"),
        "st_atime_ns": np.dtype("uint64"),
        "st_ctime": np.dtype("float64"),
        "st_ctime_ns": np.dtype("uint64"),
        "st_dev": np.dtype("uint32"),
        "st_file_attributes": np.dtype("uint32"),
        "st_gid": np.dtype("uint32"),
        "st_ino": np.dtype("uint64"),
        "st_mode": np.dtype("uint32"),
        "st_mtime": np.dtype("float64"),
        "st_mtime_ns": np.dtype("uint64"),
        "st_nlink": np.dtype("uint32"),
        "st_reparse_tag": np.dtype("uint32"),
        "st_size": np.dtype("uint32"),
        "st_uid": np.dtype("uint32"),
    }
    for key, item in dt.items():
        if key in statdf.columns:
            statdf[key] = statdf[key].astype(item)
    statdf.insert(0, "filepath", list_or_series)
    return statdf


def copy_files_from_df(dfstats, destfolder, sizelimit):
    dfstats["dest_path"] = dfstats.filepath.apply(
        lambda q: os.path.normpath(os.path.join(destfolder, q[3:]))
    )
    allsuccesscopies = []

    def copyfast(src, dst, size):
        nonlocal allsuccesscopies
        if src in allsuccesscopies:
            return True
        if size > sizelimit:
            return False
        try:
            if os.path.isfile(src):
                touch(dst)
                _ = copyfile(
                    src=src,
                    dst=dst,
                    copy_date=False,
                    copystat=False,
                    buffer=1000 * 1024,
                )
                if _:
                    allsuccesscopies.append(src)
                    return True
        except Exception as fa:
            print(fa)
            return False
        return False

    dfstats["copy_success"] = dfstats.apply(
        lambda q: copyfast(src=q.filepath, dst=q.dest_path, size=q.st_size), axis=1
    )
    return dfstats


def scan_processes(
    allexefiles: str,
    use_regex: bool,
    pidlist: tuple,
    regex_reg_filter: list[tuple[bool, str, Union[int, re.RegexFlag]]],
    mindepth: int,
    sizelimit_mb: int | float,
    forbiddenfolders: tuple[str, ...],
    exclude_folders_with_string: str,
    destfolder: str,
) -> tuple[pd.DataFrame | list, pd.DataFrame]:
    r"""
    Scans processes and performs various operations on them. - press CTRL+C when you want the observation to stop

    Args:
        allexefiles (str): A string representing the partial process name or regex pattern to match against process names.
        use_regex (bool): A boolean indicating whether to treat `allexefiles` as a regex pattern or a partial process name.
        pidlist (tuple): A tuple of process IDs to include in the scan.
        regex_reg_filter (list[tuple[bool, str, Union[int, re.RegexFlag]]]): A list of tuples representing regular expression filters for registry keys.
            Each tuple contains three elements:
                - A boolean indicating whether to include (True) or exclude (False) the matching keys.
                - A string representing the regular expression pattern to match against the registry keys.
                - An optional integer or `re.RegexFlag` value specifying additional flags for the regular expression pattern.
        mindepth (int): The minimum depth of registry keys to consider in the scan.
        sizelimit_mb (int, float): The size limit in megabytes for files to be copied.
        forbiddenfolders (tuple[str, ...]): A tuple of folder paths to exclude from the scan.
        exclude_folders_with_string (str): A string representing a regex pattern to exclude folders based on their paths.
        destfolder (str): The destination folder where the copied files will be stored.

    Returns:
        tuple[pd.DataFrame | list, pd.DataFrame]: A tuple containing the processed data.
            - `allregdfs` (pd.DataFrame | list): A pandas DataFrame or a list of DataFrames representing the registry data for all processes.
            - `allreadycopied` (pd.DataFrame): A pandas DataFrame containing information about the copied files.

    Raises:
        This function does not raise any specific exceptions, but it may raise general exceptions encountered during the process.

    """
    allreadycopied = pd.DataFrame(
        columns=[
            "filepath",
            "st_atime",
            "st_atime_ns",
            "st_ctime",
            "st_ctime_ns",
            "st_dev",
            "st_file_attributes",
            "st_gid",
            "st_ino",
            "st_mode",
            "st_mtime",
            "st_mtime_ns",
            "st_nlink",
            "st_reparse_tag",
            "st_size",
            "st_uid",
        ]
    )
    allregdfs = []
    itsover = False
    while not itsover:
        try:
            df = get_df_with_all_interessting_processes(
                partial_process_string=allexefiles, use_regex=use_regex, pidlist=pidlist
            )
            if isinstance(df, int):
                print(f"{allexefiles} Instance not found!")
                if allreadycopied.empty:
                    continue
                break
            else:
                print("found")

            dfreg = get_complete_reg_df(
                df,
                regex_reg_filter=regex_reg_filter,
                mindepth=mindepth,
            )
            allregdfs.append(dfreg)

            sizelimit_bytes = int(sizelimit_mb * 1024)
            dffilefilter = filter_files(
                df,
                forbiddenfolders=forbiddenfolders,
                exclude_folders_with_string=exclude_folders_with_string,
            ).reset_index(drop=True)

            dfstats = get_stats_from_files(dffilefilter.Name)

            copiedfiles = copy_files_from_df(
                dfstats,
                destfolder=os.path.normpath(
                    os.path.join(
                        destfolder, str(dfreg.aa_time.iloc[0]).replace(".", "_")
                    )
                ),
                sizelimit=sizelimit_bytes,
            )
            allreadycopied = pd.concat(
                [
                    allreadycopied,
                    copiedfiles.loc[copiedfiles.copy_success][copiedfiles.columns[:-2]],
                ],
                ignore_index=True,
            )
        except KeyboardInterrupt:
            while True:
                try:
                    kill_subprocs()
                    sleep(5)
                    itsover = True
                    break
                except:
                    continue
        except Exception as fa:
            print(fa)
            continue
    try:
        allregdfs = pd.concat(allregdfs, ignore_index=True)
    except Exception:
        pass
    return allregdfs, allreadycopied
