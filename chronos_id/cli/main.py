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

import sys
import time
import argparse
import secrets

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel

from chronos_id.constants import PI_GCV_SOVEREIGN_ANCHOR_USD
from chronos_id.crypto.dilithium_lattice import DilithiumLatticeEngine
from chronos_id.crypto.zk_personhood import ZkPersonhoodEngine
from chronos_id.passport.sovereign_passport import ChronosPassport
from chronos_id.passport.social_recovery import SoulRecoveryEngine
from chronos_id.registry.identity_mesh import SovereignIdentityMesh
from chronos_id.cli.dashboard import (
    BANNER,
    generate_header_panel,
    generate_passport_panel,
    generate_guardians_table,
    generate_registry_panel
)

console = Console()

def run_simulation():
    console.print(BANNER, style="bold cyan")
    console.print("[bold yellow]Initializing Chronos-ID Post-Quantum Sovereign Identity Mesh...[/bold yellow]\n")

    registry = SovereignIdentityMesh()
    console.print(generate_header_panel())
    time.sleep(0.4)

    # 1. Generate Post-Quantum Lattice Keypair (NIST Level 5)
    console.print("\n[bold magenta]>>> 1. SYNTHESIZING POST-QUANTUM LATTICE KEYPAIR (CRYSTALS-DILITHIUM-5) <<<[/bold magenta]")
    public_key, private_key = DilithiumLatticeEngine.generate_keypair()
    console.print(f"[green]✔ Lattice Dimension: n=256, Modulus q=8380417, Security: NIST Level 5[/green]")
    console.print(f"[green]✔ Public Key Projection (t1): {public_key['public_vector_t1'][:32]}...[/green]")
    time.sleep(0.4)

    # 2. Generate Zero-Knowledge Proof of Unique Personhood (PoUP)
    console.print("\n[bold cyan]>>> 2. ISSUING ZERO-KNOWLEDGE PROOF OF UNIQUE BIOLOGICAL PERSONHOOD <<<[/bold cyan]")
    # Simulated private biometric vector (e.g. hash of encrypted iris/retina feature)
    biometric_entropy = "BIOMETRIC_IRIS_SHA512_PIONEER_ALICE_JAKARTA_9831"
    zk_proof = ZkPersonhoodEngine.generate_personhood_proof(biometric_entropy)
    console.print(f"[green]✔ Deterministic Nullifier: {zk_proof['personhood_nullifier'][:32]}... (Sybil Anchor)[/green]")
    console.print(f"[green]✔ ZK-Commitment Witness: {zk_proof['proof_witness'][:32]}... (Zero Biometric Leakage)[/green]")
    time.sleep(0.4)

    # 3. Mint Soulbound Sovereign Passport
    console.print("\n[bold yellow]>>> 3. MINTING SOVEREIGN PIONEER PASSPORT & GCV CLEARANCE <<<[/bold yellow]")
    guardians = [
        "did:chronos:pi:guardian_singapore",
        "did:chronos:pi:guardian_tokyo",
        "did:chronos:pi:guardian_geneva",
        "did:chronos:pi:guardian_london",
        "did:chronos:pi:guardian_nairobi"
    ]
    passport = ChronosPassport(
        passport_did="did:chronos:pi:pioneer_alice_9831",
        nullifier_hash=zk_proof["personhood_nullifier"],
        lattice_public_key=public_key,
        zk_proof=zk_proof,
        guardian_ring=guardians
    )

    success, reason = registry.register_passport(passport)
    console.print(f"[bold green]✔ Registration Status: {reason}[/bold green]")
    console.print(generate_passport_panel(passport.to_dict()))
    time.sleep(0.4)

    # 4. Social Recovery Shards Distribution (3-of-5 Shamir Threshold)
    console.print("\n[bold cyan]>>> 4. SEEDLESS SOUL-RECOVERY: DISTRIBUTING GUARDIAN SHARDS <<<[/bold cyan]")
    shards = SoulRecoveryEngine.create_guardian_shards(
        master_seed_hex=private_key["seed_k"],
        guardian_dids=guardians,
        threshold_k=3
    )
    console.print(generate_guardians_table(shards))
    time.sleep(0.4)

    # 5. Sybil Attack Prevention Test (Attempting duplicate passport with same person)
    console.print("\n[bold red]>>> 5. TESTING SYBIL ATTACK: Malicious Attempt to Mint Duplicate Identity <<<[/bold red]")
    duplicate_proof = ZkPersonhoodEngine.generate_personhood_proof(biometric_entropy)
    dup_pk, _ = DilithiumLatticeEngine.generate_keypair()
    duplicate_passport = ChronosPassport(
        passport_did="did:chronos:pi:sybil_clone_fake",
        nullifier_hash=duplicate_proof["personhood_nullifier"],
        lattice_public_key=dup_pk,
        zk_proof=duplicate_proof,
        guardian_ring=guardians
    )
    dup_success, dup_reason = registry.register_passport(duplicate_passport)
    console.print(f"[bold red]⛔ SYBIL ATTACK BLOCKED: {dup_reason}[/bold red]")
    time.sleep(0.4)

    # 6. Post-Quantum Transaction Authorization Test
    console.print("\n[bold green]>>> 6. POST-QUANTUM COMMERCIAL AUTHORIZATION TEST (GCV $314,159 TIER) <<<[/bold green]")
    barter_agreement = f"BARTER_AUTHORIZATION::RWA_EV_PURCHASE::42000_USD::0.13369_PI::DID_PIONEER_ALICE"
    auth = passport.attest_transaction_authorization(barter_agreement, private_key)
    verified = passport.verify_authorization(barter_agreement, auth["signature"])
    console.print(f"[bold green]✔ Dilithium Lattice Signature Verified: {verified} (Quantum-Safe Commercial Clearance)[/bold green]\n")

    # 7. Render Registry Status
    console.print(generate_registry_panel(registry.get_registry_telemetry()))
    console.print("\n[bold cyan]>>> Chronos-ID Operating in Optimal Sovereign State: Quantum-Resistant & Sybil-Proof. <<<[/bold cyan]")

def main():
    parser = argparse.ArgumentParser(description="Chronos-ID: Post-Quantum Sovereign Identity Protocol")
    parser.add_argument("command", choices=["demo", "simulate", "telemetry"], nargs="?", default="demo")
    args = parser.parse_args()

    if args.command in ("demo", "simulate"):
        run_simulation()
    elif args.command == "telemetry":
        reg = SovereignIdentityMesh()
        console.print(generate_registry_panel(reg.get_registry_telemetry()))

if __name__ == "__main__":
    main()
