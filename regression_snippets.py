import parser_syntax
import semantic


def _format_err(err):
    if not err:
        return "NO_ERROR"
    if isinstance(err, list):
        parts = []
        for e in err:
            if hasattr(e, "as_string"):
                parts.append("\n".join(str(x) for x in e.as_string()))
            else:
                parts.append(str(e))
        return "\n---\n".join(parts)
    if hasattr(err, "as_string"):
        return "\n".join(str(x) for x in err.as_string())
    return str(err)


def run_case(name: str, src: str, expect_syntax_error: bool, expect_semantic_error: bool):
    _, syn_err = parser_syntax.run(name, src)
    _, sem_err = semantic.run(name, src)

    syn_has = bool(syn_err)
    sem_has = bool(sem_err)

    ok = (syn_has == expect_syntax_error) and (sem_has == expect_semantic_error)

    print(f"\n== {name} ==")
    print(f"syntax:   {'ERROR' if syn_has else 'OK'}")
    if syn_has:
        print(_format_err(syn_err))

    print(f"semantic: {'ERROR' if sem_has else 'OK'}")
    if sem_has:
        print(_format_err(sem_err))

    if not ok:
        raise SystemExit(f"FAILED: {name} (expected syntax_error={expect_syntax_error}, semantic_error={expect_semantic_error})")


PLANT_PFX = "planting$\n"
PLANT_SFX = "perfection$\n"


def main():
    cases = []

    # ++ / newline delimiter cases
    cases.append((
        "unary_ok_same_line",
        PLANT_PFX + "pelican(){\n" + "crop I = 0$\nI++$\n}\n" + PLANT_SFX,
        False,
        False,
    ))

    cases.append((
        "unary_missing_dollar_newline",
        PLANT_PFX + "pelican(){\n" + "crop I = 0$\nI++\n}\n" + PLANT_SFX,
        True,
        True,
    ))

    # fall update clause with assignment update
    cases.append((
        "fall_update_assignment",
        PLANT_PFX
        + "pelican(){\n"
        + "crop I = 0$\n"
        + "fall(crop I = 0$ I < 3$ I = I + 1){\n"
        + "ship(\"x\")$\n"
        + "}\n"
        + "}\n"
        + PLANT_SFX,
        False,
        False,
    ))

    # harvest constraints
    cases.append((
        "harvest_in_pelican_rejected",
        PLANT_PFX + "pelican(){\nharvest 1$\n}\n" + PLANT_SFX,
        True,
        True,
    ))

    cases.append((
        "harvest_outside_craft_rejected",
        PLANT_PFX + "farmhouse crop A = 1$\nharvest A$\npelican(){\n}\n" + PLANT_SFX,
        True,
        True,
    ))

    cases.append((
        "harvest_last_in_craft_ok",
        PLANT_PFX
        + "craft Foo(){\n"
        + "crop A = 1$\n"
        + "harvest A$\n"
        + "}\n"
        + "pelican(){\n}\n"
        + PLANT_SFX,
        False,
        False,
    ))

    cases.append((
        "harvest_not_last_in_craft_rejected",
        PLANT_PFX
        + "craft Foo(){\n"
        + "crop A = 1$\n"
        + "harvest A$\n"
        + "ship(\"after\")$\n"
        + "}\n"
        + "pelican(){\n}\n"
        + PLANT_SFX,
        True,
        True,
    ))

    for name, src, exp_syn, exp_sem in cases:
        run_case(name, src, exp_syn, exp_sem)

    print("\nALL REGRESSION SNIPPETS PASSED")


if __name__ == "__main__":
    main()
