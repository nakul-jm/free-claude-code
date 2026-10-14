"""AutoShorts clip generation system for creating meaningful video clips from transcripts."""

from .clip_generator import (
    AutoShortsClipGenerator,
    TranscriptSegment,
    ClipResult,
    create_default_clip_generator
)

__all__ = [
    "AutoShortsClipGenerator",
    "TranscriptSegment",
    "ClipResult",
    "create_default_clip_generator"
]