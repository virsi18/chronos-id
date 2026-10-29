import unittest
from chronos_id.crypto.dilithium_lattice import DilithiumLatticeEngine

class TestDilithiumLattice(unittest.TestCase):
    def test_keypair_generation(self):
        pk, sk = DilithiumLatticeEngine.generate_keypair()
        self.assertEqual(pk["algorithm"], "CRYSTALS-Dilithium-5")
        self.assertEqual(pk["nist_security_level"], 5)
        self.assertTrue(len(pk["public_vector_t1"]) > 0)
        self.assertTrue(len(sk["secret_s1"]) > 0)

    def test_sign_and_verify(self):
        pk, sk = DilithiumLatticeEngine.generate_keypair()
        message = "GCV_314159_POST_QUANTUM_TRANSACTION"
        sig = DilithiumLatticeEngine.sign(message, sk, pk)

        # Verification succeeds with matching message
        valid = DilithiumLatticeEngine.verify(message, sig, pk)
        self.assertTrue(valid)

        # Verification fails if message is tampered
        tampered = DilithiumLatticeEngine.verify(message + "_TAMPERED", sig, pk)
        self.assertFalse(tampered)

if __name__ == "__main__":
    unittest.main()
