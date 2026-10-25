# Security policy

This is a deliberately vulnerable **educational** range. The intended deployment is isolated Docker-only networking, without host port publishing. Do not attach the DC to the open Internet, corporate LAN, or university production network.

## Reporting an unintended security issue

Avoid publishing exploit details or real secrets in a public issue. Contact the project maintainer through the contact information on [GREEN ARMOR ACADEMY](https://www.greenarmor.academy) and provide reproduction steps without external victim data.

**Expected insecure behavior**: LDAP simple binds without TLS, broadly readable example files, exposed fictional service-account credentials, and excessive access to the mock archive.

**Unexpected insecure behavior**: any escape from Docker to the host, disclosure of non-lab credentials, public-network exposure by default, or unintended secrets committed to Git.
