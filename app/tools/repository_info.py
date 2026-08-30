
import subprocess
from pathlib import Path

def _run_git(
    repository_path: str,
    arguments: list[str]
):
    root = Path(repository_path)

    if not root.exists():
        raise ValueError(
            f"Repository path does not exist: {repository_path}"
        )

    if not root.is_dir():
        raise ValueError(
            f"Repository path is not a directory: {repository_path}"
        )

    try:
        result = subprocess.run(
            ["git", "-C", str(root), *arguments],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    except subprocess.CalledProcessError as exc:

        raise RuntimeError(
            f"Git command failed: {exc.stderr.strip()}"
        )from exc

def get_repository_info(
    repository_path: str,
)->dict:

    branch = _run_git(
        repository_path = repository_path,
        arguments=["branch", "--show-current"],
    )

    commit = _run_git(
        repository_path=repository_path,
        arguments= ["log", "-1", "--format=%H"]
    )

    commit_message = _run_git(
        repository_path=repository_path,
        arguments= ["log", "-1", "--format=%s"]
    )

    status = _run_git(
        repository_path=repository_path,
        arguments=["status", "--short"]
    )

    return {
        "branch": branch,
        "latest_commit": commit,
        "latest_commit_message": commit_message,
        "status": status,
    }
    

    

