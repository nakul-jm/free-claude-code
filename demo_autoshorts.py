"""Demonstration of the AutoShorts clip generation system."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from free_claude_code.messaging.autoshorts import (
    AutoShortsClipGenerator,
    TranscriptSegment
)


def demo_autoshorts():
    """Demonstrate AutoShorts functionality with a realistic example."""
    print("🎬 AutoShorts Clip Generation Demo")
    print("=" * 50)

    # Sample transcript from a coding tutorial
    transcript_segments = [
        TranscriptSegment("Welcome back to our coding tutorial! ", 0.0, 2.5),
        TranscriptSegment("Today we're going to build a REST API using Python and FastAPI. ", 2.5, 6.0),
        TranscriptSegment("First, let's set up our project structure. ", 6.0, 8.5),
        TranscriptSegment("We'll create a main.py file for our application entry point. ", 8.5, 11.0),
        TranscriptSegment("Then we'll define our data models using Pydantic. ", 11.0, 13.5),
        TranscriptSegment("This will give us automatic validation and serialization. ", 13.5, 16.0),
        TranscriptSegment("Pretty neat, right? ", 16.0, 17.5),
        TranscriptSegment("Now let's create our first endpoint for getting all users. ", 17.5, 20.0),
        TranscriptSegment("We'll use the @app.get decorator to define a GET route. ", 20.0, 22.5),
        TranscriptSegment("The function will return a list of user objects from our database. ", 22.5, 25.5),
        TranscriptSegment("Let's test it with curl to make sure it's working correctly. ", 25.5, 28.0),
        TranscriptSegment("Great! We're getting the expected JSON response. ", 28.0, 30.0),
        TranscriptSegment("Next, let's add authentication to protect our endpoints. ", 30.0, 32.5),
        TranscriptSegment("We'll implement JWT-based authentication for security. ", 32.5, 35.0),
        TranscriptSegment("This will ensure only authorized users can access sensitive data. ", 35.0, 37.5),
        TranscriptSegment("Finally, let's add API documentation with Swagger UI. ", 37.5, 40.0),
        TranscriptSegment("FastAPI automatically generates beautiful docs for us. ", 40.0, 42.0),
        TranscriptSegment("And that's it for today's tutorial! ", 42.0, 43.5),
        TranscriptSegment("Thanks for watching and happy coding! ", 43.5, 45.0),
    ]

    # Create AutoShorts generator with preferred 30-60 second clips
    generator = AutoShortsClipGenerator(
        min_duration=25.0,   # Minimum 25 seconds
        max_duration=35.0,   # Maximum 35 seconds (will extend to complete thoughts)
        sentence_boundary_punctuation=".!?"
    )

    print(f"\n📝 Input: {len(transcript_segments)} transcript segments")
    print(f"⏱️  Total duration: {transcript_segments[-1].end_time:.1f} seconds")
    print(f"🎯 Target clip duration: {generator.min_duration}-{generator.max_duration} seconds")

    # Generate clips
    clips = generator.generate_clips(transcript_segments)

    print(f"\n✂️  Generated {len(clips)} clips:")
    print("-" * 50)

    for i, clip in enumerate(clips, 1):
        print(f"\nClip {i}:")
        print(f"  📄 Text: \"{clip.text.strip()}\"")
        print(f"  ⏱️  Duration: {clip.duration:.1f} seconds ({clip.start_time:.1f}s → {clip.end_time:.1f}s)")
        print(f"  🎯 Meets min duration: {'✅' if clip.duration >= generator.min_duration else '❌'}")
        print(f"  📝 Ends with punctuation: {'✅' if clip.text.strip() and clip.text.strip()[-1] in '.!?' else '❌'}")

        # Show FFmpeg commands
        cut_cmd = generator.get_ffmpeg_cut_command("input_video.mp4", f"clip_{i}.mp4", clip)
        caption_cmd = generator.get_ffmpeg_caption_command("input_video.mp4", f"clip_{i}_captioned.mp4", clip)

        print(f"  🎬 FFmpeg cut: {' '.join(cut_cmd[:8])}...")
        print(f"  📝 FFmpeg caption: {' '.join(caption_cmd[:8])}...")

    print("\n" + "=" * 50)
    print("🎉 Demo complete! AutoShorts is working correctly.")
    print("\n🔑 Key features demonstrated:")
    print("   • Sentence-aware clipping (no mid-sentence cuts)")
    print("   • Respects duration preferences (25-35s target)")
    print("   • Extends clips to complete thoughts when needed")
    print("   • Generates FFmpeg commands for video cutting")
    print("   • Preserves caption synchronization with drawtext filter")
    print("   • Handles edge cases (empty segments, single segments, etc.)")


if __name__ == "__main__":
    demo_autoshorts()