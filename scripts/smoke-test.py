#!/usr/bin/env python3
"""Optional end-to-end smoke test; needs a running range and Docker Engine.

Never runs inside GitHub Actions. Use after `python3 armorlab.py up`.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / 'runtime' / 'state.json'


def cmd(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ('docker', 'compose', '-f', str(ROOT / 'compose.yaml'), 'exec', '-T', 'student', *args),
        cwd=ROOT, capture_output=True, text=True, check=False, timeout=40,
    )


def require(name: str, result: subprocess.CompletedProcess[str], *, success: bool, contains: str = '') -> bool:
    matched = (result.returncode == 0) if success else (result.returncode != 0)
    if contains:
        matched = matched and contains in (result.stdout + result.stderr)
    print(f"[{'PASS' if matched else 'FAIL'}] {name}")
    if not matched:
        print('    Exit code:', result.returncode)
        # Do not dump outputs: they could contain dynamic secrets.
    return matched


def main() -> int:
    if not STATE.exists():
        print('Start the range first: python3 armorlab.py up')
        return 2
    state = json.loads(STATE.read_text(encoding='utf-8'))
    student = r'ARMOR\student01%GreenArmor2026!'
    service = 'ARMOR\\svc_backup%' + state['service_password']
    checks = [
        require('Docker DNS', cmd('getent', 'hosts', 'dc'), success=True, contains='dc'),
        require('Samba SMB port', cmd('nc', '-z', 'dc', '445'), success=True),
        require('Public share with student identity', cmd('smbclient', '//dc/GA-Public', '-U', student, '-c', 'ls'), success=True),
        require('Private archive rejects student', cmd('smbclient', '//dc/GA-Archive', '-U', student, '-c', 'ls'), success=False),
        require('Private archive accepts service account', cmd('smbclient', '//dc/GA-Archive', '-U', service, '-c', 'ls'), success=True),
        require('LDAP account attribute', cmd('ldapsearch', '-x', '-H', 'ldap://dc', '-D', 'student01@armor.test', '-w', 'GreenArmor2026!', '-b', 'DC=armor,DC=test', '(sAMAccountName=svc_backup)', 'description'), success=True, contains=state['flags']['02']),
    ]
    print(f'\n{sum(checks)}/{len(checks)} checks passed.')
    return 0 if all(checks) else 1


if __name__ == '__main__':
    sys.exit(main())
