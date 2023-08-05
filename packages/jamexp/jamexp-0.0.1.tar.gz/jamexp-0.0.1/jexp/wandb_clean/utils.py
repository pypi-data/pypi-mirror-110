import datetime
import os.path as osp
import shutil

from loguru import logger

TIME_PARTTERN = "%Y-%m-%dT%H:%M:%S"


def extract_time(run):
    """extract run info

    :param run: [description]
    :type run: [type]
    :return: duration, run2now
    :rtype: datetime.timedelta
    """
    create_time_str = run.createdAt
    last_time_str = run.heartbeatAt
    start_time = datetime.datetime.strptime(create_time_str, TIME_PARTTERN)
    end_time = datetime.datetime.strptime(last_time_str, TIME_PARTTERN)
    now_time = datetime.datetime.now()
    duration = end_time - start_time
    run2now = now_time - end_time
    return duration, run2now


def delete_run(run, delete=True):
    delete_info = f"{run.name}\t{run.url}"
    cfg = run.config
    if "hyd_path" in cfg:
        if osp.exists(cfg["hyd_path"]):
            if delete:
                shutil.rmtree(cfg["hyd_path"], ignore_errors=True)
            delete_info += f"\n\t{cfg['hyd_path']}"
    logger.info(delete_info)
    if delete:
        run.delete()
