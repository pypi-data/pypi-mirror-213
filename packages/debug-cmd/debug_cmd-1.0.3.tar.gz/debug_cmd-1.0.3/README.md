# debug_cmd

## Installation

```shell
pip install debug_cmd
```

## How to use.

You need OpenAI key.

```shell
export OPENAI_API_KEY='your key'
```

Then,

```shell
debug_cmd ls /aaa
```

Or, if you want to use pipe `|` or redirect `>`, etc, you need to use -c option.

```shell
debug_cmd -c 'ls /aaa'
```
