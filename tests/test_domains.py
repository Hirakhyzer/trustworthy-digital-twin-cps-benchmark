import unittest
from twinsec.domains.registry import DOMAIN_PROFILES, make_domain

class DomainTests(unittest.TestCase):
    def test_all_domains_step(self):
        self.assertEqual(len(DOMAIN_PROFILES), 7)
        for name in DOMAIN_PROFILES:
            d = make_domain(name)
            state = d.step(0)
            self.assertEqual(set(state), set(d.profile.signals))
