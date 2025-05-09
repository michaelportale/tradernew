#!/usr/bin/env python
"""
Script to run the Celery worker for the ML Trading System.

Usage:
    # Run a worker with the 'model_tasks' queue
    python celery_worker.py --queue model_tasks

    # Run a worker with the 'data_tasks' queue
    python celery_worker.py --queue data_tasks

    # Run a worker with all queues
    python celery_worker.py

    # Run with concurrency (number of worker processes)
    python celery_worker.py --concurrency 4

    # Run with beat scheduler (for periodic tasks)
    python celery_worker.py --beat
"""

import os
import sys
import argparse
from app.tasks.worker import celery_app


def main():
    parser = argparse.ArgumentParser(description="Run Celery worker for ML Trading System")
    parser.add_argument(
        "--queue", "-q", type=str, 
        help="Queue to process (model_tasks, data_tasks, or leave empty for all)"
    )
    parser.add_argument(
        "--concurrency", "-c", type=int, default=2,
        help="Number of worker processes/threads"
    )
    parser.add_argument(
        "--beat", "-b", action="store_true",
        help="Include beat scheduler for periodic tasks"
    )
    parser.add_argument(
        "--loglevel", "-l", type=str, default="INFO",
        help="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )
    
    args = parser.parse_args()
    
    # Build the command arguments
    command_args = [
        "worker",
        f"--concurrency={args.concurrency}",
        f"--loglevel={args.loglevel}",
    ]
    
    # Add the queue if specified
    if args.queue:
        command_args.append(f"--queues={args.queue}")
    
    # Add the beat scheduler if requested
    if args.beat:
        command_args.append("--beat")
    
    # Run the worker
    sys.argv = [sys.argv[0]] + command_args
    celery_app.worker_main()


if __name__ == "__main__":
    main() 