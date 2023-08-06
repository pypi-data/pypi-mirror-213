# Example where generative model is better than search:

footnote:[You.com search engine provides YouChat in addiation to conventional full text search. Neither will disguise ads as answers (https://you.com/chat).]



```text
AI: Good day! How may I help you?

Human: "How do I write the pyproject.toml dependencies line for an optional package e.g. haystack[faiss]?"

AI: The dependencies line for an optional package in pyproject.toml can be written using the brackets syntax. For example, to include the optional package faiss in haystack, the dependencies line would be:
```

```toml
[project]
# ...
[tool.poetry.dependencies]
# ...
haystack = { version = "*",  extra = ["faiss"] }
```

```text
This indicates that the version of haystack does not matter (hence *), and includes the faiss optional package. This assumes that poetry is used for dependency management.

Note that when using an optional package, it may be necessary to install additional system dependencies or configure the environment in a specific way. Consult the documentation of the package for details.
```

It's a bit verbose but gives references in case I need to dive even deeper.