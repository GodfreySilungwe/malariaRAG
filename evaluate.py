"""Simple evaluation harness: measures latency and captures answers for a set of questions."""
import json
import time
from pathlib import Path
import malaria_rag


def run_eval(questions_file: str, output_file: str = "eval_results.json"):
    qs = json.loads(Path(questions_file).read_text(encoding="utf-8"))
    results = []
    latencies = []
    for q in qs:
        start = time.time()
        out = malaria_rag.answer_and_sources(q)
        dur = int((time.time() - start) * 1000)
        latencies.append(dur)
        results.append({"question": q, "answer": out.get("answer"), "latency_ms": out.get("latency_ms", dur), "sources": out.get("sources")})

    summary = {
        "count": len(results),
        "p50_ms": int(sorted(latencies)[len(latencies)//2]) if latencies else None,
        "p95_ms": int(sorted(latencies)[int(len(latencies)*0.95)]) if latencies else None,
    }

    final = {"summary": summary, "results": results}
    Path(output_file).write_text(json.dumps(final, indent=2), encoding="utf-8")
    print(f"Wrote evaluation results to {output_file}")


if __name__ == "__main__":
    run_eval("eval_questions.json")
