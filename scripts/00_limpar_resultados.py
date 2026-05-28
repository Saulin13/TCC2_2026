from __future__ import annotations

import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RESULTS_DIR = BASE_DIR / "data" / "results"
TESTS_GENERATED_DIR = BASE_DIR / "tests" / "generated"
TESTS_LEGACY_DIR = TESTS_GENERATED_DIR / "legacy"

COVERAGE_FILES = [
    BASE_DIR / ".coverage",
    BASE_DIR / "coverage.json",
]

PYCACHE_TARGETS = [
    BASE_DIR / "scripts",
    TESTS_GENERATED_DIR,
]

RECREATE_DIRS = [
    BASE_DIR / "data" / "results",
    BASE_DIR / "data" / "results" / "plots",
    BASE_DIR / "data" / "results" / "plots" / "thealgorithms",
    BASE_DIR / "data" / "results" / "plots" / "real",
    BASE_DIR / "data" / "results" / "generated_prompts",
    BASE_DIR / "data" / "results" / "generated_prompts" / "thealgorithms" / "gpt",
    BASE_DIR / "data" / "results" / "generated_prompts" / "thealgorithms" / "claude",
    BASE_DIR / "data" / "results" / "generated_prompts" / "real" / "gpt",
    BASE_DIR / "data" / "results" / "generated_prompts" / "real" / "claude",
    BASE_DIR / "data" / "results" / "logs",
    BASE_DIR / "tests" / "generated" / "thealgorithms" / "gpt",
    BASE_DIR / "tests" / "generated" / "thealgorithms" / "claude",
    BASE_DIR / "tests" / "generated" / "real" / "gpt",
    BASE_DIR / "tests" / "generated" / "real" / "claude",
]


def _collect_contents(path: Path, *, exclude: frozenset[Path] | None = None) -> list[Path]:
    if not path.exists() or not path.is_dir():
        return []
    excluded = exclude or frozenset()
    return sorted(
        (p for p in path.iterdir() if p.resolve() not in excluded),
        key=lambda p: p.as_posix(),
    )


def _collect_pycache_dirs(root: Path) -> list[Path]:
    if not root.exists() or not root.is_dir():
        return []
    return sorted(
        [p for p in root.rglob("__pycache__") if p.is_dir()],
        key=lambda p: p.as_posix(),
    )


def _remove_path(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink(missing_ok=True)


def _rel(path: Path) -> str:
    try:
        return path.relative_to(BASE_DIR).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    to_remove: list[Path] = []

    to_remove.extend(_collect_contents(RESULTS_DIR))
    legacy_exclude = frozenset({TESTS_LEGACY_DIR.resolve()})
    to_remove.extend(
        _collect_contents(TESTS_GENERATED_DIR, exclude=legacy_exclude)
    )
    to_remove.extend([p for p in COVERAGE_FILES if p.exists()])

    for root in PYCACHE_TARGETS:
        to_remove.extend(_collect_pycache_dirs(root))

    unique_to_remove = sorted(set(to_remove), key=lambda p: p.as_posix())

    print("Itens que serão limpos:")
    if not unique_to_remove:
        print("- Nenhum arquivo/pasta gerado encontrado.")
    else:
        for item in unique_to_remove:
            print(f"- {_rel(item)}")

    confirmacao = input("\nDigite SIM para confirmar a limpeza: ").strip()
    if confirmacao != "SIM":
        print("Limpeza cancelada. Nada foi apagado.")
        return

    for item in unique_to_remove:
        _remove_path(item)

    for directory in RECREATE_DIRS:
        directory.mkdir(parents=True, exist_ok=True)

    print("\nLimpeza concluída com sucesso.")
    print("Pastas recriadas:")
    for directory in RECREATE_DIRS:
        print(f"- {_rel(directory)}")


if __name__ == "__main__":
    main()
