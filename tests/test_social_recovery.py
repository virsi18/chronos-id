import unittest
from chronos_id.passport.social_recovery import SoulRecoveryEngine, PRIME_MODULUS

class TestSocialRecovery(unittest.TestCase):
    def test_shamir_3_of_5_recovery(self):
        secret = 1234567890987654321
        threshold_k = 3
        total_n = 5

        shares = SoulRecoveryEngine.split_secret(secret, threshold_k, total_n)
        self.assertEqual(len(shares), 5)

        # Recover using exactly 3 shares (shares 1, 3, 5)
        subset_3 = [shares[0], shares[2], shares[4]]
        recovered = SoulRecoveryEngine.recover_secret(subset_3, threshold_k)
        self.assertEqual(recovered, secret)

        # Recover using another subset of 3 shares (shares 2, 3, 4)
        subset_other = [shares[1], shares[2], shares[3]]
        recovered_other = SoulRecoveryEngine.recover_secret(subset_other, threshold_k)
        self.assertEqual(recovered_other, secret)

    def test_insufficient_shares_fails(self):
        secret = 9999999
        shares = SoulRecoveryEngine.split_secret(secret, threshold_k=3, total_n=5)
        
        # Only 2 shares provided
        with self.assertRaises(ValueError):
            SoulRecoveryEngine.recover_secret(shares[:2], threshold_k=3)

if __name__ == "__main__":
    unittest.main()
