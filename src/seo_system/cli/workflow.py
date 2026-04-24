#!/usr/bin/env python3
"""
run_workflow.py — SEO Content System Orchestrator
Chains all scripts and Claude Code sessions together for a single article.

Usage:
    python3 run_workflow.py --client monx --article "us-expat-tax" --step all
    python3 run_workflow.py --client monx --article "us-expat-tax" --step keyword
    python3 run_workflow.py --client monx --article "us-expat-tax" --from headline-outline
    python3 run_workflow.py --client monx --article "us-expat-tax" --step audit --force
"""

import argparse
import sys

from seo_system.config import (
    HUMAN_GATES,
    STEPS,
    get_content_base,
    load_client_profile,
    normalise_slug,
)
from seo_system.gates import interactive_gate
from seo_system.runner import print_status
from seo_system.steps import STEP_RUNNERS, RunContext
from seo_system.workspace import (
    init_article_files,
    is_complete,
    load_log,
    log_step_end,
    log_step_start,
    mark_complete,
    save_log,
    update_content_index,
    workspace,
)


def main():
    parser = argparse.ArgumentParser(description="SEO Content System Orchestrator")
    parser.add_argument("--client",  required=True, help="Client slug (e.g. monx)")
    parser.add_argument("--article", required=True, help="Article slug (e.g. us-expat-tax)")
    parser.add_argument("--step",    default="all",  help="Single step to run, or 'all'")
    parser.add_argument("--from",    dest="from_step", default=None,
                        help="Resume from this step (skips earlier completed steps)")
    parser.add_argument("--force",   action="store_true",
                        help="Re-run step even if already marked complete")
    args = parser.parse_args()

    content_base = get_content_base()
    client_dir = content_base / args.client

    if not client_dir.exists():
        print(f"ERROR: Client folder not found: {client_dir}")
        print(f"       Run onboard_client.py --client {args.client} to create it.")
        sys.exit(1)

    content_dir = client_dir / "content"
    brand_dir   = client_dir / "brand"
    content_dir.mkdir(parents=True, exist_ok=True)

    if not brand_dir.exists():
        print(f"WARNING: Brand folder not found at {brand_dir} — skills will not find brand files")

    profile = load_client_profile(client_dir)
    ctx = RunContext(
        content_dir=content_dir,
        brand_dir=brand_dir,
        sitemap_url=profile.get("sitemap_url"),
    )

    display_name = args.article
    article = normalise_slug(display_name)
    ws = workspace(content_dir, article)
    ws.mkdir(parents=True, exist_ok=True)
    (ws / "editorial").mkdir(exist_ok=True)
    (ws / "data").mkdir(exist_ok=True)
    (ws / "publish").mkdir(exist_ok=True)

    log = load_log(content_dir, article)
    if not log.get("steps"):
        log["steps"] = {s: {"status": "pending"} for s in STEPS}
        log["display_name"] = display_name
        save_log(content_dir, article, log)
    init_article_files(article, ws, display_name)

    if args.step == "all" or args.from_step:
        steps_to_run = STEPS
        if args.from_step:
            if args.from_step not in STEPS:
                print(f"Unknown step: {args.from_step}. Valid steps: {', '.join(STEPS)}")
                sys.exit(1)
            steps_to_run = STEPS[STEPS.index(args.from_step):]
    else:
        if args.step not in STEPS:
            print(f"Unknown step: {args.step}. Valid steps: {', '.join(STEPS)}")
            sys.exit(1)
        steps_to_run = [args.step]

    print()
    print(f"  SEO Content System — {args.client} / {display_name}  [{article}]")
    print(f"  {'─' * 50}")
    print()

    for step in steps_to_run:
        if not args.force and is_complete(content_dir, article, step):
            print_status(f"{step} — already complete, skipping", "skip")
            continue

        print_status(f"Starting step: {step.upper()}")
        log_step_start(article, ws, step)

        success = STEP_RUNNERS[step](ctx, article)

        if not success:
            log_step_end(article, ws, step, "failed")
            print_status(f"Step '{step}' failed. Fix the issue and re-run with --step {step} --force", "error")
            sys.exit(1)

        mark_complete(content_dir, article, step)
        log_step_end(article, ws, step, "complete")
        update_content_index(content_dir)
        print_status(f"{step} — done", "ok")

        if step in HUMAN_GATES and steps_to_run.index(step) < len(steps_to_run) - 1:
            interactive_gate(step, ws)

    print()
    print_status(f"All done. Workspace: {ws.resolve()}", "ok")
    print()


