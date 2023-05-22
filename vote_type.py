from enum import Enum
from pathlib import Path


class VoteType(Enum):
    """
    Enum for vote types.
    Assuming 'vote_type' 1 is support and 'vote_type' 2 is oppose.
    """

    SUPPORT = "1"
    OPPOSE = "2"
