from pydantic2ts import generate_typescript_defs
from pathlib import Path

PROJECT = Path(__file__).parents[1]
SCHEMAS = PROJECT / "ih" / "schema"
FRONTEND = PROJECT / "frontend" / "src" /  "api" / "types"

from pathlib import Path

# taken from mealie (https://github.com/mealie-recipes/mealie/blob/955e38ea0b99e5a38029e4ab5f529f27e6120957/dev/code-generation/gen_ts_types.py)
def path_to_module(path: Path):
    str_path: str = str(path)

    str_path = str_path.removeprefix(str(PROJECT))
    str_path = str_path.removeprefix("/")
    return str_path.replace("/", ".")

def main():

    for module in SCHEMAS.iterdir():
        if not module.is_dir() or not module.joinpath("__init__.py").is_file():
            continue

        name = module.name + ".ts"
        path = path_to_module(module)
        frontend_path = str(FRONTEND / name)
        generate_typescript_defs(path, frontend_path)



if __name__ == "__main__":
    main()

