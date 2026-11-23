# Changelog

## 2026-11-23

- Combine upstream `01d6ce9` (ranch improvements) with PR #180 farm illustrated
  auto rewards, including an independent setting and persistent duplicate protection.
- Preserve existing deployment compatibility patches. Add the bounded Linux02
  activation/check entry point; Compose remains managed through ops-config-file.
- Deployment procedure and rollback: [November 23 release](docs/deploy-20261123.md).
- Deployed on Linux02 at 19:55 CST and verified after container restart. Core
  300/300 and web 21/21 passed; existing account/config data preserved. See the
  deployment receipt for image identity, private backup and rollback details.
