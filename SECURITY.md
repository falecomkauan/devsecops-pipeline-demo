# Security Policy

## Scope

This is a **demonstration repository**. The code under `app/` and the manifests
under `infra/` contain **intentional** vulnerabilities and misconfigurations,
used to show the scanning pipeline detecting them. Those are by design and do
not need to be reported.

This policy applies to genuine issues in the **pipeline itself**
(`.github/workflows/`) or the supporting tooling — for example a misconfigured
action, a broken pin, or a workflow that leaks something it should not.

## Reporting a vulnerability

If you find a real security issue in the pipeline or tooling:

1. **Do not** open a public issue describing the exploit.
2. Use GitHub's **private vulnerability reporting** (the "Report a
   vulnerability" button under the Security tab), or open a minimal issue
   asking to be contacted privately.
3. Include enough detail to reproduce: affected file, expected vs actual
   behavior, and impact.

You can expect an acknowledgement within a few days.

## Supported versions

This is a learning project on a rolling `main` branch. Only the latest commit
on `main` is maintained.

## Hardening already in place

- GitHub Actions pinned by commit SHA (defense against tag retargeting).
- Scanner tools pinned to exact versions, passed as install arguments.
- Least-privilege workflow permissions (`contents: read`).
- No secrets committed; intentional sample credentials are obvious
  placeholders, not real-format keys.