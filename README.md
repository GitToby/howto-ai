<p align="center">
 <picture>
  <img alt="howto logo" src="docs/assets/logo.png">
</picture>
</p>

---

Dont know how to do something in your terminal?

```
howto print my system information?
```

And you'll be told!

```
╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ You can use the system_profiler command on macOS to print detailed system information. For example:          │
│                                                                                                              │
│                                                                                                              │
│  system_profiler SPHardwareDataType                                                                          │
│                                                                                                              │
│                                                                                                              │
│ This command will display detailed information about your Mac's hardware, including the model name,          │
│ processor, number of processors, total number of cores, memory, and other hardware specifics. For more       │
│ comprehensive system information, you can run:                                                               │
│                                                                                                              │
│                                                                                                              │
│  system_profiler                                                                                             │
│                                                                                                              │
│                                                                                                              │
│ This command provides an extensive report on hardware, software, and network configurations. It may take a   │
│ few moments to complete due to the amount of information it gathers.                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
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

# Backends

`howto` uses 3rd party services as backends. By default` configured to use [ollama](https://ollama.com/) which is expected to be running locally. If it
is, it should just start.

`howto` can also be used against popular local, private and public AI APIs including ChatGPT, Gemini and others. To
configure this, you need to edit the config file. Locating the config file can be done with:

```shell
howto --config-path
```

Edit this in your favourite text editor. If this is difficult, please open an Issue and we can help.

### Open AI

Set the model you want by updating the config file

```toml
model = "gpt-4o"
# or
model = "gpt-4"
# or
model = "gpt-3.5-turbo"
# ...
``` 

then export your `OPENAI_API_KEY` for that session (in your .envrc or .bashrc or wherever)

```shell
export OPENAI_API_KEY="<your key here>" # https://platform.openai.com/api-keys
```
and you should be good to go


### Hugging Face
Set the model you want by updating the config file

```toml
model = "huggingface/<hugging_face_model>"
# for example
model = "huggingface/facebook/blenderbot-400M-distill" # https://huggingface.co/facebook/blenderbot-400M-distill
# or
model = "Qwen/Qwen2.5-Coder-32B-Instruct" # https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct
# ...
``` 

then export your `HUGGINGFACE_API_KEY` for that session (in your .envrc or .bashrc or wherever)

```shell
export HUGGINGFACE_API_KEY="<your key here>" # https://huggingface.co/docs/hub/security-tokens
```
and you should be good to go

### Anthropic
Set the model you want by updating the config file

```toml
model = "claude-3-5-sonnet-20241022" # https://docs.anthropic.com/en/docs/about-claude/models
# or 
model = "claude-3-5-haiku-latest"
# or
model = "claude-3-opus-latest"
# ...
``` 

then export your `ANTHROPIC_API_KEY` for that session (in your .envrc or .bashrc or wherever)

```shell
export ANTHROPIC_API_KEY="<your key here>" # https://huggingface.co/docs/hub/security-tokens
```
and you should be good to go

> **Remember** AI can produce rubbish code, remember to research the commands `howto` spits out