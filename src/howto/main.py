import platform
from pathlib import Path
from typing import Annotated, Type

import tomli_w
import typer
from litellm import completion
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
    TomlConfigSettingsSource,
)
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
    include_system_info: bool = False

    model_config = SettingsConfigDict(
        env_prefix="HOWTO_", toml_file=[DEFAULT_CONFIG_PATH]
    )

    # https://docs.pydantic.dev/latest/concepts/pydantic_settings/#other-settings-source
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # order is indicative of priority; most -> least
        return init_settings, env_settings, TomlConfigSettingsSource(settings_cls)

    def write_to_path(self, out_path: Path = DEFAULT_CONFIG_PATH):
        DEFAULT_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        print(f"writing {self.model_dump()} to {out_path}")
        with out_path.open("wb") as f:
            tomli_w.dump(self.model_dump(), f)

    def print(self):
        print(f"config path: {DEFAULT_CONFIG_PATH}")
        print(self.model_dump())


@app.command()
def main(
    query: Annotated[
        list[str] | None,
        typer.Argument(
            help="This is what you'd like to ask as a question. Empty queries will open a prompt."
        ),
    ] = None,
    verbose: Annotated[
        int, typer.Option("--verbose", "-v", help="Show debug logging", count=True)
    ] = False,
    dry_run: Annotated[bool, typer.Option(help="Make no requests to llms")] = False,
    config_path: Annotated[
        bool, typer.Option(help="Print the default config path and exit.")
    ] = False,
    config_show: Annotated[
        bool, typer.Option(help="Print the config and exit.")
    ] = False,
    set_model: Annotated[
        str | None, typer.Option(help="Set the model in the config file then run")
    ] = None,
    render_md: Annotated[
        bool,
        typer.Option(
            help="Ask not to render markdown on output. Will display unprocessed markdown."
        ),
    ] = True,
):
    """
    Get help for any query in your terminal with documented tool use.
    """
    config = Config()

    # Setting the model should set and persist but not run through
    if set_model:
        config.model = set_model
        config.write_to_path()
        return

    # Printing the config path should not run through
    if config_path:
        # we want to stop if only the config path is asked for
        print(DEFAULT_CONFIG_PATH)
        return

    # Showing the config should not run through
    if config_show:
        config.print()
        return

    if query:
        _query = " ".join(query)
    else:
        _query = typer.prompt("Whats your question?")

    _query.strip()

    if not _query.endswith("?"):
        _query += "?"

    if verbose > 0 or dry_run:
        print(f'config {config}')
        print(f'query "{_query}"')

    # Break before actually calling the LLM in question
    if dry_run:
        return

    try:
        if verbose > 1:
            print(system_messages)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Thinking...", total=None)

            content = f"Question:\n 'how to {_query}'"

            if config.include_system_info:
                    content +=  f" - user is on {platform.platform()}"

            response = completion(
                model=config.model,
                messages=[
                    *system_messages,
                    {
                        "content": f"{content}'\n\n Answer:",
                        "role": "user",
                    },
                ],
            )

        _response = response.choices[0].message.content

        if render_md:
            _response = Panel.fit(Markdown(_response))
        print(_response)

    except Exception as e:
        print("Something went wrong:", e)


if __name__ == "__main__":
    app()
