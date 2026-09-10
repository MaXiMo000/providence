# providence

[![ci](https://github.com/MaXiMo000/providence/actions/workflows/ci.yml/badge.svg)](https://github.com/MaXiMo000/providence/actions/workflows/ci.yml)

**One versioned shape for "content + sha256(content)" evidence, and a
checker that catches tampering.**

`receipt` and `invariant` (two other tools in this portfolio) both already
write proof-of-work to disk this way — a result, a hash of it, a
timestamp. They arrived at two different envelope shapes for the same
idea. `providence` names the shape underneath both, as one small, checkable
spec, so a third or fourth tool doesn't reinvent it a third or fourth time.

This is a spec-and-checker, not a platform. It doesn't run checks, collect
evidence, or replace `receipt`/`invariant` — it only answers "is this
bundle what it claims to be."

```
$ providence check proof/
PASS  proof/ is a conformant Providence bundle

$ providence check proof/   # after someone hand-edits a file in it
FAIL  proof/manifest.json: items[0] (id=no_negative_payments): sha256 mismatch -- manifest says 6bc0..., no_negative_payments.json actually hashes to 9fab... (tampered or corrupted)
```

Full shape, and why it looks the way it does: [SPEC.md](SPEC.md).

## Install

```
pip install providence-evidence
```

(`providence` and `receipt` were both already taken on PyPI — same story
as `invariant-verify`/`receipt-evidence` in this portfolio. The installed
command is still the short name, `providence`.)

## Convert existing output

`receipt` and `invariant` don't need to change what they write — a
converter reads each tool's real output and emits a Providence-conformant
bundle from it:

```
providence convert-invariant proof/ providence-proof/   # invariant's --evidence dir
providence convert-receipt out/20260909T...-abcd.json providence-proof/   # a single receipt
providence check providence-proof/
```

## What it checks

1. The envelope has `providence_version` (currently `1`), `generated_at`, `tool`.
2. Every hash in the manifest matches the actual bytes of the file it
   claims to cover. A mismatch means the content changed after the
   manifest was written — that's the entire point.
3. (Directory form) every file on disk is referenced by the manifest, and
   vice versa — no silently-orphaned or silently-missing evidence.

## What this is not

Not a signature scheme — a sha256 proves content wasn't edited *after* the
manifest was written, not who wrote it or that the manifest itself wasn't
regenerated from scratch. Not a general JSON-schema validator — it checks
Providence's specific envelope, nothing about your `payload`'s own shape.
Not a replacement for `receipt` or `invariant` — see `SPEC.md`'s "Status"
section for exactly what is and isn't unified today. Not a secret
scanner — a bundle's `payload` validates identically whether it's been
redacted or not; see SPEC.md's "Redaction and secrets" for whose job
that actually is.

## Tests

```
python3 tests/test_providence.py
```

Assert-based, no framework, no fixtures beyond what each test builds
inline — including two tests that construct fixtures matching `receipt`'s
and `invariant`'s real, current output byte-for-shape (not imported
cross-repo, so this repo has zero dependency on either being installed)
and round-trip them through `convert_*` → `check_bundle` to prove the
converters work against real shapes, not just the canonical one.
