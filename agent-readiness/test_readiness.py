import json
import unittest
from unittest.mock import MagicMock, patch
from readiness import CloudGPUReadinessTool, MAX_BYTES

class DiscoveryBoundaryTests(unittest.TestCase):
    def invoke(self, payload):
        response = MagicMock(status=200)
        response.read.return_value = payload
        response.__enter__.return_value = response
        with patch('readiness.urlopen', return_value=response) as request:
            result = json.loads(CloudGPUReadinessTool()._run('causal_lm_lora'))
            self.assertEqual(request.call_args.args[0].get_method(), 'GET')
        return result

    def test_preserves_unknown_reliability_and_known_issues(self):
        data = {'read_only': True, 'authentication_required': False,
                'reliability': {'task_success_rate': None},
                'known_issues': [{'status': 'investigating'}]}
        result = self.invoke(json.dumps(data).encode())
        self.assertIsNone(result['reliability']['task_success_rate'])
        self.assertEqual(result['known_issues'], data['known_issues'])
        self.assertFalse(result['paid_work_approved'])

    def test_changed_authorization_contract_fails_closed(self):
        result = self.invoke(b'{"read_only": false, "authentication_required": true}')
        self.assertEqual(result['status'], 'unavailable')
        self.assertFalse(result['paid_work_approved'])

    def test_invalid_json_fails_closed(self):
        self.assertEqual(self.invoke(b'<html>unavailable</html>')['status'], 'unavailable')

    def test_oversized_response_fails_closed(self):
        self.assertEqual(self.invoke(b'x' * (MAX_BYTES + 1))['status'], 'unavailable')

if __name__ == '__main__':
    unittest.main()
