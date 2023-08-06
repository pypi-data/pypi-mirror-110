from dataclasses import dataclass
from os import environ, name, system
from pathlib import Path
from typing import Any, Iterable, Optional
from unicodedata import category, normalize

from rich.console import Console
from rich.prompt import InvalidResponse, Prompt, PromptBase
from rich.table import Table
from rich.text import TextType
from rich.traceback import install

console = Console()

install(console=console)  # install traceback hook

WIN = name == "nt"


@dataclass
class Editor:
    extension: Optional[str] = ".cpp"
    path: Optional[str] = None
    env: Optional[dict[str, str]] = None

    def get_editor(self) -> str:
        if self.path is not None:
            return self.path
        for key in "VISUAL", "EDITOR":
            rv = environ.get(key)
            if rv:
                return rv
        if WIN:
            return "notepad"
        for editor in ("nvim", "vim", "nano"):
            if system(f"which {editor} >/dev/null 2>&1") == 0:
                return editor
        return "vi"

    def edit_file(self, filename: str) -> None:
        from subprocess import Popen

        editor = self.get_editor()
        env: Optional[dict[str, str]] = None

        if self.env:
            env = env.copy()  # type: ignore
            env.update(self.env)

        try:
            c = Popen(f'{editor} "{filename}"', env=env, shell=True)
            exit_code = c.wait()
            if exit_code != 0:
                raise SystemExit(f"{editor}: Editing failed")
        except OSError as e:
            raise OSError(f"{editor}: Editing failed: {e}") from e

    def edit(self, text: Optional[str]) -> Optional[str]:
        import tempfile

        if not text:
            data = b""
        elif isinstance(text, (bytes, bytearray)):
            data = text
        else:
            if text and not text.endswith("\n"):
                text += "\n"
            if WIN:
                data = text.replace("\n", "\r\n").encode("utf-8-sig")
            else:
                data = text.encode("utf-8")

        fd, name = tempfile.mkstemp(prefix="editor-", suffix=self.extension)

        try:
            with open(fd, "wb") as f:
                f.write(data)

            self.edit_file(name)

            with open(name, "rb") as f:
                rv = f.read()

            if isinstance(text, (bytes, bytearray)):
                return rv.decode("utf-8-sig").replace("\r\n", "\n")

            return rv.decode("utf-8-sig").replace("\r\n", "\n")  # type: ignore
        finally:
            Path(name).unlink()


class PromptPath(PromptBase[Path]):
    def __init__(
        self,
        prompt: TextType,
        *,
        console: Optional[Console],
        password: bool,
        choices: Optional[list[str]] = None,
        show_default: bool,
        show_choices: bool,
    ) -> None:
        super().__init__(
            prompt=prompt,
            console=console,
            password=password,
            choices=choices,
            show_default=show_default,
            show_choices=show_choices,
        )

    response_type = Path

    def process_response(self, value: str) -> Path:
        if not value:
            raise InvalidResponse("[b][prompt.invalid]You should enter a path.")
        path = Path(value).absolute()
        if not value or not path.exists():
            raise InvalidResponse(
                "[b][prompt.invalid]Path does not exist. Try with an absolute path."
            )
        return path.absolute()


@dataclass
class NoStructException(Exception):
    message: str

    def __str__(self) -> str:
        return self.message


prompt = Prompt


def edit(text: str):
    editor = Editor()
    code = editor.edit(text)
    code = code.split(text, 1)[1]
    return code.strip()


def add_includes(*, libs: list[str]) -> str:
    lib = ["#include " + (f"<{lib}>" if "/" not in lib else f'"{lib}"') for lib in libs]
    return "\n".join(lib) + "\n"


def build_cfn(
    ret: str,
    name: str,
    *,
    params: Optional[list[str]] = None,
    body: Optional[list[str]] = None,
    vret: Optional[str] = None,
) -> str:
    """Builds a Cpp function"""
    if body:
        body = ["  " + line for line in body]
    if ret == "string":
        ret = "std::string"
    return (
        f'{ret} {name}({", ".join(params or [])})\n'  # returntype functionName(type varname, for all params)
        + "{\n"  # {
        + (";\n".join(body) + ";\n" if body else "")  # function body
        + (f"  return {vret};\n" if ret != "void" else "")
        + "};\n"  # return varname;  # };
    )


def create_table(title: str, columns: Iterable[Any], rows: Iterable[Any] = None):
    table = Table(
        highlight=True,
        title=title,
        title_justify="center",
        show_header=True,
        show_lines=True,
    )
    for col in columns:
        table.add_column(col, justify="center")
    if rows:
        for row in rows:
            table.add_row(row)
    return table


def sanitize_name(fname: str) -> str:
    return "".join(
        c for c in normalize("NFD", fname) if category(c) != "Mn" and c != " "
    )
