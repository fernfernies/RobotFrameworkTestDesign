import os
import json
import requests

from collections import Counter

class RobotListener(object):
    ROBOT_LISTENER_API_VERSION = 3
    HEADERS = {'Content-Type': 'application/json'}

    def __init__(self, webhook_url, channel, icon=':squirrel:'):
        self.webhook_url = webhook_url
        self.channel = channel
        self.icon = icon
        self._suite_status = dict()
        self._test_status = dict()

    def end_test(self, data, result):
        self._test_status[data] = result.passed

    def end_suite(self, data, result):
        self._suite_status[data] = self._test_status
        self._test_status = dict()

    def close(self):
        attachments = self._build_overall_results_attachment()
        self._send_slack_request(attachments)

    def _build_overall_results_attachment(self):
        results = {k: v for test_results in self._suite_status.values() for k, v in test_results.iteritems()}
        return [
        {
            "pretext": "*All Results*",
            "color": "good" if all(results.values()) else "danger",
            "mrkdwn_in": [
                "pretext"
            ],
            "fields": [
                {
                    "title": "Tests Passed",
                    "value": Counter(results.values())[True],
                    "short": True
                },
                {
                    "title": "Total Tests",
                    "value": len(results.values()),
                    "short": True
                },
                {
                    "title": "Pass Percentage",
                    "value": "{0:.2f}%".format(float((Counter(results.values())[True])/float(len(results))) * 100),
                    "short": True
                },
                {
                    "title": "Results",
                    "value": os.environ['bamboo_resultsUrl'],
                    "short": True} if os.environ.get('bamboo_resultsUrl', False) else None,
            ],
        }]

    def _send_slack_request(self, attachments):
        try:
            data = {"channel": "@{0}".format(self.channel), "username": "ufgatestbot", "attachments": attachments,
                "icon_emoji": self.icon}

            response = requests.post(url=self.webhook_url, data=json.dumps(data), headers=self.HEADERS)
            if response.status_code != 200:
                print 'Error in sending data to Slack - Status Code: {0}, Text: {1}'.format(response.status_code,
                                                                                        response.content)
        except Exception as e:
            print str(e)
