import os
import re
import subprocess
import sys

# Define ownership mapping as compiled regex patterns
OWNERSHIP_MAP = [
    (re.compile(r"^apps/web/src/features/.*"), "@frontend"),
    (re.compile(r"^apps/web/src/app/.*"), "@frontend"),
    (re.compile(r"^apps/web/Dockerfile$"), "@devops"),
    (re.compile(r"^apps/web/package\.json$"), "@frontend"),
    (re.compile(r"^apps/web/.*\.config\..*"), "@frontend"),
    
    (re.compile(r"^apps/api/src/modules/.*"), "@backend"),
    (re.compile(r"^apps/api/src/core/.*"), "@backend"),
    (re.compile(r"^apps/api/src/main\.py$"), "@backend"),
    (re.compile(r"^apps/api/alembic/.*"), "@backend"),
    (re.compile(r"^apps/api/tests/test_integration_.*"), "@qa"),
    (re.compile(r"^apps/api/tests/.*"), "@backend"),
    (re.compile(r"^apps/api/Dockerfile$"), "@devops"),
    (re.compile(r"^apps/api/requirements\.txt$"), "@backend"),
    
    (re.compile(r"^packages/shared/types/.*"), "@api-steward"),
    (re.compile(r"^packages/shared/enums/.*"), "@backend"),
    (re.compile(r"^packages/shared/constants/.*"), "@backend"),
    
    (re.compile(r"^infra/.*"), "@devops"),
    (re.compile(r"^runbooks/.*"), "@devops"),
    
    (re.compile(r"^docs/api/.*"), "@api-steward"),
    (re.compile(r"^docs/product/.*"), "@pm"),
    (re.compile(r"^docs/.*"), "@architect"),
    (re.compile(r"^agents/.*"), "@architect"),
    (re.compile(r"^AGENTS\.md$"), "@architect"),
    (re.compile(r"^\.agent/tasks/.*"), "tasks"), # Tasks are updated by owner, handled separately
    (re.compile(r"^\.agent/requests/.*"), "requests"), # Requests can be created by any agent
    (re.compile(r"^\.agent/rules/.*"), "@architect"),
    (re.compile(r"^\.agent/skills/.*"), "@architect"),
    (re.compile(r"^\.agent/team_status\.md$"), "shared"), # Read/write by all
    
    (re.compile(r"^evals/.*"), "@qa"),
]

def get_modified_files():
    try:
        # Run git status --porcelain to see all added/modified/deleted files
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True
        )
        files = []
        for line in result.stdout.splitlines():
            if len(line) > 3:
                # Format is usually ' M path/to/file' or 'A  path/to/file'
                status = line[:2].strip()
                path = line[3:].strip()
                # Handle renamed files (e.g. "R  old -> new")
                if " -> " in path:
                    path = path.split(" -> ")[-1]
                files.append((status, path))
        return files
    except Exception as e:
        print(f"Error running git command: {e}")
        return []

def get_active_agents(team_status_path):
    active_agents = set()
    if not os.path.exists(team_status_path):
        print(f"Error: {team_status_path} does not exist.")
        return active_agents
        
    with open(team_status_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Find lines like "| `@agent` | 🟡 IN_PROGRESS | ..."
    pattern = r"\|\s*`?(@[a-zA-Z0-9_-]+)`?\s*\|\s*🟡\s*IN_PROGRESS\s*\|"
    matches = re.findall(pattern, content)
    for match in matches:
        active_agents.add(match.strip())
    return active_agents

def get_owner(file_path):
    # Normalize path to use forward slashes
    file_path = file_path.replace("\\", "/")
    for pattern, owner in OWNERSHIP_MAP:
        if pattern.match(file_path):
            return owner
    return None

def validate():
    workspace_root = os.getcwd()
    team_status_path = os.path.join(workspace_root, ".agent", "team_status.md")
    
    modified_files = get_modified_files()
    active_agents = get_active_agents(team_status_path)
    
    print("=== AGENTIC GOVERNANCE VALIDATOR ===")
    print(f"Active Agents (IN_PROGRESS): {', '.join(active_agents) if active_agents else 'None'}")
    print(f"Modified files detected: {len(modified_files)}")
    print("-" * 40)
    
    violations = 0
    for status, file_path in modified_files:
        owner = get_owner(file_path)
        if owner is None:
            print(f"[WARN] [UNKNOWN OWNER] {file_path} (No ownership pattern matched)")
            continue
            
        if owner in ["tasks", "requests", "shared"]:
            # Special directories that are collaborative
            continue
            
        # Check if the owner is currently marked as active
        if owner not in active_agents:
            print(f"[ERROR] [VIOLATION] File '{file_path}' (owned by {owner}) was modified, but {owner} is not marked as active (IN_PROGRESS)!")
            violations += 1
        else:
            print(f"[OK] {file_path} (modified by active owner {owner})")
            
    print("-" * 40)
    if violations > 0:
        print(f"[FAIL] FAILED: Found {violations} governance violation(s).")
        sys.exit(1)
    else:
        print("[PASS] SUCCESS: No ownership violations detected.")
        sys.exit(0)

if __name__ == "__main__":
    validate()
