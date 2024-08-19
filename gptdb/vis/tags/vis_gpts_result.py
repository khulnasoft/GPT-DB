"""Visualize the result of the GPTBbs flow."""

from ..base import Vis


class VisGptdbsFlowResult(Vis):
    """Protocol for visualizing the result of the GPTBbs flow."""

    @classmethod
    def vis_tag(cls) -> str:
        """Return the tag name of the vis protocol module."""
        return "gptdbs-result"
