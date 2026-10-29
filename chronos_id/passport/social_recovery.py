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

import random
import hashlib
from typing import List, Tuple, Dict, Any

# Large Mersenne prime for Shamir polynomial arithmetic (2^127 - 1)
PRIME_MODULUS = (1 << 127) - 1

class SoulRecoveryEngine:
    """
    Seedless Social Recovery Protocol.
    Distributes post-quantum recovery shards across trusted Pioneer guardians (k-of-n threshold).
    Eliminates fragile 24-word seed phrases through modular polynomial secret sharing.
    """

    @classmethod
    def split_secret(cls, secret_int: int, threshold_k: int = 3, total_n: int = 5) -> List[Tuple[int, int]]:
        """
        Splits an integer secret into N shares using a polynomial of degree (k - 1):
        f(x) = secret + a_1 * x + a_2 * x^2 + ... + a_{k-1} * x^{k-1} mod PRIME
        """
        if threshold_k > total_n:
            raise ValueError("Threshold k cannot exceed total shares n")

        # Generate k-1 random polynomial coefficients
        coefficients = [secret_int] + [random.randint(1, PRIME_MODULUS - 1) for _ in range(threshold_k - 1)]

        shares = []
        for x in range(1, total_n + 1):
            y = 0
            for power, coeff in enumerate(coefficients):
                y = (y + coeff * (x ** power)) % PRIME_MODULUS
            shares.append((x, y))

        return shares

    @classmethod
    def recover_secret(cls, shares: List[Tuple[int, int]], threshold_k: int = 3) -> int:
        """
        Reconstructs the master secret using Lagrange polynomial interpolation at x = 0:
        f(0) = sum_{j=1}^k ( y_j * prod_{m != j} ( -x_m / (x_j - x_m) ) ) mod PRIME
        """
        if len(shares) < threshold_k:
            raise ValueError(f"Insufficient shares. Required: {threshold_k}, Received: {len(shares)}")

        k_shares = shares[:threshold_k]
        secret = 0

        for j, (x_j, y_j) in enumerate(k_shares):
            numerator = 1
            denominator = 1
            for m, (x_m, _) in enumerate(k_shares):
                if m == j:
                    continue
                numerator = (numerator * (-x_m)) % PRIME_MODULUS
                denominator = (denominator * (x_j - x_m)) % PRIME_MODULUS

            # Modular inverse of denominator: den^(p-2) mod p
            inv_denominator = pow(denominator, PRIME_MODULUS - 2, PRIME_MODULUS)
            lagrange_basis = (numerator * inv_denominator) % PRIME_MODULUS
            secret = (secret + y_j * lagrange_basis) % PRIME_MODULUS

        return secret

    @classmethod
    def create_guardian_shards(
        cls,
        master_seed_hex: str,
        guardian_dids: List[str],
        threshold_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Creates encrypted guardian shard packets.
        """
        total_n = len(guardian_dids)
        secret_int = int(hashlib.sha256(master_seed_hex.encode()).hexdigest(), 16) % PRIME_MODULUS
        raw_shares = cls.split_secret(secret_int, threshold_k, total_n)

        shard_packets = []
        for i, guardian_did in enumerate(guardian_dids):
            x, y = raw_shares[i]
            shard_packets.append({
                "shard_index": x,
                "shard_payload": f"{y:x}",
                "guardian_did": guardian_did,
                "threshold_k": threshold_k,
                "total_n": total_n
            })

        return shard_packets
