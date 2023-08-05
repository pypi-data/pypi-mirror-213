# langdash

[**Announcement post**](https://mysymphony.jp.net/a/langdash-announcement/)

A simple library for interfacing with language models.

**Currently in alpha!**

Features:
  
  * Support for text generation, text classification (through prompting) and vector-based document searching.
  * Lightweight, build-it-yourself-style prompt wrappers.
  * Token healing and transformers/RNN state reuse for fast inference, like in [Microsoft's guidance](https://github.com/microsoft/guidance).
  * First-class support for ggml backends.

Documentation: [Read on readthedocs.io](https://langdash.readthedocs.io/en/latest/)

## Installation

Use [pip](https://pip.pypa.io/en/stable/) to install. By default, langdash does not come preinstalled with any additional modules. You will have to specify what you need like in the following command:

```
pip install --user langdash[embeddings,sentence_transformers]
```

List of modules:
  
  * **core:**
    * *embeddings:* required for running searching through embeddings
  * **backends:**
    * Generation backends: *rwkv_cpp*, *llama_cpp*, *transformers*
    * Embedding backends: *sentence_transformers*

**Note:** If running from source, initialize the git submodules in the `langdash/extern` folder to compile foreign backends.
    
## Usage

Examples:

  * [Text generation](https://git.mysymphony.jp.net/nana/langdash/src/branch/master/docs/examples/text-generation.md)
  * [Generating TV shows](https://git.mysymphony.jp.net/nana/langdash/src/branch/master/docs/examples/generating-tv-shows.md)
  * [Embedding search](https://git.mysymphony.jp.net/nana/langdash/src/branch/master/docs/examples/embedding-search.md)

See [examples folder](https://git.mysymphony.jp.net/nana/langdash/src/branch/master/examples) for full examples.

## License

Apache 2.0