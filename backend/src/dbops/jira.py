import httpx
from src.errors import (
    JiraUnavailableError,
    JiraAuthError,
    InvalidIssueError
)

class JiraClient:
    def __init__(self, http_client: httpx.Client, jira_url: str, headers: dict):
        self.http = http_client
        self.jira_url = jira_url.rstrip("/")
        self.headers = headers

    def get_issue(self, issue_key: str) -> dict:
        try:
            response = self.http.get(
                f"{self.jira_url}/rest/api/3/issue/{issue_key}",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            status = e.response.status_code

            if status in (401, 403):
                raise JiraAuthError() from e

            if status == 404:
                raise InvalidIssueError(
                    f"Jira issue {issue_key} not found"
                ) from e

            if status >= 500:
                raise JiraUnavailableError() from e

            raise

        except httpx.RequestError as e:
            raise JiraUnavailableError(
                "Network error while contacting Jira"
            ) from e

    def update_issue(self, issue_key: str, payload: dict) -> dict:
        try:
            response = self.http.put(
                f"{self.jira_url}/rest/api/3/issue/{issue_key}/comment",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json() if response.text else {}

        except Exception as e:
            raise JiraUnavailableError(f"Failed to update issue {issue_key}") from e


    def add_comment(self, issue_key: str, comment: str) -> dict:
        """
        Adds a comment to a Jira issue.

        :param issue_key: The Jira issue key (e.g., "PROJ-123").
        :param comment: The comment text to post.
        :param visibility_role: Optional Jira role for comment visibility (e.g., "Administrators").
        :return: JSON response from Jira API.
        """
        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": comment}
                        ],
                    }
                ],
            }
        }

        try:
            response = self.http.post(
                f"{self.jira_url}/rest/api/3/issue/{issue_key}/comment",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            status = e.response.status_code

            if status in (401, 403):
                raise JiraAuthError() from e

            if status == 404:
                raise InvalidIssueError(f"Jira issue {issue_key} not found") from e

            if status >= 500:
                raise JiraUnavailableError() from e

            raise

        except httpx.RequestError as e:
            raise JiraUnavailableError("Network error while contacting Jira") from e
        #curl -D- -u fred:fred -X POST --data {see below} -H "Content-Type: application/json" http://kelpie9:8081/rest/api/2/issue/QA-31/comment

    def move_to_inprogress(self, issue_key: str, comment: str = None):
        """
        Moves a Jira ticket to 'In Progress' if possible.
        """
        transitions = self.get_transitions(issue_key)

        # Find a transition where target status name is "In Progress"
        inprogress_transition = next(
            (t for t in transitions if t["to"]["name"].lower() == "in progress"),
            None
        )

        if not inprogress_transition:
            raise Exception(f"No 'In Progress' transition available for {issue_key}")

        payload = {"transition": {"id": inprogress_transition["id"]}}

        # Add comment if provided
        if comment:
            payload["update"] = {
                "comment": [
                    {
                        "add": {
                            "body": {
                                "type": "doc",
                                "version": 1,
                                "content": [
                                    {
                                        "type": "paragraph",
                                        "content": [
                                            {"type": "text", "text": comment}
                                        ],
                                    }
                                ],
                            }
                        }
                    }
                ]
            }

        response = self.http.post(
            f"{self.jira_url}/rest/api/3/issue/{issue_key}/transitions",
            headers=self.headers,
            json=payload,
        )

        if response.status_code >= 400:
            raise Exception(
                f"Failed to move Jira ticket {issue_key} to In Progress\n"
                f"Status: {response.status_code}\n"
                f"Response: {response.text}"
            )

        return True


    def get_transitions(self, issue_key: str) -> list:
        try:
            response = self.http.get(
                f"{self.jira_url}/rest/api/3/issue/{issue_key}/transitions",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json().get("transitions", [])

        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            if status in (401, 403):
                raise JiraAuthError() from e
            if status == 404:
                raise InvalidIssueError(f"Jira issue {issue_key} not found") from e
            if status >= 500:
                raise JiraUnavailableError() from e
            raise

        except httpx.RequestError as e:
            raise JiraUnavailableError("Network error while contacting Jira") from e


    def close_ticket(self, issue_key: str, comment: str = None) -> bool:
        """
        Closes a Jira ticket by performing the 'Done' transition.

        :param issue_key: Jira issue key, e.g., "XWITO-44020"
        :param comment: Optional comment to add while closing
        :return: True if successful
        """
        # Step 1: Get valid transitions
        transitions = self.get_transitions(issue_key)
        print(transitions)

        # Step 2: Pick transition to 'done'
        done_transition = next(
            (t for t in transitions if t["to"]["statusCategory"]["key"] == "done"),
            None
        )
        if not done_transition:
            raise Exception(f"No 'done' transition available for {issue_key}")

        payload = {"transition": {"id": done_transition["id"]}}

        # Step 3: Add comment in Atlassian Document Format if provided
        if comment:
            payload["update"] = {
                "comment": [
                    {
                        "add": {
                            "body": {
                                "type": "doc",
                                "version": 1,
                                "content": [
                                    {
                                        "type": "paragraph",
                                        "content": [
                                            {"type": "text", "text": comment}
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                ]
            }

        # Step 4: Post the transition
        response = self.http.post(
            f"{self.jira_url}/rest/api/3/issue/{issue_key}/transitions",
            headers=self.headers,
            json=payload
        )

        if response.status_code >= 400:
            raise Exception(
                f"Failed to close Jira ticket {issue_key}\n"
                f"Status: {response.status_code}\n"
                f"Response: {response.text}"
            )

        return True


"""
    def transition_issue(self, issue_key: str, transition_id: str) -> dict:
        try:
            payload = {
                "transition": {"id": transition_id},
                "fields": {
                    "resolution": {"name": "Done"}
                },
                "update": {
                    "comment": [
                        {
                            "add": {
                                "body": {
                                    "type": "doc",
                                    "version": 1,
                                    "content": [
                                        {
                                            "type": "paragraph",
                                            "content": [
                                                {
                                                    "type": "text",
                                                    "text": "Closing ticket: DB Provisioning completed by automation"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                    ]
                }
            }
            response = self.http.post(
                f"{self.jira_url}/rest/api/3/issue/{issue_key}/transitions",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json() if response.text else {}

        except httpx.HTTPStatusError as e:
            status = e.response.status_code

            if status in (401, 403):
                raise JiraAuthError() from e

            if status == 404:
                raise InvalidIssueError(f"Jira issue {issue_key} not found") from e

            if status >= 500:
                raise JiraUnavailableError() from e

            raise

        except httpx.RequestError as e:
            raise JiraUnavailableError("Network error while contacting Jira") from e
"""

class JiraTicketDetails:
    def __init__(self, issue_json: dict):
        fields = issue_json["fields"]

        self.jirat_ticket = issue_json["key"]
        self.jirat_summary = fields["summary"]
        self.jirat_status = fields["status"]["name"]
        self.jirat_created = fields["created"]
        self.jirat_issue_type = fields["issuetype"]["name"] if fields.get("issuetype") else None
        self.jirat_assignee = fields["assignee"]["displayName"] if fields.get("assignee") else None
        self.jirat_num_sites = str(int(float(fields.get("customfield_10851")))) if fields.get("customfield_10851") is not None else None
        self.jirat_desktop_licenses = str(int(float(fields.get("customfield_10856")))) if fields.get("customfield_10856") is not None else None
        self.jirat_mobile_licenses = str(int(float(fields.get("customfield_10852")))) if fields.get("customfield_10852") is not None else None
        self.jirat_db_name = fields.get("customfield_10424")
        self.jirat_src_app_type = fields.get("customfield_10860", {}).get("value")
        self.jirat_company_name = fields.get("customfield_10779")
        self.jirat_company_address = fields.get("customfield_10584")
        self.jirat_reporter = fields["reporter"]["displayName"] if fields.get("reporter") else None

    def validate_for_provisioning(self):
        if not self.database_name:
            raise InvalidIssueError("Database name is required")

        if not self.num_sites:
            raise InvalidIssueError("Number of sites is required")