import requests
from config import JIRA_URL, JIRA_USER, JIRA_TOKEN, JQL_QUERY, MAX_ISSUES

def fetch_jira_issues(jql_query):
    headers = {"Accept": "application/json"}
    auth = (JIRA_USER, JIRA_TOKEN)

    url = f"{JIRA_URL}/rest/api/2/search"
    max_results = MAX_ISSUES
    start_at = 0
    page_size = 100

    issues = []

    print(f"[INFO] Jira 이슈를 최대 {max_results}개까지 가져옵니다.")

    while start_at < max_results:
        params = {
            "jql": jql_query,
            "startAt": start_at,
            "maxResults": min(page_size, max_results - start_at),
            "fields": "summary,description"
        }

        response = requests.get(url, headers=headers, params=params, auth=auth)
        response.raise_for_status()
        data = response.json()

        fetched = len(data["issues"])
        if fetched == 0:
            break

        issues_in_page = []
        for issue in data["issues"]:
            key = issue["key"]
            summary = issue["fields"].get("summary", "")
            description = issue["fields"].get("description", "")
            full_text = (summary or "") + " " + (description or "")
            issues_in_page.append((key, full_text))

        issues.extend(issues_in_page)

        print(f"[PAGING] {start_at + 1}번부터 {start_at + fetched}번까지 이슈 로딩 완료.")

        start_at += fetched

    print(f"[INFO] 총 {len(issues)}개의 이슈를 가져왔습니다.")
    return issues
