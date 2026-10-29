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

# ==============================================================================
# POST-QUANTUM LATTICE PARAMETERS (CRYSTALS-DILITHIUM-5 EQUIVALENCE)
# ==============================================================================
# Ring polynomial dimension: R_q = Z_q[X] / (X^n + 1)
LATTICE_DIMENSION_N = 256
LATTICE_PRIME_MODULUS_Q = 8380417         # 2^23 - 2^13 + 1
SECURITY_LEVEL_NIST = 5                    # 256-bit quantum post-quantum security
GAMMA1 = 524288                           # 2^19
GAMMA2 = (LATTICE_PRIME_MODULUS_Q - 1) // 32

# ==============================================================================
# PROOF OF UNIQUE PERSONHOOD (PoUP) & ZERO-KNOWLEDGE PRIVACY
# ==============================================================================
ZK_HASH_ROUNDS = 64
PERSONHOOD_NULLIFIER_DOMAIN = "CHRONOS_POUP_V1"

# ==============================================================================
# GCV SOVEREIGN PIONEER CLEARANCE
# ==============================================================================
# Pioneer sovereign credentials unlock verified participation in Tier-1 GCV barter.
# Standard baseline transaction clearance: $314,159.00 USD per 1.00 Pi
PI_GCV_SOVEREIGN_ANCHOR_USD = 314159.00
MAX_TIER_1_BARTER_LIMIT_USD = PI_GCV_SOVEREIGN_ANCHOR_USD

# ==============================================================================
# SOUL-RECOVERY SOCIAL RECOVERY CONFIGURATION
# ==============================================================================
DEFAULT_RECOVERY_THRESHOLD_K = 3           # Minimum guardian shards required
DEFAULT_RECOVERY_TOTAL_N = 5               # Total guardian shards distributed
SHARD_EXPIRY_DAYS = 90
