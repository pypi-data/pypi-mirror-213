# Tab

This is a helper library to easily fetch and refresh access token from Tabular.

## Usage

Every command has `--help` available:

```bash
➜ tab --help
Usage: tab [OPTIONS] COMMAND [ARGS]...

Options:
--environment TEXT
--help              Show this message and exit.

Commands:
refresh-token       Retrieves a fresh token based on an existing token
request-token       Retrieves an access token based on credentials
request-user-token  Retrieves a user token based on credentials
```

And the specific commands:

```bash
➜ tab request-user-token --help
Usage: tab request-user-token [OPTIONS] [SERVICE_TOKEN] [SERVICE_TOKEN_TYPE]
[ID_TOKEN] [ID_TOKEN_TYPE] [SCOPES]...

Retrieves a user token based on credentials

Options:
--help  Show this message and exit.
```

### Requesting access token

```bash
➜ tab request-token t-GdCZGj5OpoQ:jIcDDITVeIOnqxo7FxWbI21Y3kI | jq
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJjcmVkc0tleSI6InQtR2RDWkdqNU9wb1EiLCJzdWJJZCI6ImViMzc2NTQ4LTIwNmItNDBiYS1hN2E1LWVkYmUzZjg4YWVlZCIsInN1YiI6ImZva2tvQHRhYnVsYXIuaW8iLCJ3YXJlaG91c2VJZCI6IjhiY2IwODM4LTUwZmMtNDcyZC05ZGRiLThmZWI4OWVmNWYxZSIsImlzcyI6InRhYnVsYXIuaW8iLCJsb2NhdGlvbiI6InMzOi8vdGFidWxhci13aC11cy13ZXN0LTItZGV2LzhiY2IwODM4LTUwZmMtNDcyZC05ZGRiLThmZWI4OWVmNWYxZS8iLCJ0eXBlIjoiV0FSRUhPVVNFIiwicmVnaW9uIjoidXMtd2VzdC0yIiwiZXhwIjoxNjY1NzU1MzU2LCJpYXQiOjE2NjU2Njg5NTYsImp0aSI6IjRhZjcyMzk3LTVlOGQtNDc0OS1iZThmLWI4OTFmYTMwNjNhNiIsIm9yZ0lkIjoiMWM1MmU4MzItMjY2Yy00OTYxLTk3YWYtMTE1ZDFiNzJmY2UwIn0.sTu-j2lGG02Ui_Ts7_rMfkT-zha6ugMzz0JyiumHpTupqEXnDdNiaxyEJmJcu81IcjEaWwT32hxAlznLy6Qhr-yTeSoVY5pJnTiXMNxeAZwzDkGh87uLcp0PjgwRLc6DmD3ZAXC2WQEUf8PS_mcMXF_6HoegHv1GHGLk9aHhWLze6WI_SIKSLc0Gmw8ZjjZoUpL8SSwt-uinT8gY_D0TksHkeVzM5DFxhLvhXMjJ1VyRUbsrE_6An83-aG0NzsFFgK3IhCf-RsEsOXH1MKZpdLdIlelcz8Av1uFzgWA6kFAcy9dGVZu_Ycj19e58e17IKHgLbtk4cc4wJOAg6lCBsw",
    "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
    "token_type": "Bearer",
    "expires_in": 86400,
    "scope": null
}
```

Also, stdin is supported:

```bash
➜ cat cred.json | jq
{
    "credential": "t-GdCZGj5OpoQ:jIcDDITVeIOnqxo7FxWbI21Y3kI"
}
➜ cat cred.json | tab request-token | jq
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJjcmVkc0tleSI6InQtR2RDWkdqNU9wb1EiLCJzdWJJZCI6ImViMzc2NTQ4LTIwNmItNDBiYS1hN2E1LWVkYmUzZjg4YWVlZCIsInN1YiI6ImZva2tvQHRhYnVsYXIuaW8iLCJ3YXJlaG91c2VJZCI6IjhiY2IwODM4LTUwZmMtNDcyZC05ZGRiLThmZWI4OWVmNWYxZSIsImlzcyI6InRhYnVsYXIuaW8iLCJsb2NhdGlvbiI6InMzOi8vdGFidWxhci13aC11cy13ZXN0LTItZGV2LzhiY2IwODM4LTUwZmMtNDcyZC05ZGRiLThmZWI4OWVmNWYxZS8iLCJ0eXBlIjoiV0FSRUhPVVNFIiwicmVnaW9uIjoidXMtd2VzdC0yIiwiZXhwIjoxNjY1NzU1Mjg2LCJpYXQiOjE2NjU2Njg4ODYsImp0aSI6IjZhNzljNzU1LTYzNGEtNDJlNC04YmVlLTEzZjgxOWFlYTYyNCIsIm9yZ0lkIjoiMWM1MmU4MzItMjY2Yy00OTYxLTk3YWYtMTE1ZDFiNzJmY2UwIn0.WZNP_e-cMKX9pj7ydPA_sm2Zyy54Iht1bOx7g3lr8p5NRh8jyyD2RHY1hAhvDgLASZr49vBcjAsbRdvmq3WEAO_LV3c_ts-5edDhLfetAfmcDjR5Xv70HDvpmofkEkZVK7HE8P_IPA6z2YX-CbnEcAHPzZ3hrjfR6nc2ouo0h8tlg6OqmT8w75aX5PA9inh6xquMhBLYSfeGlET5XF3fryQ6Kd2PfTTftMRqo-DbkdMHHF7t8E8wrbf-I7cE7--o_KfF2paaebyRAuS9n7RSdOw82FL2dBn9V3cMwyNeTPH05m6OKChnXenG9xorgKnRkEeB_P6UdwEPcPH8YeQJHA",
    "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
    "token_type": "Bearer",
    "expires_in": 86400,
    "scope": null
}
```

### Requesting a user access token

```bash
tab request-user-token eyJ0e...eQJHA urn:ietf:params:oauth:token-type:id_token eyJ0e...eQJHA urn:ietf:params:oauth:token-type:access_token | jq
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJjcmVkc0tleSI6InQtR2RDWkdqNU9wb1EiLCJzdWJJZCI6ImViMzc2NTQ4LTIwNmItNDBiYS1hN2E1LWVkYmUzZjg4YWVlZCIsInN1YiI6ImZva2tvQHRhYnVsYXIuaW8iLCJ3YXJlaG91c2VJZCI6IjhiY2IwODM4LTUwZmMtNDcyZC05ZGRiLThmZWI4OWVmNWYxZSIsImlzcyI6InRhYnVsYXIuaW8iLCJsb2NhdGlvbiI6InMzOi8vdGFidWxhci13aC11cy13ZXN0LTItZGV2LzhiY2IwODM4LTUwZmMtNDcyZC05ZGRiLThmZWI4OWVmNWYxZS8iLCJ0eXBlIjoiV0FSRUhPVVNFIiwicmVnaW9uIjoidXMtd2VzdC0yIiwiZXhwIjoxNjY1NzU1Mjg2LCJpYXQiOjE2NjU2Njg4ODYsImp0aSI6IjZhNzljNzU1LTYzNGEtNDJlNC04YmVlLTEzZjgxOWFlYTYyNCIsIm9yZ0lkIjoiMWM1MmU4MzItMjY2Yy00OTYxLTk3YWYtMTE1ZDFiNzJmY2UwIn0.WZNP_e-cMKX9pj7ydPA_sm2Zyy54Iht1bOx7g3lr8p5NRh8jyyD2RHY1hAhvDgLASZr49vBcjAsbRdvmq3WEAO_LV3c_ts-5edDhLfetAfmcDjR5Xv70HDvpmofkEkZVK7HE8P_IPA6z2YX-CbnEcAHPzZ3hrjfR6nc2ouo0h8tlg6OqmT8w75aX5PA9inh6xquMhBLYSfeGlET5XF3fryQ6Kd2PfTTftMRqo-DbkdMHHF7t8E8wrbf-I7cE7--o_KfF2paaebyRAuS9n7RSdOw82FL2dBn9V3cMwyNeTPH05m6OKChnXenG9xorgKnRkEeB_P6UdwEPcPH8YeQJHA",
    "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
    "token_type": "Bearer",
    "expires_in": 64982,
    "scope": null
}
```

### Refreshing an access token

```bash
➜ tab refresh-token eyJ0e...eQJHA urn:ietf:params:oauth:token-type:access_token | jq
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJjcmVkc0tleSI6InQtR2RDWkdqNU9wb1EiLCJzdWJJZCI6ImViMzc2NTQ4LTIwNmItNDBiYS1hN2E1LWVkYmUzZjg4YWVlZCIsInN1YiI6ImZva2tvQHRhYnVsYXIuaW8iLCJ3YXJlaG91c2VJZCI6IjhiY2IwODM4LTUwZmMtNDcyZC05ZGRiLThmZWI4OWVmNWYxZSIsImlzcyI6InRhYnVsYXIuaW8iLCJsb2NhdGlvbiI6InMzOi8vdGFidWxhci13aC11cy13ZXN0LTItZGV2LzhiY2IwODM4LTUwZmMtNDcyZC05ZGRiLThmZWI4OWVmNWYxZS8iLCJ0eXBlIjoiV0FSRUhPVVNFIiwicmVnaW9uIjoidXMtd2VzdC0yIiwiZXhwIjoxNjY1NzU1NDM5LCJpYXQiOjE2NjU2NjkwMzksImp0aSI6IjZhNzljNzU1LTYzNGEtNDJlNC04YmVlLTEzZjgxOWFlYTYyNCIsIm9yZ0lkIjoiMWM1MmU4MzItMjY2Yy00OTYxLTk3YWYtMTE1ZDFiNzJmY2UwIn0.DBmmCfyj4hNaP0eVwzyv6R5aoSLrwWwHbHKePs2lEphA8zzilVreN1BPligIjezLPsn57S8FiOHqsCAwkeNWPthxxCI_gBkeZuCDhqbP90GsIuKwsFIaECZjn2_sO7UAhT3oSLgSeSB289QsQck6qIPPLLXM95jKrfzClKIF3Me4lKPmsRdLNRwCEDAOIgiR9sjBEUbSxgSkRvwxPQNDu75T25pn8O18EMlhmOUROSYva8VPRCc9PIFJL0PfcD_D7wlKZfiug8v58-q-1RAfB57IF0p-o9G_5RNeDrbEDA35OM8jTZEFDpL8Q-WlzT_6EZTvsIx_b7HxNW6kxf6WsQ",
    "issued_token_type": "urn:ietf:params:oauth:token-type:access_token",
    "token_type": "Bearer",
    "expires_in": 86400,
    "scope": null
}
```
