import argparse
import subprocess
from pathlib import Path


def run(args: list[str]) -> str:
    result = subprocess.run(args, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.strip()


def parse_seed(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    meta: dict[str, str] = {}
    body_start = 0
    if lines and lines[0].strip() == "---":
        for index, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                body_start = index + 1
                break
            if ":" in line:
                key, value = line.split(":", 1)
                meta[key.strip().lower()] = value.strip().strip('"')
    body = "\n".join(lines[body_start:]).strip()
    meta["body"] = body
    return meta


def normalize_category(value: str) -> str:
    value = value.strip().lower()
    aliases = {
        "show and tell": "show and tell",
        "show-and-tell": "show and tell",
        "show & tell": "show and tell",
        "q&a": "q&a",
        "qa": "q&a",
        "questions": "q&a",
        "ideas": "ideas",
        "general": "general",
    }
    return aliases.get(value, value)


def graphql(query: str, **fields: str) -> str:
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in fields.items():
        args.extend(["-f", f"{key}={value}"])
    return run(args)


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed GitHub Discussions from discussion-seeds/*.md.")
    parser.add_argument("--repo", required=True, help="Repository in owner/name form.")
    parser.add_argument("--seeds", default="discussion-seeds", help="Seed post directory.")
    args = parser.parse_args()

    owner, name = args.repo.split("/", 1)
    run(["gh", "api", "-X", "PATCH", f"repos/{args.repo}", "-f", "has_discussions=true"])

    repo_query = """
      query($owner: String!, $name: String!) {
        repository(owner: $owner, name: $name) {
          id
          discussionCategories(first: 25) { nodes { id name } }
        }
      }
    """
    data = graphql(repo_query, owner=owner, name=name)
    import json

    parsed = json.loads(data)
    repo = parsed["data"]["repository"]
    repo_id = repo["id"]
    categories = {normalize_category(node["name"]): node["id"] for node in repo["discussionCategories"]["nodes"]}

    mutation = """
      mutation($repositoryId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
        createDiscussion(input: {repositoryId: $repositoryId, categoryId: $categoryId, title: $title, body: $body}) {
          discussion { url }
        }
      }
    """

    for seed in sorted(Path(args.seeds).glob("*.md")):
        item = parse_seed(seed)
        title = item.get("title") or seed.stem.replace("-", " ").title()
        category_name = normalize_category(item.get("category", "General"))
        category_id = categories.get(category_name) or categories.get("general") or next(iter(categories.values()))
        result = graphql(mutation, repositoryId=repo_id, categoryId=category_id, title=title, body=item["body"])
        url = json.loads(result)["data"]["createDiscussion"]["discussion"]["url"]
        print(url)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
