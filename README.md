# Solana Transaction Providers

Structured notes for Solana transaction landing / MEV-aware sender providers.

This repository is a public reference dataset. It is not an SDK and it does not contain API keys.

The provider list is based on https://circular.fi/providers and updated manually when I notice new providers. Thanks to Circular and to all listed providers for building and maintaining these products.

## Providers

| File | Provider | Notes |
| --- | --- | --- |
| `0slot.json` | 0slot | SWQoS, anti-MEV, binary endpoint |
| `astralane.json` | Astralane | Iris, bundles, batch, QUIC |
| `aura.json` | AURA | JSON-RPC, bundle, batch, binary, QUIC |
| `blocklander.json` | Blocklander | RPC-like `sendTransaction`, dynamic tip wallets |
| `blockrazor.json` | BlockRazor | HTTP/gRPC, sandwich mitigation |
| `blocksprint.json` | BlockSprint | transactions, bundles, QUIC |
| `bloxroute.json` | bloXroute | Trader API, submit-only regions, bundles |
| `circular.json` | Circular Fast | FAST endpoint, SWQoS + Jito routing |
| `corvus-falcon.json` | Corvus Falcon | Falcon sender, binary/plaintext/QUIC |
| `everstake.json` | Everstake SWQoS | HTTP/HTTPS and QUIC path |
| `flashblock.json` | FlashBlock | Solana sender, batch, binary protocol |
| `glaive.json` | Glaive | JSON-RPC, plain, binary, QUIC |
| `helius.json` | Helius Sender | Sender API, priority fee API |
| `hellomoon.json` | HelloMoon Lunar Lander | send, binary, bundle, batch |
| `jito.json` | Jito Block Engine | transactions, bundles, tip floor |
| `lightbridge.json` | LightBridge | JSON, binary, batch, CORS |
| `merkle.json` | Merkle QuickSlot (now Blink Labs) | QuickSlot, SVM RPC, status, gas sponsorship |
| `nextblock.json` | NextBlock | HTTP/gRPC/QUIC, bundles, tip floor |
| `node1.json` | Node1 | Regional sender endpoints |
| `raiden.json` | Raiden | HTTP sender and QUIC |
| `soyas.json` | Soyas | Private QUIC landing |
| `stellium.json` | Stellium | URL-path auth sender |
| `syncro.json` | P2P.org Syncro Sender | Public/private sender modes |
| `temporal.json` | Temporal Nozomi | JSON-RPC, v2, batch, tip floor |
| `zan.json` | ZAN Trading Boost | Tips mode, HTTP/HTTPS, QUIC |

## Stack Aliases

Some benchmark feeds use short names. These aliases are intentionally normalized in the JSON filenames:

| Feed label | JSON file |
| --- | --- |
| `BLOX` | `bloxroute.json` |
| `FAST` | `circular.json` |
| `SENDER` | `helius.json` |
| `NODEONE` | `node1.json` |
| `RAZOR` | `blockrazor.json` |
| `FALCON` | `corvus-falcon.json` |
| `LUNAR` | `hellomoon.json` |
| `SYNCRON` | `syncro.json` |

## Schema Notes

The files are descriptive JSON, not a strict schema yet. Common top-level fields:

- `name`, `website`, `docs`
- `api_key`
- `tip_wallets`, `min_tip_lamports`, `min_tip_sol`
- `endpoints`
- `methods`
- `features`
- `rate_limits`
- `error_codes`
- `best_practices`
- `notes`

Transport support differs widely by provider: JSON-RPC, raw HTTP binary, plaintext body, batch, bundle, QUIC, gRPC and WebSocket are all represented where documented.
