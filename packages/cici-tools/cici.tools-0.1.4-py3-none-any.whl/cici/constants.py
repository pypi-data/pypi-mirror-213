from pathlib import Path

BASE_DIR = Path(__file__).parent.absolute()

SCHEMA_DIR = BASE_DIR / "schema"

PROVIDER_DIR = BASE_DIR / "providers"

PROVIDERS = sorted(
    [path.stem for path in PROVIDER_DIR.glob("*.py") if not path.stem.startswith("_")]
    + [
        path.stem
        for path in PROVIDER_DIR.glob("*/")
        if path.is_dir() and not path.stem.startswith("_")
    ]
)
