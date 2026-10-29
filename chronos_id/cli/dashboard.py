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
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from chronos_id.constants import PI_GCV_SOVEREIGN_ANCHOR_USD

BANNER = r"""
   _____ _    _ _____   ____  _   _  ____   _____     _____ _____  
  / ____| |  | |  __ \ / __ \| \ | |/ __ \ / ____|   |_   _|  __ \ 
 | |    | |__| | |__) | |  | |  \| | |  | | (___ ______| | | |  | |
 | |    |  __  |  _  /| |  | | . ` | |  | |\___ \______| | | |  | |
 | |____| |  | | | \ \| |__| | |\  | |__| |____) |    _| |_| |__| |
  \_____|_|  |_|_|  \_\\____/|_| \_|\____/|_____/    |_____|_____/ 
   >> POST-QUANTUM SOVEREIGN PASSPORT & ZK-PERSONHOOD MESH <<
"""

def generate_header_panel() -> Panel:
    text = Text()
    text.append("CHRONOS-ID // POST-QUANTUM SOVEREIGN IDENTITY MESH\n", style="bold magenta")
    text.append("Cryptographic Standard: ", style="cyan")
    text.append("NIST Level 5 CRYSTALS-Dilithium-5 (Lattice-Based Module-LWE)\n", style="bold green")
    text.append("Privacy Architecture: ", style="cyan")
    text.append("Zero-Knowledge Unique Biological Personhood (zk-STARK Nullifiers)\n", style="bold yellow")
    text.append("Pioneer Barter Clearance: ", style="cyan")
    text.append(f"Tier-1 Sovereign Status (GCV ${PI_GCV_SOVEREIGN_ANCHOR_USD:,.2f} USD Parity Limit)\n", style="bold cyan")
    return Panel(text, title="[bold white]POST-QUANTUM IDENTITY MATRIX[/bold white]", border_style="bright_blue")

def generate_passport_panel(passport_dict: dict) -> Panel:
    text = Text()
    text.append(f"SOVEREIGN PASSPORT: {passport_dict['passport_did']}\n", style="bold yellow")
    text.append(f"  * Status:              {'ACTIVE / CERTIFIED' if passport_dict['is_active'] else 'REVOKED'}\n", style="bold green")
    text.append(f"  * Algorithm:           {passport_dict['algorithm']} (Post-Quantum)\n", style="white")
    text.append(f"  * Personhood Nullifier:{passport_dict['nullifier_hash'][:24]}... (Zero-Biometric Leak)\n", style="cyan")
    text.append(f"  * GCV Tier:            {passport_dict['gcv_clearance_tier']}\n", style="bold magenta")
    text.append(f"  * Barter Limit:        ${passport_dict['gcv_barter_limit_usd']:,.2f} USD\n", style="bold green")
    text.append(f"  * Social Guardians:    {passport_dict['guardian_count']} Trusted Pioneer Shards\n", style="yellow")
    text.append(f"  * Trust Score:         {passport_dict['reputation_score']:.1f} / 100.0\n", style="cyan")
    return Panel(text, title="[bold green]SOULBOUND SOVEREIGN CREDENTIAL[/bold green]", border_style="green")

def generate_guardians_table(shards: list) -> Table:
    table = Table(title="SOUL-RECOVERY SOCIAL GUARDIAN RING (3-of-5 THRESHOLD)", border_style="cyan")
    table.add_column("Shard #", justify="center", style="bold white")
    table.add_column("Guardian Pioneer DID", style="cyan")
    table.add_column("Encrypted Shard Payload", style="dim")
    table.add_column("Status", justify="right", style="bold green")

    for s in shards:
        table.add_row(
            f"#{s['shard_index']}",
            s["guardian_did"],
            f"{s['shard_payload'][:20]}...",
            "HELD_IN_TRUST"
        )
    return table

def generate_registry_panel(stats: dict) -> Panel:
    text = Text()
    text.append("DECENTRALIZED IDENTITY REGISTRY TELEMETRY:\n", style="bold green")
    text.append(f"  * Registered Sovereign Pioneers: {stats['total_registered_pioneers']}\n", style="white")
    text.append(f"  * Unique Nullifiers Enforced:    {stats['unique_nullifiers_tracked']}\n", style="bold yellow")
    text.append(f"  * Total GCV Clearance Pool:      ${stats['total_gcv_clearance_pool_usd']:,.2f} USD\n", style="bold cyan")
    text.append(f"  * Sybil Defense Engine:          {stats['sybil_resistance_status']}\n", style="bold green")
    return Panel(text, title="[bold cyan]GLOBAL IDENTITY MESH[/bold cyan]", border_style="cyan")
