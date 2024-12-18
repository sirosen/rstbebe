# RST Baby!

bébé (noun, french): "baby"

`rstbebe` is a tool for all y'all who work in a polyglot environment with
markdown, restructured text, and maybe other markup languages (e.g. docbook).

## What's it do?

It's a linter and [`pre-commit`](https://pre-commit.com) hook for catching
`rst` files which have incorrect or undesirable syntax.

Right now, it will help you catch this incorrect use of backticks:
```
Use `snorkwozzle()` to `frob` your `multifropnibab`!
```

### Wait, aren't single-backticks valid RST syntax?

Depends what you mean.

It *is* valid syntax, but it creates a `title_reference`.
Usually, when people use single-backticks, if they're used to markdown, they
are making a mistake and mean to have inline code with double-backticks.

## How can I use it?

CLI:

```
pipx run rstbebe bad-backticks [FILES...]
```

or pre-commit config:

```yaml
- repo: https://github.com/sirosen/rstbebe
  rev: 0.1.0
  hooks:
    - id: bad-backticks
      files: changelog\.d/.*\.rst
```

## Contributing

`rstbebe` is maintained by one guy in his spare time. Be nice.

### Can it also check for $COMMON_RST_MISTAKE ?

Open an issue! Let's see what we can do.

### Can it also autofix $COMMON_RST_MISTAKE_WITH_CLEAR_FIX ?

Yep, that also sounds like a good idea!
For now it's a linter, but it can become a fixer as long as we can come up with
good (safe) rules.
