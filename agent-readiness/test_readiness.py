import json
import unittest
from unittest.mock import MagicMock, patch
from readiness import CloudGPUReadinessTool, CloudGPUEstimateTool, MAX_BYTES

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

class EstimateBoundaryTests(unittest.TestCase):
    def test_estimate_preserves_scope_and_never_grants_spending(self):
        response = MagicMock(status=200)
        response.__enter__.return_value = response
        response.read.return_value = json.dumps({'object': 'compute.quote', 'price_guarantee': 'estimate',
            'quote_scope': 'minute-source estimates only', 'candidates': [{'gpu_model': 'example',
            'billing_increment_seconds': 60, 'minimum_billed_seconds': 60, 'estimated_total_cost': .1}]}).encode()
        with patch('readiness.urlopen', return_value=response) as request:
            result = json.loads(CloudGPUEstimateTool()._run())
            req = request.call_args.args[0]
            self.assertEqual(req.full_url, 'https://cloudgpu.app/v1/quotes')
            self.assertEqual(req.get_method(), 'POST')
            self.assertIsNone(req.get_header('Authorization'))
        self.assertFalse(result['paid_work_approved'])
        self.assertFalse(result['gpu_reserved'])
        self.assertEqual(result['quote_scope'], 'minute-source estimates only')

    def test_invalid_limits_never_reach_network(self):
        with patch('readiness.urlopen') as request:
            result = json.loads(CloudGPUEstimateTool()._run(max_budget_usd=-1))
            request.assert_not_called()
        self.assertEqual(result['status'], 'unavailable')
        self.assertFalse(result['paid_work_approved'])

    def test_unexpected_contract_is_not_an_estimate(self):
        response = MagicMock(status=200)
        response.__enter__.return_value = response
        response.read.return_value = b'{"object":"gpu.instance","candidates":[]}'
        with patch('readiness.urlopen', return_value=response):
            result = json.loads(CloudGPUEstimateTool()._run())
        self.assertEqual(result['status'], 'unavailable')
        self.assertFalse(result['gpu_reserved'])

if __name__ == '__main__':
    unittest.main()
