"""
Copyright 2026 Chronos-ID Sovereign Identity Contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from typing import Dict, Any, List, Optional, Tuple
from chronos_id.passport.sovereign_passport import ChronosPassport
from chronos_id.crypto.zk_personhood import ZkPersonhoodEngine
from chronos_id.constants import PI_GCV_SOVEREIGN_ANCHOR_USD

class SovereignIdentityMesh:
    """
    Decentralized Cross-Chain Identity Registry.
    Audits Proof of Unique Personhood nullifiers and manages Pioneer sovereign barter clearance.
    """

    def __init__(self):
        self.passports: Dict[str, ChronosPassport] = {}
        self.registered_nullifiers: set = set()
        self.total_gcv_clearance_volume_usd: float = 0.0

    def register_passport(self, passport: ChronosPassport) -> Tuple[bool, str]:
        """
        Enrolls a new sovereign passport. Enforces single-personhood uniqueness via ZK nullifiers.
        """
        valid_zk, reason = ZkPersonhoodEngine.verify_personhood_proof(
            passport.zk_proof,
            self.registered_nullifiers
        )

        if not valid_zk:
            return False, f"REGISTRATION_REJECTED: {reason}"

        # Register nullifier to prevent sybil duplicate minting
        self.registered_nullifiers.add(passport.nullifier_hash)
        self.passports[passport.passport_did] = passport
        self.total_gcv_clearance_volume_usd += passport.gcv_barter_limit_usd

        return True, "PASSPORT_REGISTERED_SOVEREIGN_TIER_1"

    def get_passport(self, did: str) -> Optional[ChronosPassport]:
        return self.passports.get(did)

    def get_registry_telemetry(self) -> Dict[str, Any]:
        return {
            "total_registered_pioneers": len(self.passports),
            "unique_nullifiers_tracked": len(self.registered_nullifiers),
            "total_gcv_clearance_pool_usd": self.total_gcv_clearance_volume_usd,
            "target_gcv_per_passport": PI_GCV_SOVEREIGN_ANCHOR_USD,
            "security_standard": "POST_QUANTUM_LATTICE_DILITHIUM_5",
            "sybil_resistance_status": "ACTIVE_ZERO_KNOWLEDGE_ENFORCEMENT"
        }
