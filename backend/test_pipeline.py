import argparse
import json
import sys
from pathlib import Path

from ai_pipeline import (
    extract_intent,
    generate_grounded_response,
    synthesize_speech,
    transcribe_audio,
)
from matching import match_schemes


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the JanMitra local AI pipeline.")
    parser.add_argument(
        "--audio",
        default="sample_hindi.wav",
        help="Path to a Hindi WAV file (default: sample_hindi.wav)",
    )
    args = parser.parse_args()

    print("[1/4] Transcribing audio...")
    transcribed = transcribe_audio(args.audio)
    print(f'      Transcribed: "{transcribed}"')

    print("[2/4] Extracting intent...")
    profile = extract_intent(transcribed)
    print(f"      Intent: {json.dumps(profile, ensure_ascii=False)}")
    if profile["age"] is None:
        raise ValueError(
            "Age is required for matching / योजनाएं खोजने के लिए उम्र आवश्यक है।"
        )

    print("[3/4] Matching schemes...")
    schemes = match_schemes(
        profile["age"],
        profile["income_annual"],
        profile["gender"],
        profile["category"],
    )
    print(f"      Matched: {len(schemes)} schemes")

    print("[4/4] Generating Hindi response audio...")
    response_text = generate_grounded_response(transcribed, schemes)
    output_path = synthesize_speech(response_text, "output_response.mp3")
    output_file = Path(output_path)
    if not output_file.is_file() or output_file.stat().st_size == 0:
        raise RuntimeError(
            "Output audio was not created / आउटपुट ऑडियो नहीं बना।"
        )
    print(f'      Response: "{response_text}"')
    print(f"      Saved: {output_file.resolve()}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"Pipeline failed / पाइपलाइन विफल: {error}", file=sys.stderr)
        raise SystemExit(1) from error
