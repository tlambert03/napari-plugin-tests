from pathlib import Path
from typing import List

from pydantic import BaseModel, Field, validator


def str2list(obj, field):
    if getattr(field.outer_type_, "__origin__", None) is list and isinstance(obj, str):
        return [obj]
    return obj


class _Config:
    extra = "forbid"
    validate_all = True


class Plugin(BaseModel):
    name: str
    hooks: List[str] = Field(default_factory=list)
    _str2list = validator("hooks", pre=True, allow_reuse=True)(str2list)

    Config = _Config


class TestCase(BaseModel):
    name: str
    plugins: List[Plugin] = Field(default_factory=list)
    deps: List[str] = Field(default_factory=list)
    conda_deps: List[str] = Field(default_factory=list)
    conda_channels: List[str] = Field(default_factory=list)
    commands: List[str] = Field(default_factory=list)

    _str2list = validator("*", pre=True)(str2list)

    Config = _Config

    def toxenv(self) -> str:
        from textwrap import indent

        lines = [f"[testenv:{self.name}]"]
        tox_fields = ("conda_deps", "conda_channels", "deps", "commands")
        for field_name in tox_fields:
            val = getattr(self, field_name)
            if not val:
                continue
            lines.append(f"{field_name} =")
            if field_name == "deps":
                val.insert(0, "{[testenv]deps}")
            lines.extend(indent(i, "  ") for i in val)
        return "\n".join(lines)

    @classmethod
    def from_file(cls, path: str) -> "TestCase":
        _path = Path(path)

        if _path.suffix.lower() in (".yml", "yaml"):
            from yaml import safe_load

            return cls(**{**safe_load(_path.read_text()), "name": _path.stem})


class TestSession(BaseModel):
    cases: List[TestCase]

    @classmethod
    def from_dir(cls, path: str):

        cases = [TestCase.from_file(c) for c in Path(path).glob("*.[ya|y]ml")]
        return cls(cases=cases)


if __name__ == "__main__":
    import sys
    from textwrap import indent

    CASE_DIR = Path(__file__).parent / "cases"
    errors = []
    for case_file in CASE_DIR.glob("*.[y|ya]ml"):
        try:
            case = TestCase.from_file(case_file)
            print(f"✅ {case.name}")
        except Exception as e:
            print(f"❌ {case_file.stem}\n{indent(str(e), '   ')}")
            errors.append(e)
    sys.exit(int(any(errors)))
