from aheadworks_core.model.http.api_request import ApiRequest as Api
import json


class JiraApiManager:
    """api manager for jira"""

    def __init__(self, config):
        self.config = config
        self.request = Api(config=self.config)

    def search_tasks_jql(self, jql):
        headers = {
            "Accept": "application/json"
        }
        url = '/rest/api/3/search?jql={}'.format(jql)
        data = self.request.request(location=url, headers=headers)

        return json.loads(data)

    def add_attachments_to_task(self, task_key, files):
        headers = {
            "Accept": "application/json",
            'X-Atlassian-Token': 'nocheck'
        }
        url = '/rest/api/3/issue/{}/attachments'.format(task_key)
        data = self.request.request(location=url, headers=headers, method='POST', files=files)

        return json.loads(data)
