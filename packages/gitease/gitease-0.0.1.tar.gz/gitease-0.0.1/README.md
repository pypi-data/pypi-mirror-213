# GitEase

A tool to simplify git usage with sprinkles of AI magic.

Humans think in simpler terms than git operates in. This tool aims to bridge that gap by providing a simpler language to
do common git tasks. Plus an LLM can write your commit messages for you.

You can load recent information with `gs load`, save current changes with `gs save` and share them with `gs share`.    
Behind the scenes it's exactly what you would expect from git, but with a simpler interface.

## Install

* Get an [openai api key](https://platform.openai.com/account/api-keys)

```bash
$ export OPENAI_API_KEY=...
$ pip install simpgit
```
* If OPENAI_API_KEY is not set, you will be prompted to enter a commit message manually.

## Usage

Within a repo, run:

```bash 
(.venv) $ ge --help
```

```bash
Commands:
  --help: show this help message and exit    
    save <message>: add files and commit changes. Massage is genereated if not provided         
    share <message>: Add, commit and push changes to git. Massage is genereated if not provided
    load : pull changes from git    
    commit <message>: commit changes. Massage is genereated if not provided

Automations:
  auto <save|share> <interval> --<detach>: run a service
  list <save|share>: list running services
  stop <save|share>: stop a service
```

## Basic Example
```bash
ge save

> Entering new StuffDocumentsChain chain...


> Entering new LLMChain chain...
Prompt after formatting:
Write a concise summary of the following:
...
> Finished chain.
Automated commit - 4 files:
 writing README.md new instructions.
gitease/__init__.py
gitease/cli.py
gitease/git.py
pyproject.toml
```

## Automation Example
```bash
$ ge auto commit 5 --detach
Running auto commit every 5.0 minutes in the background

$ ge list commit
Auto commit every 5.0 on pid 96641  in repo at /Users/yonatanalexander/development/xethub/gitease

$ ge stop commit
Stopping auto-git commit - in <repo>
Stopping processes for commit...
Stopped auto 96641..
```
