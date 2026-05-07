# Security Policy

## Reporting a Vulnerability

We take security seriously. If you believe you have found a security
vulnerability in `kaos-names`, please report it privately so we can address it
before public disclosure.

Do not file a public GitHub issue for security reports.

### How to Report

Use [GitHub Private Vulnerability Reporting](https://github.com/273v/kaos-names/security/advisories/new)
to send a report. Alternatively, email **security@273ventures.com**.

Include as much of the following as you can:

- A description of the vulnerability and its impact
- Steps to reproduce, including affected versions
- Any proof-of-concept code, if available
- Suggested mitigations, if you have any

### What to Expect

- Acknowledgement within 3 business days of your report.
- Initial triage within 7 business days, including a severity assessment.
- Fix and disclosure coordinated with you. Our target window is 90 days from
  acknowledgement to public disclosure, faster for high-severity issues.
- Credit in the release notes and security advisory unless you prefer to remain
  anonymous.

## Supported Versions

`kaos-names` follows Semantic Versioning. While the project is pre-1.0, only
the latest minor release receives security fixes. After 1.0, the latest two
minor releases will be supported.

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |
| < 0.1   | No        |

## Scope

In scope:

- The `kaos-names` Python package as published on PyPI
- The `273v/kaos-names` GitHub repository, including CI and release supply chain

Out of scope:

- Third-party dependencies, which should be reported upstream
- Issues caused by user-supplied configuration outside this package
