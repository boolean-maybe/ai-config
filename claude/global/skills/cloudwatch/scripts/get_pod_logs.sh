#!/bin/sh

programname=$0

function usage {
    echo "usage: $programname [pod id] [period]"
    echo "  pod id like 123"
    echo "  period like 24H"
}

if [[ $# -eq 0 ]] ; then
    usage
    exit 1
fi

POD=$1
PERIOD=$2

# Convert period to seconds
case $PERIOD in
    1H) PERIOD_SECS=3600 ;;
    6H) PERIOD_SECS=21600 ;;
    12H) PERIOD_SECS=43200 ;;
    24H) PERIOD_SECS=86400 ;;
    *) PERIOD_SECS=86400 ;;
esac

# Use Python to handle chunked queries and pagination
python3 -u - "$POD" "$PERIOD_SECS" << 'PYTHON_EOF'
import json
import subprocess
import sys
import time
from datetime import datetime, timedelta

pod_id = sys.argv[1]
total_period_secs = int(sys.argv[2])
chunk_size = 3600  # 1 hour chunks to ensure we get all results within CloudWatch limits

# Calculate time windows
end_time = int(datetime.now().timestamp())
start_time = end_time - total_period_secs

all_messages = []
current_start = start_time

while current_start < end_time:
    current_end = min(current_start + chunk_size, end_time)

    print(f"Querying pod {pod_id} from {datetime.fromtimestamp(current_start)} to {datetime.fromtimestamp(current_end)}", file=sys.stderr)

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
    except:
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
        except:
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
        except:
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
                    except:
                        pass

        # Check for next page
        next_token = response.get('nextToken')
        if not next_token:
            break

    current_start = current_end

# Output all log lines sorted by timestamp
for log_line in all_messages:
    print(log_line)
PYTHON_EOF
