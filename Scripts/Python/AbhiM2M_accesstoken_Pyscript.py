import time
import urllib.request
import urllib.parse
import jwt
import json

# 1. Define your private key (Ensure it is in PKCS#8 or OpenSSL PEM format)
PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCuYwR8gm4v0r14
rYmbuB8wdpC93jjh3muRRRhNMKvEJnvTpzbPqM2HctT6s5vr2jfhF6najjQ7UWL0
Lxj/CW9h1LWjkg9wCs46EGei5k4D720T10sK+TgrD993n4kuwzlAKl2Do/+Ac2me
jZ8fSVtze458RMH+7jV3nJacqD50eioLChUpyDE5qkpOVUe1S0XUHiaP/TIJSmtz
KfQOWKqEcfIooM+USlCaJlmeBDWOnQ1lZ0jK4JdKuzHg4Yh+zWJZE9FBMuaOuAuF
jQt0rD5/zxXxnJLoCrvNJujKPXTQBcsXrv3RDL8RKQLvGL2gCOaZdVbKXZ8Wr/PW
so8gyq9zAgMBAAECggEABbqZBiIezpFkyhchYy08URJEFQi846az7/TOJJMJwYrm
HIDsywunnOCH4KiP4cKsfUeSu+xaCOzWjGETuCUuNI+RXAtLWInyVnP9g5t/Sp/N
/I3hGD4xuzBtTfe+wPuG4PXDVrTHiwe/m4bZiGSXjYasmqaDnQVkWkaZqBHa42am
IuY+EPG0rajMZnbpCz3ajd5/h7SVL7NH2pB+66/LezzBVmK5ROAip8L8rVnTYeko
1I7nwb16Y9RBy7dP+mNLvNzCSsXetT8CvrUabfFiYbs9hGkYqOheho7RqBN0nId1
LDrmS4VU0r2KBs917DaA3MgV9gu4E63xj3SDH1iymQKBgQDU1ooGcjOb2beQIN5h
aNw0g8KpI2KOAQG2Iqs8mgSnJS1eDyzrOgQ3LuVgFh/3f6+TQaWPLzEmBUw0x/ns
s1ByZulMNaTuwpwL1KNLrQox8k7FqnvEsbzPwIGaY+tTkKS5Dc/NA8/0AIsUE4Zb
rdozGPjMYvZs/tNIYaHQNLdiRQKBgQDRwEk/NSuEcnDCHOZe98lXBkYonx/x4XdA
sCvIb5sZAkHGf3cGSbK23CLXAi8QjKnaAn6+pO6QoBSMJE5/LLgEf11kZvjsm0X5
EOL0kVDrAhJqt0zpFXvEdoxPmelpqW7mFM1pWZakxPNz3pr5tMcCED9V86D35t8E
8cl0JgDCVwKBgANkzFyf84y3owKsU39wIZrAwxjZVJf5EiLqWJqlxg84O4n1afzy
NuD+YW/vymCy64TIljA7S2hUy0tIKQcKMO0yEORDMrcP6VcS8+uf/bqgJ3tlZYXU
Y7NYWXixwS3a75V3z+lv9x/n5k/So+DQW9tWuZjgtxcz1QChdegQ/x+VAoGBALNv
nPm+wbC3ujDFSmrZ7VtOWbysjEZ/jGZBj+MTXwqg/KYUKz2s1H9MiV2IV7z/qNqB
Ie5z6Ea/O3S8Jo7zMaVfVATtdmvrVYwB3zY8Do5NInY6w0fvAgeLJvN+BslGkkGw
cB1877ubZW2tdMTD2y+vuI8OMZmB3y46rg136VRXAoGAJEVAk3/YLeT/j83JnyrN
BFTri4x+Lp5Q/z9aj1/wArw/bJYFwVzR2gHFiAPbsZc+/b31xpxuxk0kM/nttRI3
w61bAgsS8KIp0cTTatuP987vVaUsSHcIe/MVuQMqdbz58T+w20qzW9q3V/I5vAj5
5GVTNVADog6xmBeGO3Y9n+Q=
-----END PRIVATE KEY-----"""

# 2. Structure your JSON payload with automatic timestamps
now = int(time.time())
payload = {
    "iss": "0oa1284mh9886hbYl698",
    "sub": "0oa1284mh9886hbYl698",
    "aud": "https://integrator-6847367.okta.com/oauth2/v1/token",
    "iat": now,                  # Current time
    "exp": now + 3600           # Expires in 1 hour
}

# 3. Sign the payload using the RS256 algorithm
try:
    signed_token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")

    # 4. Exchange the signed JWT assertion for the actual Okta Access Token
    token_url = "https://integrator-6847367.okta.com/oauth2/v1/token"
    
    # 5. Format payload as form-urlencoded data
    data_dict = {
        "grant_type": "client_credentials",
        "scope": "okta.users.read",
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": signed_token
    }
    encoded_data = urllib.parse.urlencode(data_dict).encode("utf-8")
    
    # 6. Build the Request using native urllib
    req = urllib.request.Request(token_url, data=encoded_data, method="POST")
    req.add_header("Accept", "application/json")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    
    # 7. Execute the request
    with urllib.request.urlopen(req) as response:
        response_body = response.read().decode("utf-8")
        response_data = json.loads(response_body)
    
    if "access_token" in response_data:
        print("\n=================== OKTA ACCESS TOKEN ===================")
        print(response_data["access_token"])
        print("=========================================================\n")
        print("Copy the entire string above for your Postman Authorization header.")
    else:
        print("\n❌ Error exchanging token from Okta:")
        print(response_data)

except urllib.error.HTTPError as e:
    print(f"\n❌ Okta API returned an error status: {e.code}")
    print(e.read().decode("utf-8"))
except Exception as e:
    print(f"\n❌ Error signing token or making request: {e}")
 