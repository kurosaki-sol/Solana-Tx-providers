# AllenHark Relay (Slipstream)

**Auth:** optional — http: header `x-api-key: YOUR_API_KEY` (or query parameter `?api-key=YOUR_API_KEY`); quic: optional first stream line `api-key: YOUR_API_KEY\n` then the JSON payload. Transactions are accepted without a key.
**Min tip:** 0.001 SOL (bundles additionally require a separate Jito tip to a Jito tip account)

## Tip wallets
- `hark1zxc5Rz3K8Kquz79WPWFEgNCFeJnsMJ16f22uNP`
- `harkm2BTWxZuszoNpZnfe84jRbQTg6KGHaQBmWzDGQQ`
- `hark4CwtTnN2y9FaxjcFBAJdJqQrpouu5pgEixfqdEz`
- `harkoJfnM6dxrJydx5eVmDVwAgwC94KbhuxF69UbXwP`
- `hark6hUDUTekc1DGxWdJcuyDZwf6pJdCxd4SXAVtta6`
- `harkoTvFpKSrEQduYrNHXCurARVT19Ud3BnFhVxabos`
- `harkEpXoJv5qVzHaN7HSuUAd6PHjyMcFMcDYBMDJCEQ`
- `harkyXDdZSoJGyCxa24t2QXx1poPyp8YfghbtpzGSzK`
- `harkR2YJ4Dpt4UDJTcBirjnSPBhNpQFcoFkNpCkVqNk`
- `harkRBygM8pHYe4K8eBjfxyEX19oJn3LepFjvNbLbyi`
- `harkYFxB6DuUFNwDLvA5CQ66KpfRvFgUoVypMagNcmd`

## Endpoints
- **frankfurt.quic**: `84.32.223.83:4433`
- **frankfurt.https**: `https://fra.relay.allenhark.com/v1/sendTx`
- **amsterdam.quic**: `84.32.104.38:4433`
- **amsterdam.https**: `https://ams.relay.allenhark.com/v1/sendTx`
- **new_york.quic**: `66.94.98.217:4433`
- **new_york.https**: `https://ny.relay.allenhark.com/v1/sendTx`
- **tokyo.quic**: `88.216.188.28:4433`
- **tokyo.https**: `https://tyo.relay.allenhark.com/v1/sendTx`

> `relay.allenhark.com` is an alias for `fra.`. Per region also: HTTPS `/v1/sendBundle` and WebSocket `wss://{region}.relay.allenhark.com/v1/stream/{tx,bundle}`. Keepalive: `https://relay.allenhark.com/keepalive`.
