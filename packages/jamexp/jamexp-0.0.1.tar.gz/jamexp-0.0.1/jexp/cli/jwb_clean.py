import typer
import wandb

from jexp.wandb_clean import WANDB_AVAIL, WANDB_USER, delete_run, if_notag, if_stale


def clean_project(
    proj: str,
    name: str = typer.Option(None, "-n", help="run name"),
    is_delete: bool = typer.Option(False, "--d", help="delete runs"),
):
    if not WANDB_AVAIL:
        print("WANDB NON AVAIL, please set environment")
        exit(1)
    api = wandb.Api()
    runs = api.runs(f"{WANDB_USER}/{proj}")
    for run in runs:
        if if_stale(run) or if_notag(run):
            delete_run(run, is_delete)
        elif name is not None and name in run.name:
            delete_run(run, is_delete)


def main():
    typer.run(clean_project)
