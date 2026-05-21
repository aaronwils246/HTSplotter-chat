"""
HTSplotter Chat Interface
=========================
Ask questions about your HTSplotter analysis results in plain English.

Usage:
    python chat_results.py [results_dir]

    results_dir: path to an output_results directory
                 (default: my_results/drugscreen_1timepoint/output_results)

Examples:
    Which drug was most potent?
    What is the IC50 for Prexasertib?
    How does BAY1895344 compare to MK-1775?
    What does the R² value tell me about the curve fit?
    Should I be worried about the warning at the top of the IC file?
"""

import os
import sys
import glob
import anthropic

# ── Defaults ──────────────────────────────────────────────────────────────────

DEFAULT_RESULTS_DIR = os.path.expanduser(
    "~/HTSplotter/my_results/drugscreen_1timepoint/output_results"
)

SYSTEM_INTRO = """\
You are a helpful bioinformatics assistant specialising in high-throughput drug \
screen analysis. The user has just run HTSplotter to analyse a drug screen and \
you have been given all of the text output files produced by the analysis. \
Your job is to answer questions about those results clearly and accurately.

Guidelines:
- Use the data files provided to give specific, quantitative answers wherever \
possible (quote IC values, R² statistics, etc.).
- When a value is 'nan', explain what that means in context (e.g. the curve \
did not reach that level of inhibition within the tested concentration range).
- Normalised confluency is expressed as a percentage relative to the vehicle \
control (100 % = no effect, 0 % = complete inhibition).
- Remind the user of the single-replicate caveat when drawing strong conclusions.
- Be concise but thorough.
"""

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_results(results_dir: str) -> str:
    """Read every .txt file in results_dir and return them joined as one string."""
    pattern = os.path.join(results_dir, "*.txt")
    txt_files = sorted(glob.glob(pattern))

    if not txt_files:
        raise FileNotFoundError(
            f"No .txt files found in: {results_dir}\n"
            "Run run_drugscreen.py first, or pass a different results directory."
        )

    sections = []
    for path in txt_files:
        filename = os.path.basename(path)
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            content = fh.read().strip()
        sections.append(f"=== {filename} ===\n{content}")

    return "\n\n".join(sections)


def build_system_messages(data_text: str) -> list[dict]:
    """
    Return the list of system prompt blocks.

    The static data block gets a cache_control marker so Anthropic will cache it
    across turns — you pay for the tokens once, not every message.
    """
    return [
        {"type": "text", "text": SYSTEM_INTRO},
        {
            "type": "text",
            "text": (
                "Below are the full text output files from the HTSplotter analysis. "
                "Use them to answer the user's questions.\n\n"
                + data_text
            ),
            "cache_control": {"type": "ephemeral"},   # cache the stable data block
        },
    ]


def stream_reply(client: anthropic.Anthropic,
                 system: list[dict],
                 history: list[dict]) -> str:
    """Stream one assistant reply and return the full text."""
    full_text = ""

    with client.messages.stream(
        model="claude-opus-4-7",
        max_tokens=2048,
        thinking={"type": "adaptive"},
        system=system,
        messages=history,
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_text += text

    print()   # newline after streamed response
    return full_text


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    results_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_RESULTS_DIR
    results_dir = os.path.expanduser(results_dir)

    # Load data once
    try:
        data_text = load_results(results_dir)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable is not set.")
        print("  export ANTHROPIC_API_KEY='sk-ant-...'")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    system  = build_system_messages(data_text)
    history: list[dict] = []

    print("\n" + "─" * 60)
    print("  HTSplotter Chat — ask questions about your results")
    print("  Type 'quit' or press Ctrl-C to exit")
    print("─" * 60 + "\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break

        history.append({"role": "user", "content": user_input})

        print("\nClaude: ", end="", flush=True)
        reply = stream_reply(client, system, history)
        print()

        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
