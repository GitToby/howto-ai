<p align="center">
 <picture>
  <img alt="howto logo" src="https://github.com/GitToby/howto-ai/raw/main/docs/assets/logo.png">
</picture>
</p>

---

Dont know how to do something in your terminal?

```
howto print my system information?
```

And you'll be told!

```
╭────────────────────────────────────────────────────────────────────────────────╮
│ You can use the `uname -o` command to display your operating system.           │
│                                                                                │
│                                                                                │
│  uname -o                                                                      │
│                                                                                │
│                                                                                │
│ This command works with various Unix-like systems, including Linux and macOS.  │
│ If you're running a 64-bit kernel on an Apple M1 or ARM-based hardware, it     │
│ will return "Darwin" (the underlying OS name for macOS).                       │
╰────────────────────────────────────────────────────────────────────────────────╯
```

# Installing

`howto` is available on pypi and can be installed in any manner of ways

```shell
pip install howto-ai
```

```shell
pipx install howto-ai
```

```shell
uvx --from howto-ai howto
```

> **Note:** pre 1.0.0 release are assumed to be unstable and might break or do unexpected things, use wisely

# Usage

```shell
λ: howto --help

 Usage: howto [OPTIONS] [QUERY]...

╭─ Arguments ────────────────────────────────────────────────────────────────────╮
│   query      [QUERY]...  This is what you'd like to ask as a question. Empty   │
│                          queries will open a prompt.                           │
│                          [default: None]                                       │
╰────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────╮
│ --debug                 --no-debug            Make no requests to llms         │
│                                               [default: no-debug]              │
│ --dry-run               --no-dry-run          Make no requests to llms         │
│                                               [default: no-dry-run]            │
│ --config-path           --no-config-path      Print the default config path    │
│                                               and exit.                        │
│                                               [default: no-config-path]        │
│ --config-show           --no-config-show      Print the config and exit.       │
│                                               [default: no-config-show]        │
│ --install-completion                          Install completion for the       │
│                                               current shell.                   │
│ --show-completion                             Show completion for the current  │
│                                               shell, to copy it or customize   │
│                                               the installation.                │
│ --help                                        Show this message and exit.      │
╰────────────────────────────────────────────────────────────────────────────────╯
```

# Backends

`howto` uses 3rd party services as backends. By default, It's configured to use [ollama](https://ollama.com/) which is
expected to be running locally (make sure you read their docs). If it is, your `howto` commands will work.

`howto` can also be used against popular local, private and public AI APIs including ChatGPT, Gemini and others. To
configure this, you need to edit the config file. Locating the config file can be done with:

```shell
howto --config-path
```

Edit this in your favourite text editor. If this is difficult, please open an Issue and we can help.

### Open AI

Set the model you want by using the `--set-model` flag or updating the config file

```shell
howto --set-model 'gpt-4o'
```

or

```toml
model = "gpt-4o-mini"
# or
model = "gpt-4"
# ...
```

then export your `OPENAI_API_KEY` for that session (in your .envrc or .bashrc or wherever)

```shell
export OPENAI_API_KEY="<your key here>" # https://platform.openai.com/api-keys
```

and you should be good to go

### Hugging Face

Set the model you want by using the `--set-model` flag or updating the config file

```shell
howto --set-model 'huggingface/Qwen/Qwen2.5-Coder-32B-Instruct' # https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct
```

or

```toml
model = "huggingface/<hugging_face_model>"
# for example
model = "huggingface/facebook/blenderbot-400M-distill" # https://huggingface.co/facebook/blenderbot-400M-distill
# ...
```

then export your `HUGGINGFACE_API_KEY` for that session (in your .envrc or .bashrc or wherever)

```shell
export HUGGINGFACE_API_KEY="<your key here>" # https://huggingface.co/docs/hub/security-tokens
```

and you should be good to go

### Anthropic

Set the model you want by using the `--set-model` flag or updating the config file

```shell
howto --set-model 'claude-3-opus-latest' # https://docs.anthropic.com/en/docs/about-claude/models
```

or

```toml
model = "claude-3-5-sonnet-20241022"
# or
model = "claude-3-5-haiku-latest"
# ...
```

then export your `ANTHROPIC_API_KEY` for that session (in your .envrc or .bashrc or wherever)

```shell
export ANTHROPIC_API_KEY="<your key here>" # https://huggingface.co/docs/hub/security-tokens
```

and you should be good to go

> **Remember** AI can produce rubbish code, remember to research the commands `howto` spits out
