#!/usr/bin/env python3
"""
Generate the ENDPOINTS-TipsWallets_ONLY quick-reference from the root provider JSON files.

This folder is a DERIVED artifact: every value here comes from the per-provider JSON
files in the repository root. Do not edit the files under json/ or markdown/ by hand —
edit the root JSON and re-run this script:

    python3 ENDPOINTS-TipsWallets_ONLY/generate_quickref.py

It writes, for each provider, a slimmed `json/<provider>.json` and a human-friendly
`markdown/<provider>.md` containing only: name, auth (where to put the key), min tip,
tip wallets, and a flattened list of endpoints.
"""

import json
import os
import re
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
JSON_OUT = os.path.join(HERE, "json")
MD_OUT = os.path.join(HERE, "markdown")

# A base58 Solana pubkey: 32-44 chars, base58 alphabet (no 0 O I l).
PUBKEY_RE = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")
# Something that looks like a connectable endpoint: a URL, a host.tld, or host:port.
URL_RE = re.compile(r"^(https?://|wss?://|udp://|grpc://)", re.I)
HOST_RE = re.compile(r"^[A-Za-z0-9._-]+\.[A-Za-z]{2,}(:\d+)?(/.*)?$")
IPPORT_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}(:\d+)?$")

# Keys whose string values are descriptions/notes, not real endpoints — skip them.
SKIP_LABEL_SUBSTR = ("note", "_note", "guidance", "description", "example_curl",
                     "how_to_get", "format", "info")


def looks_like_endpoint(value: str) -> bool:
    v = value.strip()
    if " " in v:  # endpoints don't contain spaces; prose does
        return False
    return bool(URL_RE.match(v) or IPPORT_RE.match(v) or HOST_RE.match(v))


def looks_like_pubkey(value: str) -> bool:
    return bool(PUBKEY_RE.match(value.strip()))


def flatten_endpoints(node, prefix=""):
    """Recursively yield (label, url) for every endpoint-looking string under `node`."""
    out = []
    if isinstance(node, dict):
        for k, v in node.items():
            if any(s in k.lower() for s in SKIP_LABEL_SUBSTR):
                continue
            label = f"{prefix}.{k}" if prefix else k
            out.extend(flatten_endpoints(v, label))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            out.extend(flatten_endpoints(v, f"{prefix}[{i}]"))
    elif isinstance(node, str):
        if looks_like_endpoint(node):
            out.append((prefix, node.strip()))
    return out


def collect_tip_wallets(d):
    """Collect every base58 pubkey under any top-level key matching tip_wallet* / *sponsor*.

    Once inside a tip-related subtree, ALL nested pubkeys are collected — this handles
    object-shaped tips like {"quickslot": [...], "sponsor": [...]} as well as flat lists
    and SNS-name maps. Map keys that are themselves pubkeys (e.g. tip_wallet_sns) are
    collected too.
    """
    wallets = []

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if looks_like_pubkey(k):       # e.g. tip_wallet_sns keys are pubkeys
                    wallets.append(k.strip())
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
        elif isinstance(node, str):
            if looks_like_pubkey(node):
                wallets.append(node.strip())

    for k, v in d.items():
        if "tip_wallet" in k.lower() or "sponsor" in k.lower():
            walk(v)
    # de-dup preserving order
    seen, uniq = set(), []
    for w in wallets:
        if w not in seen:
            seen.add(w); uniq.append(w)
    return uniq


def auth_summary(d):
    ak = d.get("api_key")
    if not isinstance(ak, dict):
        return "Not documented" if ak in (None, False) else str(ak)
    parts = []
    req = ak.get("required")
    parts.append("required" if req else ("optional" if req is False else "unknown"))
    delivery = (ak.get("delivery") or ak.get("header") or ak.get("location")
                or ak.get("auth_mechanism") or ak.get("type") or ak.get("format"))
    if isinstance(delivery, dict):
        delivery = "; ".join(f"{k}: {v}" for k, v in delivery.items())
    if delivery:
        parts.append(str(delivery))
    return " — ".join(parts)


def min_tip(d):
    for k in ("min_tip_sol", "min_tip_lamports"):
        if k in d and d[k] is not None:
            return {k: d[k]}
    return {}


def build(provider_file):
    d = json.load(open(provider_file))
    name = d.get("name", os.path.basename(provider_file).replace(".json", ""))
    slim = {
        "name": name,
        "auth": auth_summary(d),
        **min_tip(d),
        "tip_wallets": collect_tip_wallets(d),
        "endpoints": {label: url for label, url in flatten_endpoints(d.get("endpoints", {}))},
    }
    return os.path.basename(provider_file), slim


def fmt_min_tip(slim):
    """Human string for min tip, handling scalar or per-mode object values."""
    def render(val, unit):
        if isinstance(val, dict):
            parts = [f"{k} {v}" for k, v in val.items()
                     if not isinstance(v, str)]  # drop note strings
            return f"{', '.join(parts)} {unit}" if parts else None
        return f"{val} {unit}"

    if slim.get("min_tip_sol") is not None:
        return render(slim["min_tip_sol"], "SOL")
    if slim.get("min_tip_lamports") is not None:
        return render(slim["min_tip_lamports"], "lamports")
    return None


def render_md(slim):
    lines = [f"# {slim['name']}", ""]
    lines.append(f"**Auth:** {slim['auth']}")
    mt = fmt_min_tip(slim)
    if mt:
        lines.append(f"**Min tip:** {mt}")
    lines.append("")
    lines.append("## Tip wallets")
    if slim["tip_wallets"]:
        lines += [f"- `{w}`" for w in slim["tip_wallets"]]
    else:
        lines.append("_None documented._")
    lines.append("")
    lines.append("## Endpoints")
    if slim["endpoints"]:
        lines += [f"- **{label}**: `{url}`" for label, url in slim["endpoints"].items()]
    else:
        lines.append("_None documented._")
    lines.append("")
    return "\n".join(lines)


def main():
    os.makedirs(JSON_OUT, exist_ok=True)
    os.makedirs(MD_OUT, exist_ok=True)
    files = sorted(glob.glob(os.path.join(ROOT, "*.json")))
    count = 0
    index_rows = []
    for f in files:
        fname, slim = build(f)
        stem = fname.replace(".json", "")
        with open(os.path.join(JSON_OUT, fname), "w") as out:
            json.dump(slim, out, indent=2)
            out.write("\n")
        with open(os.path.join(MD_OUT, stem + ".md"), "w") as out:
            out.write(render_md(slim))
        index_rows.append((slim["name"], stem, len(slim["tip_wallets"]), len(slim["endpoints"])))
        count += 1

    # README index
    readme = [
        "# ENDPOINTS & Tip Wallets — quick reference",
        "",
        "Minimal, copy-paste-friendly extract of each provider: **auth, min tip, tip wallets, endpoints** only.",
        "For full details (methods, rate limits, features, error codes) see the per-provider JSON in the repo root.",
        "",
        "> **Generated file — do not edit by hand.** Everything here is derived from the root provider JSON.",
        "> Regenerate after any change with: `python3 ENDPOINTS-TipsWallets_ONLY/generate_quickref.py`",
        "",
        "Two formats, same content:",
        "- `markdown/<provider>.md` — for reading / copy-paste in the browser",
        "- `json/<provider>.json` — for scripts",
        "",
        "| Provider | File | Tip wallets | Endpoints |",
        "| --- | --- | --: | --: |",
    ]
    for name, stem, nw, ne in index_rows:
        readme.append(f"| {name} | `{stem}` | {nw} | {ne} |")
    readme.append("")
    with open(os.path.join(HERE, "README.md"), "w") as out:
        out.write("\n".join(readme))

    print(f"Generated quick-reference for {count} providers -> json/ and markdown/")


if __name__ == "__main__":
    main()
