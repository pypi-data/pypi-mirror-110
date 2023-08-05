import os
from aheadworks_release_manager.api.release_manager import ReleaseManager
from aheadworks_core.model.data.jira import JiraConfig


class Console:
    """
    this application needed next env variables
    JIRA_USER_EMAIL
    JIRA_TOKEN
    """

    def __init__(self):
        jira_config = JiraConfig(os.getenv('JIRA_USER_EMAIL'), os.getenv('JIRA_TOKEN'))
        self.release_manager = ReleaseManager(jira_config)

    # Release manager
    def send_pack_to_manual_release(self, jql, discord_bot_url, path_to_files):
        try:
            self.release_manager.send_pack_to_manual_release(jql, discord_bot_url, path_to_files)
            exit_code = 0
        except Exception as error:
            print('Error: ' + repr(error))
            exit_code = 1

        exit(exit_code)
