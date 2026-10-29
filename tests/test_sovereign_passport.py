import unittest
from chronos_id.crypto.dilithium_lattice import DilithiumLatticeEngine
from chronos_id.crypto.zk_personhood import ZkPersonhoodEngine
from chronos_id.passport.sovereign_passport import ChronosPassport
from chronos_id.registry.identity_mesh import SovereignIdentityMesh
from chronos_id.constants import PI_GCV_SOVEREIGN_ANCHOR_USD

class TestSovereignPassport(unittest.TestCase):
    def test_passport_lifecycle(self):
        pk, sk = DilithiumLatticeEngine.generate_keypair()
        zk_proof = ZkPersonhoodEngine.generate_personhood_proof("BIOMETRIC_PIONEER_TEST")

        passport = ChronosPassport(
            passport_did="did:chronos:pi:test_pioneer",
            nullifier_hash=zk_proof["personhood_nullifier"],
            lattice_public_key=pk,
            zk_proof=zk_proof,
            guardian_ring=["g1", "g2", "g3"]
        )

        self.assertEqual(passport.gcv_barter_limit_usd, PI_GCV_SOVEREIGN_ANCHOR_USD)
        self.assertEqual(passport.gcv_clearance_tier, "TIER_1_SOVEREIGN_PIONEER")

        # Transaction authorization
        msg = "BARTER::TESLA_MODEL_3::42000_USD"
        auth = passport.attest_transaction_authorization(msg, sk)
        self.assertTrue(passport.verify_authorization(msg, auth["signature"]))

        # Registry enrollment
        mesh = SovereignIdentityMesh()
        registered, reason = mesh.register_passport(passport)
        self.assertTrue(registered)
        self.assertEqual(mesh.total_gcv_clearance_volume_usd, PI_GCV_SOVEREIGN_ANCHOR_USD)

if __name__ == "__main__":
    unittest.main()
