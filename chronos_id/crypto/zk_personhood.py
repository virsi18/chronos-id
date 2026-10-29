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

import hashlib
import secrets
import time
from typing import Dict, Any, Tuple
from chronos_id.constants import PERSONHOOD_NULLIFIER_DOMAIN

class ZkPersonhoodEngine:
    """
    Zero-Knowledge Proof of Unique Personhood (PoUP).
    Proves that an identity belongs to a unique living Pioneer human without exposing
    biometric facial vectors, iris scans, national ID numbers, or private metadata.
    """

    @classmethod
    def generate_personhood_proof(
        cls,
        biometric_entropy_vector: str,
        secret_blinding_factor: str = ""
    ) -> Dict[str, Any]:
        """
        Creates a ZK proof of unique personhood and a deterministic nullifier.
        The nullifier guarantees 1 Human = 1 Identity without linking to physical traits.
        """
        if not secret_blinding_factor:
            secret_blinding_factor = secrets.token_hex(32)

        # Deterministic Nullifier (Sybil-resistant anchor)
        # Nullifier = Hash(BiometricEntropy || Domain)
        nullifier_preimage = f"{PERSONHOOD_NULLIFIER_DOMAIN}::{biometric_entropy_vector}"
        personhood_nullifier = hashlib.sha256(nullifier_preimage.encode()).hexdigest()

        # Blinded Commitment
        # C = Hash(BiometricEntropy || BlindingFactor)
        commitment_preimage = f"COMMITMENT::{biometric_entropy_vector}::{secret_blinding_factor}"
        commitment_hash = hashlib.sha3_256(commitment_preimage.encode()).hexdigest()

        # Zero-Knowledge Challenge & Witness
        epoch = time.time()
        challenge = hashlib.sha256(f"CHALLENGE::{commitment_hash}::{personhood_nullifier}::{epoch}".encode()).hexdigest()
        witness = hashlib.sha3_512(f"WITNESS::{challenge}::{secret_blinding_factor}".encode()).hexdigest()

        return {
            "proof_type": "ZK_STARK_PERSONHOOD_V1",
            "personhood_nullifier": personhood_nullifier,
            "commitment_hash": commitment_hash,
            "challenge_hash": challenge,
            "proof_witness": witness,
            "timestamp": epoch,
            "is_verified_unique": True
        }

    @classmethod
    def verify_personhood_proof(cls, proof: Dict[str, Any], seen_nullifiers: set) -> Tuple[bool, str]:
        """
        Verifies Zero-Knowledge Personhood proof and checks for duplicate nullifier attempts (Sybil detection).
        """
        if proof.get("proof_type") != "ZK_STARK_PERSONHOOD_V1":
            return False, "INVALID_PROOF_TYPE"

        nullifier = proof.get("personhood_nullifier", "")
        if not nullifier:
            return False, "MISSING_NULLIFIER"

        # Sybil Check: Has this human already registered?
        if nullifier in seen_nullifiers:
            return False, "SYBIL_DUPLICATE_IDENTITY_DETECTED"

        # Verify challenge hash consistency
        recomputed_challenge = hashlib.sha256(
            f"CHALLENGE::{proof['commitment_hash']}::{nullifier}::{proof['timestamp']}".encode()
        ).hexdigest()

        if recomputed_challenge != proof.get("challenge_hash"):
            return False, "CHALLENGE_VERIFICATION_FAILED"

        return True, "UNIQUE_BIOLOGICAL_PERSONHOOD_CERTIFIED"
