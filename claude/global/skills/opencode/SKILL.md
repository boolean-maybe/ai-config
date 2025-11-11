---
name: opencode
description: use opencode CLI to analyze and modify repositories
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Using OpenCode CLI for Repository Analysis and Modification

OpenCode is a powerful CLI tool for analyzing and modifying entire repositories with AI assistance. Use `opencode run` to leverage OpenCode's capabilities for codebase analysis and modifications.

## Basic Command Structure

The most common usage is:
```bash
opencode run "your prompt here"
```

You can also specify a project path and model:
```bash
opencode run -p "your prompt" --model provider/model
```

## File and Directory Inclusion

When running OpenCode commands, you can reference files and directories directly in your prompt:

### Examples:

**Analyze a single file:**
```bash
opencode run "Analyze src/main.py and explain its purpose"
```

**Analyze multiple files:**
```bash
opencode run "Compare the structure of src/index.js and src/utils.js"
```

**Analyze an entire directory:**
```bash
opencode run "Summarize the architecture of the src/ directory"
```

**Analyze multiple directories:**
```bash
opencode run "Review test coverage in src/ and tests/ directories"
```

**Analyze the entire project:**
```bash
opencode run "Give me an overview of this entire project structure"
```

## Common Use Cases

### Code Review and Analysis

Review code quality and architecture:
```bash
opencode run "Review the code in src/services/ for performance and security issues"
```

Check for specific patterns or implementations:
```bash
opencode run "Has error handling been properly implemented in all API endpoints in src/api/?"
```

Verify authentication implementation:
```bash
opencode run "Analyze src/middleware/ and src/auth/ - is JWT authentication properly implemented?"
```

### Code Modifications

Make targeted code changes:
```bash
opencode run "Add proper error handling to all functions in src/utils.js"
```

Refactor code:
```bash
opencode run "Refactor src/components/ to use React hooks instead of class components"
```

Add missing features:
```bash
opencode run "Add input validation to all API endpoints in src/api/routes/"
```

### Testing and Quality

Generate tests:
```bash
opencode run "Generate comprehensive unit tests for src/services/payment.ts"
```

Verify test coverage:
```bash
opencode run "Analyze src/payment/ and tests/ - are all payment functions tested?"
```

### Documentation

Generate documentation:
```bash
opencode run "Create comprehensive JSDoc comments for all functions in src/lib/"
```

## When to Use OpenCode

Use `opencode run` when:
- You need to analyze entire repositories or large directories
- You want to make widespread code changes across multiple files
- You need AI-assisted code review and suggestions
- You're refactoring large portions of the codebase
- You need to verify implementations across the entire project
- You want to generate tests or documentation
- You need to understand project-wide patterns or architecture

## Advanced Features

### Continue Previous Sessions

```bash
opencode run -c "your next prompt"  # Continue last session
opencode run -s session-id "prompt"  # Continue specific session
```

### Export and Import Sessions

```bash
opencode export session-id  # Export session as JSON
opencode import file.json   # Import session data
```

### Using Specific Models

```bash
opencode run -m claude-3-5-sonnet "your prompt"
```

## Important Notes

- OpenCode works best with specific, clear prompts
- You can reference files and directories by their relative paths
- OpenCode can modify files directly, so be careful with your prompts
- Use descriptive prompts to get accurate results
- For large repositories, break down complex tasks into smaller prompts
- OpenCode sessions can be continued and exported for reproducibility
