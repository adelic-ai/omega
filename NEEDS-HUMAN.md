# NEEDS-HUMAN

## Cannot push `feat/atlas-coverage-cartography` to origin — deploy key lacks write access

**What:** All 7 commits for the ATLAS ingest + coverage cartography build (ATLAS-SPEC.md) are committed
locally on `feat/atlas-coverage-cartography`, branched off `main` at `dc239d1`. `git push` fails:

- HTTPS (`origin`, `https://github.com/adelic-ai/omega`): `fatal: could not read Username for
  'https://github.com': No such device or address` — no credential helper configured for HTTPS auth.
- SSH (`git@github.com:adelic-ai/omega.git`, using the VM's only key, `~/.ssh/id_ed25519` /
  `agent-vm-deploy`): `ERROR: Permission to adelic-ai/omega.git denied to deploy key.` The key is present
  and github.com is in `known_hosts`, so SSH itself works — the key just isn't authorized to write to this
  repo (read-only deploy key, or authorized for a different repo entirely).

**Why it needs a human:** fixing this means either granting the deploy key write access on
`adelic-ai/omega`, or provisioning a different credential (PAT, different deploy key) on the VM — both are
access-control changes I shouldn't make unilaterally, and I don't have another way to get the commits off
this VM without one of those (no other remote configured, and adding one would violate the "push only to
origin" discipline in CLAUDE.md).

**What I did meanwhile:** kept building and committing locally rather than blocking — all 7 commits are on
the branch, tests pass (`pytest`: 54 passed / 11 skipped with no real corpora on `PATH`; ran clean against
live SigmaHQ/sigma + mitre-attack/car + the compiled ATLAS.yaml too — see README's ATLAS section for those
real numbers). Nothing here is lost; it just needs a push once access is sorted. `git log --oneline
main..feat/atlas-coverage-cartography` on this VM shows the full stack.
