#!/usr/bin/env python3
"""
generate_xml.py
---------------
Generates all required XML files for the my-proxy-with-quota Apigee bundle.
Enforces a 3-requests-per-minute quota policy at the proxy level.

Usage:
    python scripts/generate_xml.py            # writes files under ./apiproxy/
    python scripts/generate_xml.py /some/path # writes under given base path

When run via GitHub Actions the workflow commits and pushes any changed XML
back to the repo, then imports and deploys the new revision to Apigee.
"""

import os
import sys
import textwrap

# ══════════════════════════════════════════════════════════════════════════════
#  ✏️  EDIT THESE VALUES TO CUSTOMISE YOUR PROXY
# ══════════════════════════════════════════════════════════════════════════════
PROXY_NAME      = "my-proxy-with-quota"
BASE_PATH       = "/v1/myapi"
TARGET_URL      = "https://mocktarget.apigee.net"
QUOTA_LIMIT     = 3
QUOTA_INTERVAL  = 1
QUOTA_TIME_UNIT = "minute"   # minute | hour | day
# ══════════════════════════════════════════════════════════════════════════════


# ── XML generators ────────────────────────────────────────────────────────────

def proxy_descriptor_xml() -> str:
    return textwrap.dedent(f"""\
        <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <APIProxy revision="1" name="{PROXY_NAME}">
            <DisplayName>{PROXY_NAME}</DisplayName>
            <Description>Proxy with {QUOTA_LIMIT} requests per {QUOTA_TIME_UNIT} quota policy</Description>
            <BasePaths>{BASE_PATH}</BasePaths>
            <Policies>
                <Policy>Quota-3-per-min</Policy>
            </Policies>
            <ProxyEndpoints>
                <ProxyEndpoint>default</ProxyEndpoint>
            </ProxyEndpoints>
            <TargetEndpoints>
                <TargetEndpoint>default</TargetEndpoint>
            </TargetEndpoints>
        </APIProxy>
    """)


def proxy_endpoint_xml() -> str:
    return textwrap.dedent(f"""\
        <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <ProxyEndpoint name="default">
            <Description>Default Proxy Endpoint</Description>

            <PreFlow name="PreFlow">
                <Request>
                    <Step>
                        <Name>Quota-3-per-min</Name>
                    </Step>
                </Request>
                <Response/>
            </PreFlow>

            <PostFlow name="PostFlow">
                <Request/>
                <Response/>
            </PostFlow>

            <Flows/>

            <HTTPProxyConnection>
                <BasePath>{BASE_PATH}</BasePath>
                <VirtualHost>secure</VirtualHost>
            </HTTPProxyConnection>

            <RouteRule name="default">
                <TargetEndpoint>default</TargetEndpoint>
            </RouteRule>
        </ProxyEndpoint>
    """)


def target_endpoint_xml() -> str:
    return textwrap.dedent(f"""\
        <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <TargetEndpoint name="default">
            <Description>Default Target Endpoint</Description>

            <PreFlow name="PreFlow">
                <Request/>
                <Response/>
            </PreFlow>

            <PostFlow name="PostFlow">
                <Request/>
                <Response/>
            </PostFlow>

            <Flows/>

            <HTTPTargetConnection>
                <URL>{TARGET_URL}</URL>
            </HTTPTargetConnection>
        </TargetEndpoint>
    """)


def quota_policy_xml() -> str:
    return textwrap.dedent(f"""\
        <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <Quota async="false" continueOnError="false" enabled="true" name="Quota-3-per-min">
            <DisplayName>Quota–{QUOTA_LIMIT}-per-{QUOTA_TIME_UNIT}</DisplayName>
            <Allow count="{QUOTA_LIMIT}"/>
            <Interval>{QUOTA_INTERVAL}</Interval>
            <TimeUnit>{QUOTA_TIME_UNIT}</TimeUnit>
        </Quota>
    """)


# ── File manifest ─────────────────────────────────────────────────────────────
# Each entry: (relative path under apiproxy/, generator function)

FILE_MANIFEST = [
    (f"apiproxy/{PROXY_NAME}.xml",             proxy_descriptor_xml),
    ("apiproxy/proxies/default.xml",           proxy_endpoint_xml),
    ("apiproxy/targets/default.xml",           target_endpoint_xml),
    ("apiproxy/policies/Quota-3-per-min.xml",  quota_policy_xml),
]


# ── Writer ────────────────────────────────────────────────────────────────────

def write_files(base_path: str = ".") -> None:
    for relative_path, fn in FILE_MANIFEST:
        full_path = os.path.join(base_path, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as fh:
            fh.write(fn())
        print(f"[OK] Written: {full_path}")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    base_path = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"==> Generating XML files under: {os.path.abspath(base_path)}")
    write_files(base_path)
    print("==> XML generation complete.")


if __name__ == "__main__":
    main()
