from loguru import logger
import click
import requests, json

from solidityscan_agent.config import Config
from solidityscan_agent.constants import HOST, HOST_API
from solidityscan_agent.exceptions import ReportGenerationFailed


class Report:
    def __init__(self, project_id, scan_id, scan_type):
        self.project_id = project_id
        self.scan_id = scan_id
        self.scan_type = scan_type

    @property
    def generate_report_host_url(self):
        return f"{HOST_API}/api-generate-report/"

    def make_headers(self, token):
        return {
            "Authorization": f"Bearer {token}"
        }

    def generate_report_url(self, report_id):
        return f"{HOST}/report/{self.scan_type}/{self.project_id}/{report_id}"

    def generate_report(self, token=None):
        if not token:
            token = Config.get_token_from_config()

        headers = self.make_headers(token)
        body = {
            "project_id": self.project_id,
            "scan_id": self.scan_id,
        }
        url = self.generate_report_host_url

        response = requests.post(url, json=body, headers=headers)
        json_response = json.loads(response.text)
        if not json_response.get("report_id", None):
            raise ReportGenerationFailed()
        response = {
            "url": self.generate_report_url(json_response.get("report_id")),
            "success": True,
        }
        click.echo(response)
        return json_response
