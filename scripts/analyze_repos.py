#!/usr/bin/env python3
"""
Analyze git repositories in subdirectories and generate a markdown report.
"""

import os
import subprocess
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Set


@dataclass
class RepoInfo:
    """Information about a git repository."""
    path: str
    repo_name: str
    uncommitted_files: List[str]
    untracked_files: List[str]


# Files and directories to ignore
IGNORED_ITEMS = {
    '.DS_Store',
    '.idea',
    '.specstory',
    'venv',
    '.venv',
    '.cursorindexingignore',
    '.vscode'
}


def is_git_repo(directory: Path) -> bool:
    """Check if a directory is a git repository root."""
    return (directory / '.git').is_dir()


def should_ignore(name: str) -> bool:
    """Check if a file or directory should be ignored."""
    return name in IGNORED_ITEMS


def get_git_status(repo_path: Path) -> tuple[List[str], List[str]]:
    """
    Get uncommitted and untracked files from git status.
    Returns: (uncommitted_files, untracked_files)
    """
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )

        uncommitted = []
        untracked = []

        for line in result.stdout.splitlines():
            if not line.strip():
                continue

            status = line[:2]
            filepath = line[3:].strip()

            # Skip ignored files/directories
            parts = filepath.split('/')
            if any(should_ignore(part) for part in parts):
                continue
            if should_ignore(os.path.basename(filepath)):
                continue

            # ?? means untracked
            if status.strip() == '??':
                untracked.append(filepath)
            else:
                # Any other status means uncommitted changes
                uncommitted.append(filepath)

        return uncommitted, untracked

    except subprocess.CalledProcessError:
        return [], []


def find_git_repos(base_dir: Path) -> List[RepoInfo]:
    """
    Find all git repositories up to 2 levels deep.
    """
    repos = []

    # Check immediate subdirectories
    try:
        subdirs = [d for d in base_dir.iterdir() if d.is_dir() and not should_ignore(d.name)]
    except PermissionError:
        return repos

    for subdir in subdirs:
        # Check if this subdirectory is a git repo
        if is_git_repo(subdir):
            uncommitted, untracked = get_git_status(subdir)
            repo_name = subdir.name
            relative_path = subdir.relative_to(base_dir)

            repos.append(RepoInfo(
                path=str(relative_path),
                repo_name=repo_name,
                uncommitted_files=uncommitted,
                untracked_files=untracked
            ))
        else:
            # Go one level deeper
            try:
                nested_dirs = [d for d in subdir.iterdir() if d.is_dir() and not should_ignore(d.name)]
            except PermissionError:
                continue

            for nested_dir in nested_dirs:
                if is_git_repo(nested_dir):
                    uncommitted, untracked = get_git_status(nested_dir)
                    repo_name = nested_dir.name
                    relative_path = nested_dir.relative_to(base_dir)

                    repos.append(RepoInfo(
                        path=str(relative_path),
                        repo_name=repo_name,
                        uncommitted_files=uncommitted,
                        untracked_files=untracked
                    ))

    return repos


def find_non_git_dirs(base_dir: Path) -> tuple[List[str], List[str]]:
    """
    Find directories that don't have git repos and empty directories.
    Returns: (non_git_dirs, empty_dirs)
    """
    non_git_dirs = []
    empty_dirs = []

    try:
        subdirs = [d for d in base_dir.iterdir() if d.is_dir() and not should_ignore(d.name)]
    except PermissionError:
        return non_git_dirs, empty_dirs

    for subdir in subdirs:
        relative_path = str(subdir.relative_to(base_dir))

        # Check if directory is empty
        try:
            contents = list(subdir.iterdir())
            filtered_contents = [c for c in contents if not should_ignore(c.name)]

            if not filtered_contents:
                empty_dirs.append(relative_path)
                continue
        except PermissionError:
            continue

        # Check if this dir or any nested dir (one level) contains a git repo
        has_git_repo = is_git_repo(subdir)

        if not has_git_repo:
            # Check one level deeper
            try:
                nested_dirs = [d for d in subdir.iterdir() if d.is_dir() and not should_ignore(d.name)]
                has_nested_git = any(is_git_repo(nd) for nd in nested_dirs)

                if not has_nested_git:
                    non_git_dirs.append(relative_path)
            except PermissionError:
                non_git_dirs.append(relative_path)

    return non_git_dirs, empty_dirs


def truncate_path(filepath: str, max_length: int = 30) -> str:
    """Truncate file path if it exceeds max_length."""
    if len(filepath) > max_length:
        return os.path.basename(filepath)
    return filepath


def format_file_list(files: List[str], max_files: int = 4) -> str:
    """Format file list with truncation rules."""
    if len(files) <= max_files:
        return '\n'.join(f"  - {truncate_path(f)}" for f in files)
    return f"  ({len(files)} files)"


def generate_markdown(repos: List[RepoInfo], non_git_dirs: List[str], empty_dirs: List[str]) -> str:
    """Generate the markdown report."""
    # Categorize repositories
    clean_repos = []
    only_uncommitted = []
    only_untracked = []
    both_changes = []

    for repo in repos:
        has_uncommitted = len(repo.uncommitted_files) > 0
        has_untracked = len(repo.untracked_files) > 0

        if not has_uncommitted and not has_untracked:
            clean_repos.append(repo)
        elif has_uncommitted and not has_untracked:
            only_uncommitted.append(repo)
        elif has_untracked and not has_uncommitted:
            only_untracked.append(repo)
        else:
            both_changes.append(repo)

    # Build markdown
    md = []

    # Section 1: Clean repos
    md.append(f"## Git repos with no uncommitted or untracked files (Total: {len(clean_repos)})\n")
    if clean_repos:
        for repo in clean_repos:
            md.append(f"- **{repo.repo_name}** (`{repo.path}`)")
            md.append(f"  - delete? - [ ]")
        md.append("")
    else:
        md.append("None\n")

    # Section 2: Only uncommitted files
    md.append(f"## Git repos with only uncommitted files (Total: {len(only_uncommitted)})\n")
    if only_uncommitted:
        for repo in only_uncommitted:
            md.append(f"- **{repo.repo_name}** (`{repo.path}`)")
            md.append(f"  - Uncommitted: {len(repo.uncommitted_files)}")
            if len(repo.uncommitted_files) <= 4:
                for f in repo.uncommitted_files:
                    md.append(f"    - {truncate_path(f)}")
            md.append(f"  - delete? - [ ]")
        md.append("")
    else:
        md.append("None\n")

    # Section 3: Only untracked files
    md.append(f"## Git repos with only untracked files (Total: {len(only_untracked)})\n")
    if only_untracked:
        for repo in only_untracked:
            md.append(f"- **{repo.repo_name}** (`{repo.path}`)")
            md.append(f"  - Untracked: {len(repo.untracked_files)}")
            if len(repo.untracked_files) <= 4:
                for f in repo.untracked_files:
                    md.append(f"    - {truncate_path(f)}")
            md.append(f"  - delete? - [ ]")
        md.append("")
    else:
        md.append("None\n")

    # Section 4: Both uncommitted and untracked
    md.append(f"## Git repos with both uncommitted and untracked files (Total: {len(both_changes)})\n")
    if both_changes:
        for repo in both_changes:
            md.append(f"- **{repo.repo_name}** (`{repo.path}`)")
            md.append(f"  - Uncommitted: {len(repo.uncommitted_files)}")
            if len(repo.uncommitted_files) <= 4:
                for f in repo.uncommitted_files:
                    md.append(f"    - {truncate_path(f)}")
            md.append(f"  - Untracked: {len(repo.untracked_files)}")
            if len(repo.untracked_files) <= 4:
                for f in repo.untracked_files:
                    md.append(f"    - {truncate_path(f)}")
            md.append(f"  - delete? - [ ]")
        md.append("")
    else:
        md.append("None\n")

    # Section 5: Non-git directories
    md.append(f"## Directories without git repos (Total: {len(non_git_dirs)})\n")
    if non_git_dirs:
        for dir_path in non_git_dirs:
            md.append(f"- `{dir_path}`")
            md.append(f"  - delete? - [ ]")
        md.append("")
    else:
        md.append("None\n")

    # Section 6: Empty directories
    md.append(f"## Empty directories (Total: {len(empty_dirs)})\n")
    if empty_dirs:
        for dir_path in empty_dirs:
            md.append(f"- `{dir_path}`")
            md.append(f"  - delete? - [ ]")
        md.append("")
    else:
        md.append("None\n")

    return '\n'.join(md)


def main():
    """Main function."""
    base_dir = Path.cwd()

    print("Analyzing directories...")
    repos = find_git_repos(base_dir)
    non_git_dirs, empty_dirs = find_non_git_dirs(base_dir)

    print(f"Found {len(repos)} git repositories")
    print(f"Found {len(non_git_dirs)} non-git directories")
    print(f"Found {len(empty_dirs)} empty directories")

    print("\nGenerating report...")
    markdown = generate_markdown(repos, non_git_dirs, empty_dirs)

    output_file = base_dir / 'dir.md'
    output_file.write_text(markdown)

    print(f"Report saved to {output_file}")


if __name__ == '__main__':
    main()
