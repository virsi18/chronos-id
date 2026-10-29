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

import time
import uuid
import hashlib
from typing import Dict, Any, List, Optional
from chronos_id.constants import PI_GCV_SOVEREIGN_ANCHOR_USD
from chronos_id.crypto.dilithium_lattice import DilithiumLatticeEngine
from chronos_id.crypto.zk_personhood import ZkPersonhoodEngine

class ChronosPassport:
    """
    Soulbound Post-Quantum Decentralized Identity Document (DID).
    Integrates Dilithium lattice cryptography, ZK unique personhood,
    and GCV $314,159 barter attestation clearance.
    """

    def __init__(
        self,
        passport_did: str,
        nullifier_hash: str,
        lattice_public_key: Dict[str, Any],
        zk_proof: Dict[str, Any],
        guardian_ring: List[str]
    ):
        self.passport_did = passport_did
        self.nullifier_hash = nullifier_hash
        self.lattice_public_key = lattice_public_key
        self.zk_proof = zk_proof
        self.guardian_ring = guardian_ring
        self.reputation_score: float = 100.0
        self.gcv_clearance_tier: str = "TIER_1_SOVEREIGN_PIONEER"
        self.gcv_barter_limit_usd: float = PI_GCV_SOVEREIGN_ANCHOR_USD
        self.created_at: float = time.time()
        self.is_active: bool = True

    def attest_transaction_authorization(self, message: str, private_key: Dict[str, Any]) -> Dict[str, Any]:
        """
        Signs a commercial transaction with post-quantum lattice signature.
        """
        signature = DilithiumLatticeEngine.sign(message, private_key, self.lattice_public_key)
        return {
            "passport_did": self.passport_did,
            "signature": signature,
            "gcv_tier": self.gcv_clearance_tier,
            "gcv_limit_usd": self.gcv_barter_limit_usd
        }

    def verify_authorization(self, message: str, signature: Dict[str, Any]) -> bool:
        """
        Validates the transaction authorization against this passport's public lattice key.
        """
        if not self.is_active:
            return False
        return DilithiumLatticeEngine.verify(message, signature, self.lattice_public_key)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "passport_did": self.passport_did,
            "nullifier_hash": self.nullifier_hash,
            "public_key_t1": self.lattice_public_key.get("public_vector_t1"),
            "algorithm": self.lattice_public_key.get("algorithm"),
            "reputation_score": self.reputation_score,
            "gcv_clearance_tier": self.gcv_clearance_tier,
            "gcv_barter_limit_usd": self.gcv_barter_limit_usd,
            "guardian_count": len(self.guardian_ring),
            "created_at": self.created_at,
            "is_active": self.is_active
        }
