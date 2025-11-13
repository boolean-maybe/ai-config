---
name: cloudwatch
description: use CloudWatch to retrieve logs and analyze failures
allowed-tools: Read, Grep, Glob, Update, "Bash(ls:*), "Bash(aws logs:*), "Bash(~/.claude/skills/cloudwatch/scripts/get_pod_logs.sh:*)"
---

# Patcher job logs

If user asks to find a log for a pod for example 123 it means find a log for a Kubernetes
job that ran patcher for pod 123. "pod" in this context means our 1P pods, not Kubernetes pods
These Kubernetes jobs that are deleted when done. Their logs are saved to CloudWatch
They can be retrieved using [get_pod_logs.sh](~/.claude/skills/cloudwatch/scripts/get_pod_logs.sh) helper script:

```bash
scripts/get_pod_logs.sh podId period
```

where `podId` is like 123 and period is like `24H`
write this log to a temporary file to avoid multiple roundtrips to CloudWatch