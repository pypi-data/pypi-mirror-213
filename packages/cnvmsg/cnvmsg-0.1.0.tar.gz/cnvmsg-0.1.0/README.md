# ConventionalMessage
Conventional Message handling.

> ⚠️ WARNING: Poorly tested, error-prone. Works well only with perfectly matched strings.

## What is Conventional Message?
A specification for domain-agnostic message which helps in better describing of the context:
```
%<condition>% [<status>] <project>/<type>(<module>)!: <text> #<...tags>
```

Inspired by [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) and [Angular commits](https://gist.github.com/brianclements/841ea7bffdb01346392c) and is compliant *in some forms* to it.

## Conventional Message Examples
Full:
```
%after closing #8b78% [maybe] orwynn/refactor(bootscript): Rearrange bootscript structure #awaiting #nextrelease
```

General feature:
```
orwynn/feat(di): advanced sharing container
```

Condition:
```
%if noone called% call service for further information
```
