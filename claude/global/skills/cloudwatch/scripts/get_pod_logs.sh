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

# find the latest log stream for a pod
LOG_STREAM=$(aws logs describe-log-streams \
    --log-group-name /aws/containerinsights/prod/application \
    --order-by LastEventTime --descending \
    --query "logStreams[?logStreamName.contains(@,'patching_patcher') && logStreamName.contains(@,'patcher-$POD')].logStreamName | [0]" \
    | jq -r)

echo "log stream $LOG_STREAM"

# initiate a query
QUERY_ID=$(aws logs start-query \
    --log-group-name /aws/containerinsights/prod/application \
    --start-time $(date -v-$PERIOD +%s) \
    --end-time $(date +%s) \
    --query-string "filter @logStream = '$LOG_STREAM' | fields @message | sort @timestamp" --query "queryId" \
    | jq -r)

echo "query id: $QUERY_ID"

COMPLETED_QUERIES=0
while [ $COMPLETED_QUERIES = 0 ]
do
   # this will return 0 until complete
   COMPLETED_QUERIES=$(aws logs describe-queries --query "queries[?queryId.contains(@,'$QUERY_ID')]" --status Complete | jq length)
   echo "wating for query to complete..."
done

aws logs get-query-results --query-id $QUERY_ID | jq -r '.results[][0].value | fromjson | .log'