#!/usr/bin/env python3
"""
run_workflow.py — SEO Content System Orchestrator

Usage:
    python3 run_workflow.py --client monx --article "us-expat-tax" --step all
    python3 run_workflow.py --client monx --article "us-expat-tax" --from headline-outline
"""
from seo_system.cli.workflow import main

if __name__ == "__main__":
    main()
