#!/usr/bin/env python3
"""AI Code Bench — CLI 入口。"""

import argparse
import json
import os
import sys

from rich.console import Console

from bench.models import load_clients
from bench.runner import run_benchmark, print_summary
from bench.reporter import generate_report
from challenges import load_all, get_by_difficulty

console = Console()


def load_config(path: str = "config.json") -> dict:
    """加载配置文件。"""
    if not os.path.exists(path):
        console.print(f"[red]错误: 配置文件 {path} 不存在[/]")
        console.print(f"[yellow]请复制 config.example.json 为 config.json 并填入 API Key[/]")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_args():
    parser = argparse.ArgumentParser(
        description="AI Code Bench — AI 模型编程能力评估工具"
    )
    parser.add_argument(
        "--config", default="config.json", help="配置文件路径 (默认: config.json)"
    )
    parser.add_argument(
        "--models", default=None, help="指定模型，逗号分隔 (默认: 使用配置文件中所有模型)"
    )
    parser.add_argument(
        "--difficulty",
        default=None,
        choices=["easy", "medium", "hard"],
        help="只运行指定难度的题目",
    )
    parser.add_argument(
        "--output", default="results/report.md", help="报告输出路径 (默认: results/report.md)"
    )
    parser.add_argument(
        "--runs", type=int, default=1, help="每题运行次数 (默认: 1)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    console.print("[bold cyan]🧪 AI Code Bench[/] — AI 模型编程能力评估工具\n")

    # 加载配置
    config = load_config(args.config)

    # 加载模型
    clients = load_clients(config)
    if args.models:
        model_names = [n.strip() for n in args.models.split(",")]
        clients = [c for c in clients if c.name in model_names]

    if not clients:
        console.print("[red]错误: 没有可用的模型，请检查配置文件[/]")
        sys.exit(1)

    console.print(f"[green]✓ 已加载 {len(clients)} 个模型: {', '.join(c.name for c in clients)}[/]")

    # 加载题目
    if args.difficulty:
        challenges = get_by_difficulty(args.difficulty)
    else:
        challenges = load_all()

    if not challenges:
        console.print("[red]错误: 没有找到题目[/]")
        sys.exit(1)

    console.print(f"[green]✓ 已加载 {len(challenges)} 道题目[/]\n")

    # 运行评估
    results = run_benchmark(clients, challenges, runs_per_challenge=args.runs)

    # 打印摘要
    print_summary(results)

    # 生成报告
    report_path = generate_report(results, output_path=args.output)
    console.print(f"[bold green]📄 报告已生成: {report_path}[/]\n")


if __name__ == "__main__":
    main()
