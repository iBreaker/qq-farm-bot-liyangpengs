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
- Follow-up `564a878`: ranch normal/giant book checks now run on startup and
  every five minutes without notifications; giant reward claims require state
  readback. Deployed 20:17 CST; core 304/304 passed. Live reward delivery awaits
  manual game login after the container recreation. Subsequent 20:18 live validation
  confirmed all three giant tiers automatically claimed, with no pending operation.
