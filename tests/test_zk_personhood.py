import unittest
from chronos_id.crypto.zk_personhood import ZkPersonhoodEngine

class TestZkPersonhood(unittest.TestCase):
    def test_personhood_proof_generation_and_verification(self):
        biometric = "BIOMETRIC_FEATURE_IRIS_HASH_999"
        proof = ZkPersonhoodEngine.generate_personhood_proof(biometric)
        self.assertTrue(proof["is_verified_unique"])
        self.assertTrue(len(proof["personhood_nullifier"]) > 0)

        seen_nullifiers = set()
        valid, reason = ZkPersonhoodEngine.verify_personhood_proof(proof, seen_nullifiers)
        self.assertTrue(valid)
        self.assertEqual(reason, "UNIQUE_BIOLOGICAL_PERSONHOOD_CERTIFIED")

    def test_sybil_duplicate_rejection(self):
        biometric = "SAME_PERSON_DUPLICATE_ATTEMPT"
        proof1 = ZkPersonhoodEngine.generate_personhood_proof(biometric)
        seen_nullifiers = {proof1["personhood_nullifier"]}

        # Second proof from same person generates identical nullifier
        proof2 = ZkPersonhoodEngine.generate_personhood_proof(biometric)
        valid, reason = ZkPersonhoodEngine.verify_personhood_proof(proof2, seen_nullifiers)
        self.assertFalse(valid)
        self.assertEqual(reason, "SYBIL_DUPLICATE_IDENTITY_DETECTED")

if __name__ == "__main__":
    unittest.main()
