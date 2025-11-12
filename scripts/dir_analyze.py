#!/usr/bin/env python3
"""
Directory and Git Repository Analyzer
Scans subdirectories to find git repositories and their status.
"""

import os
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class GitRepoInfo:
    """Information about a git repository"""
    path: str
    repo_name: str
    uncommitted_count: int
    untracked_count: int
    untracked_files: List[str]
    uncommitted_files: List[str]


def is_git_repo(path: Path) -> bool:
    """Check if directory is a git repository root"""
    return (path / '.git').exists()


def get_repo_name(path: Path) -> str:
    """Extract repository name from path"""
    return path.name


def should_ignore_path(path: str) -> bool:
    """Check if a path should be ignored based on ignore patterns"""
    ignore_patterns = {
        '.DS_Store',
        '.idea',
        '.specstory',
        'venv',
        '.venv',
        '.cursorindexingignore',
        '.vscode'
    }

    # Check if the path or any of its components match ignore patterns
    path_parts = path.split('/')
    for part in path_parts:
        if part in ignore_patterns:
            return True

    # Check if filename itself matches
    filename = path_parts[-1] if path_parts else ''
    if filename in ignore_patterns:
        return True

    return False


def get_git_status(repo_path: Path) -> Tuple[int, int, List[str], List[str]]:
    """
    Get git status for a repository.
    Returns: (uncommitted_count, untracked_count, untracked_files_list, uncommitted_files_list)
    """
    try:
        # Run git status in porcelain format for easier parsing
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return 0, 0, [], []

        uncommitted = 0
        untracked = 0
        untracked_files = []
        uncommitted_files = []

        for line in result.stdout.strip().split('\n'):
            if not line:
                continue

            status = line[:2]
            filename = line[3:]

            # Skip ignored patterns
            if should_ignore_path(filename):
                continue

            # Check if file is untracked
            if status == '??':
                untracked += 1
                untracked_files.append(filename)
            else:
                # Any other status means uncommitted changes
                uncommitted += 1
                uncommitted_files.append(filename)

        return uncommitted, untracked, untracked_files, uncommitted_files

    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        return 0, 0, [], []


def scan_directory(base_path: Path) -> Tuple[List[GitRepoInfo], List[str], List[str]]:
    """
    Scan directory for git repositories up to 2 levels deep.
    Returns: (git_repos, non_git_dirs, empty_dirs)
    """
    git_repos = []
    non_git_dirs = []
    empty_dirs = []

    ignore_names = {'.DS_Store', '.idea', '.specstory', 'venv', '.venv', '.cursorindexingignore', '.vscode'}

    try:
        # Get all subdirectories in base path (skip ignored patterns)
        subdirs = [d for d in base_path.iterdir()
                   if d.is_dir() and not d.name.startswith('.') and d.name not in ignore_names]
    except PermissionError:
        return git_repos, non_git_dirs, empty_dirs

    for subdir in subdirs:
        has_git_repo = False

        # Check if current directory is a git repo
        if is_git_repo(subdir):
            has_git_repo = True
            uncommitted, untracked, untracked_files, uncommitted_files = get_git_status(subdir)
            relative_path = subdir.relative_to(base_path)

            git_repos.append(GitRepoInfo(
                path=str(relative_path),
                repo_name=get_repo_name(subdir),
                uncommitted_count=uncommitted,
                untracked_count=untracked,
                untracked_files=untracked_files,
                uncommitted_files=uncommitted_files
            ))

        # Check one level deeper
        try:
            subdirs_level2 = [d for d in subdir.iterdir()
                              if d.is_dir() and not d.name.startswith('.') and d.name not in ignore_names]

            # Check for empty directory (ignoring ignored patterns)
            all_contents = list(subdir.iterdir())
            non_ignored_contents = [item for item in all_contents
                                    if item.name not in ignore_names and not item.name.startswith('.')]

            if not non_ignored_contents:
                relative_path = subdir.relative_to(base_path)
                empty_dirs.append(str(relative_path))
                continue

            for subdir2 in subdirs_level2:
                if is_git_repo(subdir2):
                    has_git_repo = True
                    uncommitted, untracked, untracked_files, uncommitted_files = get_git_status(subdir2)
                    relative_path = subdir2.relative_to(base_path)

                    git_repos.append(GitRepoInfo(
                        path=str(relative_path),
                        repo_name=get_repo_name(subdir2),
                        uncommitted_count=uncommitted,
                        untracked_count=untracked,
                        untracked_files=untracked_files,
                        uncommitted_files=uncommitted_files
                    ))

            # If no git repos found at any level
            if not has_git_repo:
                relative_path = subdir.relative_to(base_path)
                non_git_dirs.append(str(relative_path))

        except PermissionError:
            continue

    return git_repos, non_git_dirs, empty_dirs


def generate_markdown_report(git_repos: List[GitRepoInfo], non_git_dirs: List[str],
                             empty_dirs: List[str], output_file: str):
    """Generate markdown report file"""

    # Categorize git repos
    clean_repos = []
    uncommitted_only = []
    untracked_only = []
    both_changes = []

    for repo in git_repos:
        if repo.uncommitted_count == 0 and repo.untracked_count == 0:
            clean_repos.append(repo)
        elif repo.uncommitted_count > 0 and repo.untracked_count == 0:
            uncommitted_only.append(repo)
        elif repo.uncommitted_count == 0 and repo.untracked_count > 0:
            untracked_only.append(repo)
        else:
            both_changes.append(repo)

    # Write markdown file
    with open(output_file, 'w') as f:
        f.write("# Directory Analysis Report\n\n")

        # Clean repos
        f.write(f"## Git Repos (Clean - No Changes) - Total: {len(clean_repos)}\n\n")
        if clean_repos:
            for repo in sorted(clean_repos, key=lambda r: r.path):
                f.write(f"- **{repo.path}**\n")
                f.write(f"  - Repository: {repo.repo_name}\n")
                f.write(f"  - Status: Clean\n\n")
        else:
            f.write("*None*\n\n")

        # Uncommitted only
        f.write(f"## Git Repos (Uncommitted Changes Only) - Total: {len(uncommitted_only)}\n\n")
        if uncommitted_only:
            for repo in sorted(uncommitted_only, key=lambda r: r.path):
                f.write(f"- **{repo.path}**\n")
                f.write(f"  - Repository: {repo.repo_name}\n")
                f.write(f"  - Uncommitted files: {repo.uncommitted_count}\n")

                # List files if 4 or fewer
                if repo.uncommitted_count <= 4:
                    for file in repo.uncommitted_files:
                        f.write(f"    - `{file}`\n")
                f.write("\n")
        else:
            f.write("*None*\n\n")

        # Untracked only
        f.write(f"## Git Repos (Untracked Files Only) - Total: {len(untracked_only)}\n\n")
        if untracked_only:
            for repo in sorted(untracked_only, key=lambda r: r.path):
                f.write(f"- **{repo.path}**\n")
                f.write(f"  - Repository: {repo.repo_name}\n")
                f.write(f"  - Untracked files: {repo.untracked_count}\n")

                # List files if 4 or fewer
                if repo.untracked_count <= 4:
                    for file in repo.untracked_files:
                        f.write(f"    - `{file}`\n")
                f.write("\n")
        else:
            f.write("*None*\n\n")

        # Both changes
        f.write(f"## Git Repos (Both Uncommitted and Untracked Changes) - Total: {len(both_changes)}\n\n")
        if both_changes:
            for repo in sorted(both_changes, key=lambda r: r.path):
                f.write(f"- **{repo.path}**\n")
                f.write(f"  - Repository: {repo.repo_name}\n")
                f.write(f"  - Uncommitted files: {repo.uncommitted_count}\n")
                f.write(f"  - Untracked files: {repo.untracked_count}\n")

                # List uncommitted files if 4 or fewer
                if repo.uncommitted_count <= 4:
                    f.write(f"  - Uncommitted:\n")
                    for file in repo.uncommitted_files:
                        f.write(f"    - `{file}`\n")

                # List untracked files if 4 or fewer
                if repo.untracked_count <= 4:
                    f.write(f"  - Untracked:\n")
                    for file in repo.untracked_files:
                        f.write(f"    - `{file}`\n")
                f.write("\n")
        else:
            f.write("*None*\n\n")

        # Non-git directories
        f.write(f"## Directories Without Git Repos - Total: {len(non_git_dirs)}\n\n")
        if non_git_dirs:
            for dir_path in sorted(non_git_dirs):
                f.write(f"- {dir_path}\n")
            f.write("\n")
        else:
            f.write("*None*\n\n")

        # Empty directories
        f.write(f"## Empty Directories - Total: {len(empty_dirs)}\n\n")
        if empty_dirs:
            for dir_path in sorted(empty_dirs):
                f.write(f"- {dir_path}\n")
            f.write("\n")
        else:
            f.write("*None*\n\n")


def main():
    """Main execution function"""
    base_path = Path.cwd()
    print(f"Analyzing directories in: {base_path}")
    print("Scanning for git repositories...")

    git_repos, non_git_dirs, empty_dirs = scan_directory(base_path)

    print(f"\nFound:")
    print(f"  - {len(git_repos)} git repositories")
    print(f"  - {len(non_git_dirs)} non-git directories")
    print(f"  - {len(empty_dirs)} empty directories")

    output_file = base_path / "dir.md"
    generate_markdown_report(git_repos, non_git_dirs, empty_dirs, output_file)

    print(f"\nReport generated: {output_file}")


if __name__ == "__main__":
    main()