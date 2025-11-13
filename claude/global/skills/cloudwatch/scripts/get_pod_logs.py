#!/usr/bin/env python3
"""
Retrieve CloudWatch logs for a specific pod from AWS EKS.

Usage: python get_pod_logs.py [pod_id] [period]
    pod_id: like 123
    period: like 1H, 6H, 12H, 24H (default: 24H)
"""

import json
import subprocess
import sys
import time
from datetime import datetime


def usage():
    print(f"usage: {sys.argv[0]} [pod id] [period]")
    print("  pod id like 123")
    print("  period like 1H, 6H, 12H, 24H")


def convert_period_to_seconds(period):
    """Convert period string to seconds."""
    period_map = {
        "1H": 3600,
        "6H": 21600,
        "12H": 43200,
        "24H": 86400,
    }
    return period_map.get(period, 86400)


def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    pod_id = sys.argv[1]
    period = sys.argv[2] if len(sys.argv) > 2 else "24H"
    total_period_secs = convert_period_to_seconds(period)
    chunk_size = 3600  # 1 hour chunks to ensure we get all results within CloudWatch limits

    # Calculate time windows
    end_time = int(datetime.now().timestamp())
    start_time = end_time - total_period_secs

    all_messages = []
    current_start = start_time

    while current_start < end_time:
        current_end = min(current_start + chunk_size, end_time)

        # Start query for this time window
        cmd = [
            "aws", "logs", "start-query",
            "--log-group-name", "/aws/containerinsights/prod/application",
            "--start-time", str(current_start),
            "--end-time", str(current_end),
            "--query-string", f'filter @logStream like /patcher-{pod_id}/ and @message like /"container_name":"patcher"/ | fields @message | sort @timestamp',
            "--query", "queryId"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        try:
            query_id = json.loads(result.stdout)
        except Exception:
            print(f"Failed to start query: {result.stderr}", file=sys.stderr)
            current_start = current_end
            continue

        # Wait for query to complete
        attempts = 0
        while attempts < 120:
            cmd = ["aws", "logs", "describe-queries", "--query", f"queries[?queryId=='{query_id}']"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            try:
                queries = json.loads(result.stdout)
                if queries and queries[0].get('status') == 'Complete':
                    break
            except Exception:
                pass
            attempts += 1
            time.sleep(0.5)

        # Get results with pagination
        next_token = None
        while True:
            if next_token:
                cmd = ["aws", "logs", "get-query-results", "--query-id", query_id, "--next-token", next_token]
            else:
                cmd = ["aws", "logs", "get-query-results", "--query-id", query_id]

            result = subprocess.run(cmd, capture_output=True, text=True)
            try:
                response = json.loads(result.stdout)
            except Exception:
                print(f"Failed to parse response", file=sys.stderr)
                break

            # Extract log messages
            for result_set in response.get('results', []):
                for field_obj in result_set:
                    if field_obj.get('field') == '@message':
                        try:
                            msg_obj = json.loads(field_obj.get('value', ''))
                            log_line = msg_obj.get('log', '')
                            if log_line:
                                all_messages.append(log_line)
                        except Exception:
                            pass

            # Check for next page
            next_token = response.get('nextToken')
            if not next_token:
                break

        current_start = current_end

    # Output all log lines sorted by timestamp
    for log_line in all_messages:
        print(log_line)


if __name__ == "__main__":
    main()
