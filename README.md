# DevSecOps Security Pipeline Demo

A reference implementation of a **shift-left security pipeline** for CI/CD,
running four open-source scanners on every push and pull request. Built to
demonstrate how to integrate SAST, SCA and IaC scanning into GitHub Actions
with supply-chain hardening in mind.

> This repository is a **portfolio / learning project**. The application code
> under `app/` and the manifests under `infra/` contain **intentional
> vulnerabilities and misconfigurations** so the scanners have something to
> find. Nothing here is meant to run in production.

---

## What it does

| Layer | Tool | Purpose |
|-------|------|---------|
| SAST  | [Semgrep](https://semgrep.dev) | Static analysis of source code (injection, secrets, weak crypto) |
| SCA   | [Grype](https://github.com/anchore/grype) | Known CVEs in dependencies |
| SCA + config | [Trivy](https://github.com/aquasecurity/trivy) | Dependencies, IaC and image misconfiguration |
| IaC   | [Checkov](https://www.checkov.io) | Misconfigurations in Dockerfile and Kubernetes manifests |

Every scanner exports its findings as **SARIF**, uploaded as a build artifact
for review.

---

## Pipeline design

The workflow lives in [`.github/workflows/security-scan.yml`](.github/workflows/security-scan.yml).
The reasoning behind each choice is documented in
[`docs/technical-decisions.md`](docs/technical-decisions.md). In short:

- **Actions pinned by commit SHA**, not by tag, to defend against tag
  retargeting attacks on the supply chain.
- **Scanner versions pinned exactly** - and pinned *correctly*: the version is
  passed as an argument to the install script, because the script URL alone
  fetches the latest release (a subtle pitfall documented in the decisions file).
- **Monitoring mode** via `continue-on-error`: findings are surfaced without
  blocking merges, which suits a team still triaging an initial backlog.
- **pip and tool binaries cached** to reduce runtime and CI cost.

---

## Repository layout

```
devsecops-pipeline-demo/
├── .github/workflows/
│   └── security-scan.yml      # the pipeline
├── app/
│   ├── requirements.txt       # intentionally outdated deps (CVEs for SCA)
│   └── vulnerable_example.py  # intentional code flaws (for SAST)
├── infra/
│   ├── Dockerfile             # intentional image misconfig (for Trivy/Checkov)
│   └── k8s-deployment.yaml    # intentional K8s misconfig (for Checkov)
└── docs/
    └── technical-decisions.md # why each pipeline choice was made
```

---

## Running it

The pipeline runs automatically on push / pull request to `main`. To inspect
the findings, open the **Actions** tab, pick a run, and download the SARIF
artifacts.

To experiment locally with a single scanner, for example Semgrep:

```bash
pip install semgrep==1.165.0
semgrep scan --config auto .
```

---

## What this demonstrates

- Integrating multiple security scanners into a single CI pipeline
- Supply-chain hardening (SHA pinning, exact version pinning)
- Understanding of SAST vs SCA vs IaC scanning and what each catches
- Pragmatic rollout strategy (monitoring mode before enforcement)
- Reading scanner output critically rather than applying fixes blindly

---

## License

MIT - see [LICENSE](LICENSE). Use freely for learning.
