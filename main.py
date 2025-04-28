from modules.jira_client import fetch_jira_issues
from modules.duplicate_checker import find_duplicates_among_issues
from config import JQL_QUERY, MAX_ISSUES
from setup_logger import logger
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=float, default=0.98, help="Similarity threshold for duplicate detection")
    args = parser.parse_args()

    print(f"[DEBUG] MAX_ISSUES: {MAX_ISSUES}")
    print(f"[DEBUG] JQL_QUERY: {JQL_QUERY}")
    print(f"[DEBUG] SIMILARITY_THRESHOLD (CLI 입력): {args.threshold}")

    from config import SIMILARITY_THRESHOLD
    SIMILARITY_THRESHOLD = args.threshold

    print("[STEP 1] Jira 이슈 목록 가져오는 중...")
    issues = fetch_jira_issues(JQL_QUERY)
    print(f"[STEP 2] {len(issues)}개의 이슈를 불러왔습니다.")

    print("\n[STEP 3] Jira 이슈 간 중복 확인 시작...\n")
    find_duplicates_among_issues(issues)
