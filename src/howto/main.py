from pathlib import Path
from typing import Annotated

import typer
from litellm import completion
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich import print
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from howto.examples import system_messages

APP_NAME = "howto-ai"
DEFAULT_CONFIG_PATH = Path(typer.get_app_dir(APP_NAME)) / "config.toml"
app = typer.Typer(name=APP_NAME)


class Config(BaseSettings):
    model: str = "ollama_chat/llama3.2"
    md_print: bool = True

    model_config = SettingsConfigDict(
        env_prefix="HOWTO_", toml_file=[DEFAULT_CONFIG_PATH]
    )


@app.command()
def main(
        query: Annotated[
            list[str] | None,
            typer.Argument(
                help="This is what you'd like to ask as a question. Empty queries will open a prompt."
            ),
        ] = None,
        debug: Annotated[bool, typer.Option(help="Make no requests to llms")] = False,
        dry_run: Annotated[bool, typer.Option(help="Make no requests to llms")] = False,
        config_path: Annotated[
            bool, typer.Option(help="Print the default config path and exit.")
        ] = False,
        show_config: Annotated[
            bool, typer.Option(help="Print the config and exit.")
        ] = False,
):
    config = Config()

    # Writes default config path if its not there already
    # if not DEFAULT_CONFIG_PATH.exists():
    #     DEFAULT_CONFIG_PATH.parent.mkdir(mode=0o006, parents=True, exist_ok=True)
    #     toml.dump(config.model_dump(), DEFAULT_CONFIG_PATH.open("w+"))

    if config_path:
        # we want to stop if only the config path ias asked for
        print(DEFAULT_CONFIG_PATH)
        return

    if show_config:
        print(f"config@'{DEFAULT_CONFIG_PATH}'")
        print(config.model_dump())
        return

    if debug:
        print(f"Currint config @ {DEFAULT_CONFIG_PATH}:")
        print(config.model_dump())

    if query:
        _query = " ".join(query)
    else:
        _query = typer.prompt("Whats your question?")

    if not _query.endswith("?"):
        _query += " ?"

    # Print the post setup debug info if required.
    if debug or dry_run:
        print(f'calling {config.model}: "{_query}"')

    # Break before actually calling the LLM in question
    if dry_run:
        return

    try:
        if debug:
            print(system_messages)

        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
        ) as progress:
            progress.add_task(description="Thinking...", total=None)
            response = completion(
                model=config.model,
                messages=[*system_messages, {"content": f"Question:\n 'how to {_query}' \n\n Answer:", "role": "user"}],
            )

        _response = response.choices[0].message.content

        if config.md_print:
            _response = Panel.fit(Markdown(_response))
        print(_response)

    except Exception as e:
        print("Something went wrong:", e)


if __name__ == "__main__":
    app()
