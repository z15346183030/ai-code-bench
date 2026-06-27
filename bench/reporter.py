"""报告生成 — 输出 Markdown 格式的评估报告。"""

import os
from datetime import datetime
from bench.evaluator import EvalResult


def generate_report(
    results: dict[str, list[EvalResult]],
    output_path: str = "results/report.md",
) -> str:
    """
    生成 Markdown 评估报告。

    Returns:
        报告文件路径
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    lines = []
    lines.append("# 🧪 AI Code Bench 评估报告\n")
    lines.append(f"**评估时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # ---- 总分排名 ----
    lines.append("## 📊 总分排名\n")
    lines.append("| 排名 | 模型 | 总分 | 正确性 | 代码质量 | 通过率 |")
    lines.append("|------|------|------|--------|----------|--------|")

    model_scores = []
    for model_name, evals in results.items():
        if not evals:
            continue
        avg_score = sum(e.score for e in evals) / len(evals)
        avg_corr = sum(e.correctness for e in evals) / len(evals)
        avg_qual = sum(e.quality for e in evals) / len(evals)
        total_passed = sum(e.passed for e in evals)
        total_cases = sum(e.total for e in evals)
        model_scores.append((model_name, avg_score, avg_corr, avg_qual, total_passed, total_cases))

    model_scores.sort(key=lambda x: x[1], reverse=True)

    for rank, (name, score, corr, qual, passed, total) in enumerate(model_scores, 1):
        lines.append(
            f"| {rank} | {name} | {score:.1f} | {corr:.1f} | {qual:.1f} | {passed}/{total} |"
        )

    # ---- 各题详情 ----
    lines.append("\n## 📝 各题详情\n")

    # 按题目聚合
    challenge_names = set()
    for evals in results.values():
        for e in evals:
            challenge_names.add(e.challenge_name)

    for cname in sorted(challenge_names):
        lines.append(f"### {cname}\n")
        lines.append("| 模型 | 得分 | 通过 | 代码质量 |")
        lines.append("|------|------|------|----------|")

        for model_name, evals in results.items():
            for e in evals:
                if e.challenge_name == cname:
                    status = "✅" if e.passed == e.total else f"⚠️ {e.passed}/{e.total}"
                    if e.error:
                        status = f"❌ {e.error[:30]}"
                    lines.append(
                        f"| {model_name} | {e.score:.1f} | {status} | {e.quality:.1f} |"
                    )

        lines.append("")

    # ---- 代码示例 ----
    lines.append("## 💻 代码示例\n")
    lines.append("以下展示各模型在 **two_sum** 题目上的生成代码：\n")

    for model_name, evals in results.items():
        for e in evals:
            if e.challenge_name == "two_sum" and e.code:
                lines.append(f"### {model_name}\n")
                lines.append("```python")
                lines.append(e.code.strip())
                lines.append("```\n")

    # 写入文件
    report_content = "\n".join(lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    return output_path
