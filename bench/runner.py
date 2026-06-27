"""评估流程编排 — 串联模型调用、评分、报告生成。"""

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from bench.models import ModelClient
from bench.evaluator import evaluate, EvalResult
from challenges.base import Challenge

console = Console()


def run_benchmark(
    clients: list[ModelClient],
    challenges: list[Challenge],
    runs_per_challenge: int = 1,
) -> dict[str, list[EvalResult]]:
    """
    运行完整评估流程。

    Returns:
        {model_name: [EvalResult, ...]}
    """
    results: dict[str, list[EvalResult]] = {c.name: [] for c in clients}

    total_tasks = len(clients) * len(challenges) * runs_per_challenge

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("评估中...", total=total_tasks)

        for client in clients:
            for challenge in challenges:
                for run_idx in range(runs_per_challenge):
                    run_label = f" (run {run_idx + 1})" if runs_per_challenge > 1 else ""
                    progress.update(
                        task,
                        description=f"[cyan]{client.name}[/] → "
                        f"[yellow]{challenge.name}[/]{run_label}",
                    )

                    try:
                        prompt = challenge.build_prompt()
                        raw_code = client.generate_code(prompt)
                        result = evaluate(challenge, raw_code)
                        results[client.name].append(result)
                    except Exception as e:
                        results[client.name].append(
                            EvalResult(
                                challenge_name=challenge.name,
                                passed=0,
                                total=len(challenge.test_cases),
                                correctness=0,
                                quality=0,
                                score=0,
                                code="",
                                error=str(e),
                            )
                        )

                    progress.advance(task)

    return results


def print_summary(results: dict[str, list[EvalResult]]):
    """在终端打印评估摘要。"""
    table = Table(title="📊 AI Code Bench 评估结果", show_lines=True)
    table.add_column("模型", style="cyan", no_wrap=True)
    table.add_column("总分", justify="right", style="bold")
    table.add_column("正确性", justify="right")
    table.add_column("代码质量", justify="right")
    table.add_column("通过率", justify="right")

    # 按总分排序
    model_scores = []
    for model_name, evals in results.items():
        if not evals:
            continue
        avg_score = sum(e.score for e in evals) / len(evals)
        avg_correctness = sum(e.correctness for e in evals) / len(evals)
        avg_quality = sum(e.quality for e in evals) / len(evals)
        total_passed = sum(e.passed for e in evals)
        total_cases = sum(e.total for e in evals)
        model_scores.append((model_name, avg_score, avg_correctness, avg_quality, total_passed, total_cases))

    model_scores.sort(key=lambda x: x[1], reverse=True)

    for rank, (name, score, corr, qual, passed, total) in enumerate(model_scores, 1):
        table.add_row(
            f"#{rank} {name}",
            f"{score:.1f}",
            f"{corr:.1f}",
            f"{qual:.1f}",
            f"{passed}/{total}",
        )

    console.print()
    console.print(table)
    console.print()
