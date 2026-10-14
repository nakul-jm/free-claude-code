"""Test cases for the AutoShorts clip generation system."""

from clip_generator import (
    AutoShortsClipGenerator,
    TranscriptSegment,
    ClipResult
)


def test_basic_clip_generation():
    """Test basic clip generation functionality."""
    # Create transcript segments
    segments = [
        TranscriptSegment("Hello world. ", 0.0, 2.0),
        TranscriptSegment("This is a test. ", 2.0, 5.0),
        TranscriptSegment("Another sentence here. ", 5.0, 8.0),
        TranscriptSegment("Final thought. ", 8.0, 10.0),
    ]

    generator = AutoShortsClipGenerator(min_duration=2.0, max_duration=5.0)
    clips = generator.generate_clips(segments)

    # Should generate clips respecting duration limits
    assert len(clips) > 0
    for clip in clips:
        assert clip.duration >= generator.min_duration
        assert clip.duration <= generator.max_duration * 1.5  # Allow some flexibility
        # Check that we don't cut in middle of sentences
        assert clip.text.strip() == "" or clip.text.strip()[-1] in ".!?"


def test_sentence_boundary_detection():
    """Test that clips end at sentence boundaries."""
    segments = [
        TranscriptSegment("First sentence. ", 0.0, 2.0),
        TranscriptSegment("Second sentence! ", 2.0, 4.0),
        TranscriptSegment("Third sentence? ", 4.0, 6.0),
        TranscriptSegment("Incomplete thought", 6.0, 8.0),
    ]

    generator = AutoShortsClipGenerator(min_duration=1.0, max_duration=5.0)
    clips = generator.generate_clips(segments)

    # Check that complete sentences end with proper punctuation
    for clip in clips[:-1]:  # All but possibly the last clip
        if clip.text.strip():
            assert clip.text.strip()[-1] in ".!?"


def test_minimum_duration():
    """Test that clips meet minimum duration requirements."""
    segments = [
        TranscriptSegment("Short. ", 0.0, 1.0),
        TranscriptSegment("Bit longer. ", 1.0, 3.0),
        TranscriptSegment("Getting there. ", 3.0, 6.0),
        TranscriptSegment("Now we have enough. ", 6.0, 10.0),
    ]

    generator = AutoShortsClipGenerator(min_duration=5.0, max_duration=10.0)
    clips = generator.generate_clips(segments)

    for clip in clips:
        assert clip.duration >= generator.min_duration


def test_ffmpeg_commands():
    """Test FFmpeg command generation."""
    segments = [
        TranscriptSegment("Test clip. ", 0.0, 5.0),
    ]

    generator = AutoShortsClipGenerator()
    clip_result = ClipResult("Test clip.", 0.0, 5.0, segments)

    # Test cut command
    cut_cmd = generator.get_ffmpeg_cut_command("input.mp4", "output.mp4", clip_result)
    assert "ffmpeg" in cut_cmd
    assert "-i" in cut_cmd
    assert "input.mp4" in cut_cmd
    assert "-ss" in cut_cmd
    assert "0.0" in cut_cmd
    assert "-t" in cut_cmd
    assert "5.0" in cut_cmd
    assert "output.mp4" in cut_cmd

    # Test caption command
    caption_cmd = generator.get_ffmpeg_caption_command("input.mp4", "output.mp4", clip_result)
    assert "ffmpeg" in caption_cmd
    assert "-i" in caption_cmd
    assert "input.mp4" in caption_cmd
    assert "-vf" in caption_cmd
    assert "drawtext" in caption_cmd[caption_cmd.index("-vf") + 1]
    assert "output.mp4" in caption_cmd


def test_empty_segments():
    """Test handling of empty segment list."""
    generator = AutoShortsClipGenerator()
    clips = generator.generate_clips([])
    assert clips == []


def test_single_segment():
    """Test handling of single segment."""
    segments = [TranscriptSegment("Single segment. ", 0.0, 3.0)]
    generator = AutoShortsClipGenerator(min_duration=2.0, max_duration=10.0)
    clips = generator.generate_clips(segments)

    assert len(clips) == 1
    assert clips[0].text.strip() == "Single segment."
    assert clips[0].duration == 3.0


if __name__ == "__main__":
    test_basic_clip_generation()
    test_sentence_boundary_detection()
    test_minimum_duration()
    test_ffmpeg_commands()
    test_empty_segments()
    test_single_segment()
    print("All tests passed!")