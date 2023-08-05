import os

from .filters import if_notag, if_stale
from .utils import delete_run

WANDB_USER = os.environ["WANDB_ENTITY"] or False
WANDB_KEY = os.environ["WANDB_API_KEY"] or False
WANDB_AVAIL = WANDB_USER and WANDB_KEY
