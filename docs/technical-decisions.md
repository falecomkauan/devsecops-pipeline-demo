# Technical Decisions

This document explains *why* the pipeline is built the way it is. The goal is
to show the reasoning, not just the result - the same trade-offs you would
discuss in a real security review.

---

## 1. Why pin actions by commit SHA instead of tag?

```yaml
uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8 # v5.0.0
```

Git tags are **mutable**. A maintainer (or an attacker who compromises the
repository) can move a tag like `v5` to point at different code. A workflow
that references `@v5` would then silently pull and execute that new code.

Pinning to a full commit SHA makes the reference **immutable**: what you pin is
what runs, forever. The trailing `# v5.0.0` comment keeps it human-readable and
lets Dependabot propose updates.

This is a defense against **tag retargeting / supply-chain attacks**, which
have become a common vector in CI/CD.

---

## 2. Why pass the scanner version as an argument, not in the URL?

This one is subtle and easy to get wrong.

```yaml
# WRONG - looks pinned, but installs the LATEST release:
curl -sSfL https://raw.githubusercontent.com/anchore/grype/v0.104.1/install.sh | sh -s -- -b /usr/local/bin

# CORRECT - pins the actual installed version:
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin v0.104.1
```

The version in the **URL** only selects which *install script* is downloaded.
When that script runs, it queries the GitHub API for the **latest** release and
installs that. So `.../v0.104.1/install.sh` happily installs whatever the newest
version happens to be.

To pin the installed binary, the version must be passed as a **positional
argument** to the script (per the official Anchore / Aqua docs). Without this,
"reproducible builds" are an illusion - each run can pull a different version.

**Takeaway:** verify that a pin actually pins. Don't assume.

---

## 3. Why `continue-on-error` instead of `|| true`?

Both keep a failing scanner from breaking the build, but they behave differently:

| Approach | Effect |
|----------|--------|
| `\|\| true` | Masks the command's exit code; the step is always green, even on real failure. |
| `continue-on-error: true` | The step is marked failed (visible/amber) but does not block the job. |

`continue-on-error` is preferred because it **preserves visibility**: you can
see that a scanner ran and what happened, without blocking the merge. `|| true`
hides everything, which is a code smell.

---

## 4. Why "monitoring mode" at all?

When you first add security scanning to an existing codebase, the scanners will
light up with a backlog of pre-existing findings. Blocking every merge on day
one would grind delivery to a halt and make the team resent the tooling.

Monitoring mode (non-blocking) lets the team **see** findings, triage them, and
fix them progressively. Enforcement (failing the build on new criticals) is a
later phase, introduced once the backlog is under control - ideally gated
per-tool and per-severity.

---

## 5. Why SARIF output?

SARIF is a standard format for static-analysis results. Exporting to SARIF means
the findings can later be fed into:

- GitHub Code Scanning (the Security tab), or
- an ASPM / vulnerability-management hub (e.g. DefectDojo)

without re-parsing each tool's bespoke output. It keeps the pipeline portable.

---

## 6. Why cache pip and the tool binaries?

Without caching, every run re-downloads Semgrep, Checkov (via pip) and the Grype
/ Trivy binaries. Caching:

- pip via `actions/setup-python` with `cache: pip`
- binaries via `actions/cache` keyed by exact version

cuts a meaningful amount of time and CI cost on repeated runs. The install step
is skipped entirely on a cache hit.

---

## 7. SAST vs SCA vs IaC - what catches what?

| Scanner type | Looks at | Example finding in this repo |
|--------------|----------|------------------------------|
| SAST (Semgrep) | Your source code | SQL injection, hardcoded secret, `eval` |
| SCA (Grype/Trivy) | Third-party dependencies | Known CVE in an outdated `requests` |
| IaC (Checkov/Trivy) | Infra definitions | Privileged container, `latest` image tag |

A complete pipeline needs all three, because each blind-spots the others: clean
code can still ship a vulnerable dependency, and perfect dependencies can still
run in a misconfigured container.
