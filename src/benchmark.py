"""Compare models on GitHub Models: latency and output for a few sample texts.

Run: python benchmark.py [model ...]   (defaults to the "models" list in config.json)
"""
import sys
import time

from refiner import MODELS, PROMPT, get_client, refine

SAMPLES = [
    "sounds like a plan, take it directly with john on Mon so he can allocate time properly?",
    "I beleive this project will have a great impact cause we need it to improve productivity.",
    "The timing I referred to in my comparison is of the daily report email, its sent at 9 am every day",
]


def main(models):
    client = get_client()
    results = []
    for model in models:
        times = []
        for text in SAMPLES:
            start = time.perf_counter()
            try:
                output = refine(PROMPT.format(text), model, client=client)
            except Exception as error:  # report and continue with the next model
                print(f"FAIL {model}: {error}")
                break
            times.append(time.perf_counter() - start)
            print(f"[{model}] {times[-1]:.2f}s\n  in:  {text}\n  out: {output}\n")
        if times:
            results.append((sum(times) / len(times), model))

    print("\nAverage latency:")
    for avg, model in sorted(results):
        print(f"  {avg:6.2f}s  {model}")


if __name__ == "__main__":
    main(sys.argv[1:] or MODELS)
