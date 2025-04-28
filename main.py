from modules.jira_client import fetch_jira_issues
from modules.duplicate_checker import find_duplicates_among_issues
from config import JQL_QUERY
from setup_logger import setup_logger

if __name__ == "__main__":
    logger = setup_logger()

    logger.info("[STEP 1] Jira 이슈 목록 가져오는 중...")
    issues = fetch_jira_issues(JQL_QUERY)
    logger.info(f"[STEP 2] {len(issues)}개의 이슈를 불러왔습니다.")

    logger.info("\n[STEP 3] Jira 이슈 간 중복 확인 시작...\n")
    find_duplicates_among_issues(issues, logger=logger)
