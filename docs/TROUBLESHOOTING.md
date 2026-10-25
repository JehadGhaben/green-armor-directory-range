# Validation and troubleshooting

## Before giving this to students

On a Linux machine with a functional Docker Engine and Compose v2:

```bash
python3 armorlab.py doctor
python3 armorlab.py up
python3 armorlab.py status
python3 armorlab.py shell
```

Then in the `student` shell (the password is in `README.md`):

```bash
getent hosts dc
dig @dc _ldap._tcp.armor.test SRV
nc -zv dc 445
smbclient -L //dc -U 'ARMOR\student01'
ldapsearch -x -H ldap://dc -D 'student01@armor.test' -W \
  -b 'DC=armor,DC=test' '(sAMAccountName=svc_backup)' sAMAccountName description memberOf
```

Validate authentication boundaries with a **negative check**: `student01` must not be able to read the `GA-Archive` share, while the designated service principal can. Finally, submit one discovered flag to verify the scorer, then use `reset --yes` to rotate all flags for distribution.

> This repository's CI runs static Python tests. **Runtime integration validation requires Docker**; do not assume that a successful CI badge proves a working Samba provisioning on every host.

## Common problems

**No Docker daemon**: Check `docker info`, start the service or configure Docker Desktop/WSL, and confirm your account can access the daemon.

**Samba not healthy**: Run `python3 armorlab.py logs`. Initial provisioning can take some time. Review the `samba-tool domain provision` and user/group creation messages.

**Conflicting existing domain data**: Do not manually edit persistent Samba volumes. Use `python3 armorlab.py reset --yes` to start fresh (all progress and flags will be lost).

**DNS cannot resolve AD SRV records**: Docker embedded DNS handles container aliases, not necessarily native AD SRV records. Use `dig @dc _ldap._tcp.armor.test SRV`. `dc` points to the private container DNS alias.

**Out-of-date files after image rebuild**: `down` preserves named volumes. Rebuilding an image does not replay first-boot domain provisioning. Explicitly `reset --yes` if a fresh seed is required.

**Ports on the laptop**: No port publishing is configured; tests run from the bundled `student` container. Direct connections from host Kali to DC are **not** supported in this security-minded default setup.

**Weak AD behaviors**: The environment is intentionally vulnerable in a Docker-only network; do not attach real network interfaces or port-forward from campus infrastructure.

### Automated smoke test (instructor)

Once `python3 armorlab.py up` reports a healthy lab, run:

```bash
python3 scripts/smoke-test.py
```

The smoke test performs DNS, SMB (including a negative access check), and LDAP verification, and **does not print service credentials or live flags**. It requires an actual Docker Engine; this test has not been executed in the artifact-generation environment.
