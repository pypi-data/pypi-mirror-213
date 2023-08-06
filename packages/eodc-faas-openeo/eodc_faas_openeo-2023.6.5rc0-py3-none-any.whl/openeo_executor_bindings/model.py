import logging
from pathlib import Path

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class OpenEOExecutorParameters(BaseModel):
    """Pydantic model of parameters required to run openeo job."""

    process_graph: dict
    user_workspace: Path
