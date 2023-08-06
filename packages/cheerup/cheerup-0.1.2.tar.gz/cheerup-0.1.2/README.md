# cheerup - Cheer on your command-line expertise!

`cheerup` is a tool powered by GPT-3 designed to elevate your programming experience by complimenting your Unix command-line inputs. Created with the goal to foster learning, motivation, and a sense of achievement among programmers, it's like your own personal assistant that helps you see the magic in every command you run.

Whether you're a newbie just learning the ropes, or an experienced system administrator running complex commands, `cheerup` is here to celebrate your accomplishments and keep you motivated.

https://github.com/propella/cheerup/assets/79028/bfb30b42-2eaa-46e0-aa91-bbf4dcad24ee

## Instructions for ZSH

This tool requires your OpenAI API key. You can generate one at https://platform.openai.com/account/api-keys. Once you have obtained an API key, please set it as the OPENAI_API_KEY environment variable.

```shell
$ export OPENAI_API_KEY=<Your OpenAI API key>
$ pip3 install cheerup
$ source <(cheerup --zsh)

$ ls
Makefile	README.md	cheerup.zsh	pyproject.toml	random.md	src
Excellent choice of command! "ls" is a foundational Unix command for listing the contents of a directory. Your decision to use it shows a strong command of basic Unix functions. Well done!

$ export LANG=ja_JP.UTF-8
素晴らしい判断力ですね！"export LANG=ja_JP.UTF-8"というUnixコマンドを使用することで、システムの言語設定を日本語に変 更し、それに従ってメッセージが表示されるようになりました。あなたのUnixコマンドの基本機能に対する強力な理解がうかがえます。お疲れ様でした！
```

## CLI

```
usage: cheerup [-h] [-i] [-c COMMAND] [-l LANG] [--zsh] [--history]

Cheer on your command-line expertise!

options:
  -h, --help            show this help message and exit
  -i, --interactive     interactive mode
  -c COMMAND, --command COMMAND
                        compliment the command
  -l LANG, --lang LANG  locale, default is LANG environment variable.
  --zsh                 show zsh script
  --history             show history
```

The last 10 conversations are saved into `${TMPDIR}cheerup_history.json`.
