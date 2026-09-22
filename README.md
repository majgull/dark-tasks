# dark-tasks

The task set that [dark](https://github.com/majgull/dark) measures models on: 31 small Go and Python tasks with known answers, each with hidden acceptance tests, a reference solution, and for 14 of them deliberately broken solutions that the tests must catch. The tag `v1.0` is the set the paper [dark-paper](https://github.com/majgull/dark-paper) used; its run records name it `acceptance-v4`, the name it carried in the private tree, and the tag sits on identical content.

## A task

```
tasks/<id>/task.toml      id (= directory), title, class (additive | mechanical | repair), lang (go | python), spec, may_edit
tasks/<id>/start/         files laid over the language template before the run (optional)
tasks/<id>/acceptance/    hidden: run.sh (+ fixtures). Runs in a fresh machine at the repo root; prints `CHECK <name> ok|fail` lines; exit 0 = pass
tasks/<id>/oracle/        a reference solution overlay, used only to validate the acceptance set (never shown to a model)
mutants/<id>/<name>/      a solution broken on purpose; every mutant must fail at least one hidden check
```

The model sees the language template, `start/` and `spec`. Nothing else. `may_edit` is the only way an existing file may be rewritten, and additive tasks grant none. A task may follow another (`after = "<id>"`): `obs-01-parse` to `obs-06-typehints` build one product over six steps, and `obs-all` is the same product from one specification.

## Checking the set

From a checkout of `dark`, with this repository beside it:

```
cd bench && python3 tools/check_tasks.py ../../dark-tasks     # 31 tasks, 0 problems
```

`DARK_TASKS=<path to this checkout>` makes every bench tool read this set instead of the two example tasks that `dark/bench/tasks` keeps for reference. The reference solutions and the mutants are checked with `tools/validate.py` and `tools/mutants.py` there; section 5.1 of the paper is what those checks found.

## Provenance and licence

Written by language models under one person's direction, imported here from a private tree with private identifiers replaced by role names; the paper's section 8 says who did what. Dedicated to the public domain under CC0 1.0 Universal; `LICENSE` is its text. Cite the paper, not this repository.
