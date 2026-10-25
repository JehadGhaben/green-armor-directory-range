<div align="center">

<img src="assets/cover.svg" alt="GREEN ARMOR Directory Range" width="100%" />

### A Lightweight, Isolated Active Directory Training Range

**Samba AD • LDAP • Kerberos • SMB • Four Rotating Flags • Docker Compose**

Created by **JEHAD GHABEN** · **GREEN ARMOR ACADEMY**

[Arabic guide / الدليل العربي](README_AR.md) · [Student assignment](docs/STUDENT_TASK.md) · [Architecture](docs/ARCHITECTURE.md) · [Troubleshooting](docs/TROUBLESHOOTING.md)

</div>

---

## Overview

**Operation Directory** is an original, compact Active Directory security-assessment lab for classroom use. It uses **one Samba AD Domain Controller** and **one Linux student toolbox** on an **internal Docker network**, avoiding the overhead of multiple Windows virtual machines. Four connected challenges cover authenticated service discovery, LDAP account analysis, a leaked service credential, and an improperly exposed operations archive.

The lab creates **fresh random flags and a service password** the first time it is started. The instructor can rotate all challenges with a single reset. Students submit flags to a local scoring interface and write a professional vulnerability report.

> [!IMPORTANT]
> This is a **Samba AD simulation**, not Microsoft Windows Server. It does not provide native Windows workstations, enterprise GPO behavior, Windows-specific access-control primitives, or AD Certificate Services. Best suited for **beginner/intermediate AD fundamentals and security assessment**, not Windows-specific attack emulation.

## Why this range?

- **Compact:** two Docker services and no hypervisor or Windows licensing requirements.
- **Authentic directory services:** Samba Active Directory, SMB, LDAP, Kerberos, and internal DNS.
- **Safe default networking:** no host ports published, `internal: true` Docker bridge.
- **Student experience:** built-in hints, interactive student shell, scoreboard, reset, and self-check.
- **Original identity:** branded for GREEN ARMOR ACADEMY, with attribution to JEHAD GHABEN.
- **No committed challenge secrets:** local run-specific answers and credentials are ignored by Git.

## Architecture

```text
                  Docker private bridge (internal only)
          ┌──────────────────────────────────────────────┐
          │                                              │
          │  ┌────────────────────┐    ┌──────────────┐  │
          │  │ student            │    │ dc           │  │
          │  │ Debian toolbox     │───▶│ ARMOR.TEST   │  │
          │  │ ldapsearch         │    │ Samba AD DC  │  │
          │  │ smbclient          │    │ LDAP/SMB/DNS │  │
          │  │ dig / nmap / kinit │    │ Kerberos     │  │
          │  └────────────────────┘    └──────────────┘  │
          │                                              │
          └──────────────────────────────────────────────┘

           No published ports  •  No production access
```

## Prerequisites

- Linux with **Docker Engine** and **Docker Compose v2**; alternatively a platform with working Linux containers.
- Python **3.9 or newer** (standard library only).
- Working internet connection **for initial Docker image builds**.
- Suggested starting allowance: around **2 GB RAM free and 3 GB disk available**; exact usage varies by host and image versions, **not benchmarked here**.

## Quick start

```bash
git clone https://github.com/YOUR-USERNAME/green-armor-directory-range.git
cd green-armor-directory-range
python3 armorlab.py doctor
python3 armorlab.py up
python3 armorlab.py info
python3 armorlab.py shell
```

**Replace `YOUR-USERNAME` with the GitHub account you actually publish to.** This repository has not been uploaded to GitHub on your behalf.

In the student's toolbox:

```bash
# Find the DC and enumerate the shared resources.
dig @dc _ldap._tcp.armor.test SRV
smbclient -L //dc -U 'ARMOR\student01'

# Enumerate directory identities (enter the initial password when prompted).
ldapsearch -x -H ldap://dc -D 'student01@armor.test' -W \
  -b 'DC=armor,DC=test' '(objectClass=user)' sAMAccountName description
```

### Student entry card

| Field | Value |
| --- | --- |
| Realm | `ARMOR.TEST` |
| Domain | `ARMOR` |
| Domain Controller | `dc` |
| Account | `student01` |
| Initial password | `GreenArmor2026!` |

All accounts and passwords in this range are intentionally fictional and must **never** be used outside the isolated lab.

## Scenarios and grading

| Stage | Task | Points |
| --- | --- | ---: |
| 01 | Network and SMB discovery | 15 |
| 02 | LDAP directory enumeration | 20 |
| 03 | Exposed service credentials | 25 |
| 04 | Unauthorized archive access | 40 |
| **Total** | | **100** |

Evidence/reporting is expected in addition to the four flag submissions; instructors may assess report quality separately. See [Student task](docs/STUDENT_TASK.md).

### CLI reference

```bash
python3 armorlab.py up                  # Build/start (initializes secrets)
python3 armorlab.py shell               # Student's Linux shell
python3 armorlab.py info                # Student entry card and tasks
python3 armorlab.py status              # Containers
python3 armorlab.py submit 'GA{...}'   # Verify one flag
python3 armorlab.py score               # Scoring table
python3 armorlab.py score --json        # Machine-readable score
python3 armorlab.py hint 02 1          # First hint, stage 02
python3 armorlab.py logs                # Domain Controller logs
python3 armorlab.py down                # Stop, preserve data
python3 armorlab.py reset --yes         # Delete everything and rotate answers
```

> [!CAUTION]
> `reset --yes` removes persistent domain data, progress, and all active flags. Previous submissions become invalid.

## Educational safety boundary

The directory is **intentionally misconfigured**: a share is readable too broadly, service credentials are stored insecurely, and plaintext LDAP simple binds are permitted on the internal network to simplify the exercises. **Never bridge this range to a campus, corporate, or Internet-facing network.** The Compose file publishes no ports by default. Never use real student credentials inside the lab.

For fair grading, do not rely on local flags as tamper-proof exam evidence: **any student with full access to their own Docker host can inspect containers, volumes, and run-time files**. Require screenshots/terminal transcripts and a written report; for exam-style grading, host the range on instructor-controlled infrastructure.

## Project layout

```text
green-armor-directory-range/
├── armorlab.py                  # Python CLI and local flag verifier
├── compose.yaml                 # Internal network and containers
├── docker/
│   ├── dc/                     # Samba AD DC and provisioning
│   └── student/                # LDAP/SMB/DNS/Kerberos toolbox
├── docs/
│   ├── STUDENT_TASK.md
│   ├── ARCHITECTURE.md
│   └── TROUBLESHOOTING.md
├── scripts/                     # Optional Docker smoke test
├── tests/                       # Dependency-free CLI tests
├── assets/                      # Original typographic brand banner
└── runtime/                     # Generated locally; NEVER COMMIT
```

## Development

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile armorlab.py
```

GitHub Actions runs lightweight Python/packaging checks. **Container integration testing is not performed by the included CI workflow**; you should complete the checklist in [Troubleshooting](docs/TROUBLESHOOTING.md) before publishing a release or assigning students.

## Credits

**Author & maintainer:** JEHAD GHABEN  
**Organization:** GREEN ARMOR ACADEMY / GREEN ARMOR CYBER SECURITY  
**Website:** [www.greenarmor.academy](https://www.greenarmor.academy)  
**License:** MIT (see [LICENSE](LICENSE))

This is an independently written teaching project built using Samba and Docker. It is **not** a fork or rebranded copy of a third-party training suite. Samba and Docker remain trademarks/projects of their respective owners.
