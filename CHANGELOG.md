# Changelog

All notable changes to this repository are recorded here. A version names a
tagged release: `v1.0` is the first release.

## v1.1 (2026-09-24)

- The task contract path in every specification is now `.dark/verify.sh` (the
  script at the root of a task's working tree that checks formatting, the build
  and the tests), following the rename in `dark`. This is the only change to a
  specification; the hidden acceptance and the reference solutions are
  untouched.
- `tasks/vmreap-plan` uses neutral machine names in its `qm` output fixtures
  instead of the names of the host they were taken from, and its task text
  states the requirement without the dated incident behind it.
- `README.md` gained a Terms section: each word this repository uses in its own
  sense (hidden acceptance, staging VM, acceptance set, oracle, mutant, start
  overlay, run record) is defined once, in plain words.

## v1.0

First release. The set at the content the `v1.0` tag names: 31 Go and Python
tasks, each with hidden acceptance tests, a reference solution, and for 14 of
them mutants that the tests must catch.
