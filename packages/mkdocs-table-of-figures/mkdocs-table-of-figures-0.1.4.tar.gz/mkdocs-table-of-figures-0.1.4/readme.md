# mkdocs-table-of-figures

This is a plugin that creates a `figcaption` with image `alt` and lists all figures in files into a table of figures to be integrated in `Markdown` pages for MkDocs.

## Setup

### Installing using pip:

`pip install mkdocs-table-of-figures`

## Config

You need to activate the plugin in `mkdocs.yml`:

``` yaml
plugins:
  - table-of-figures:
      title_label: "Table of figures of the documentation" # Optional --> Default : Table of Figures
      figure_label: "Figure N°" # Optional --> Default : Figure
      description_label: "Description of the figures" # Optional --> Default : Description

      temp_dir: "folder_name" # Optional --> Default : temp_figures
      file: "file_name" # Optional --> Default : figures.md
```

As you can see, every option is optional, but if you want to generate a table of figures in another language than English, you will need to set up label options.

Set at least one annex to use this plugin. If you don't have any annex, don't add this plugin to the `MkDocs` plugins list in the config file `mkdocs.yml`.

- `title_label` - This is the title (heading 1) given to the page that will contain the table of figures.
- `figure_label` - This is the name given to every figure right before the auto-incremented number.
- `description_label` - This is the label given to the column containing the description of each figure (alt text).
- `temp_dir` - The temporary directory used to store the table of figures `Markdown` file before rendering to HTML. Only set this option if you already have a `temp_figures` folder in the root directory (same as `mkdocs.yml`), which you should not normally have.
- `file` - The name of the `Markdown` file containing the table of figures. Only set this option if you already have a `figures.md` file in the `docs` directory.

## Usage

The plugin will only look for `Markdown` image composed of alt text. If you don't set any alt text for the `Markdown` image it will be ignored.

There is two way of correctly rendering image stored within the docs:

- Using url from base: this mean that you give the full path from the docs directory starting with `/` like this `/path/to/image/from/docs/image.png`
- With the help of `md_in_html`: there is a `Markdown` extension that you can set in `mkdocs.yml` that allow the plugin to place `Markdown` in `HTML` which allow this plugin to let `MkDocs` set relative link in src attribute properly during `HTML` rendering

Concerning external images nothing change.

You can set the `md_in_html` option like so :

``` yaml
markdown_extensions:
  - md_in_html
```

Using the command `mkdocs build` or `mkdocs serve` will trigger the plugin if it has been set correctly in the config file.

## Support

This plugin currently supports markdown images and `mermaid` diagrams.

To make a `mermaid` diagram detectable by this plugin, you need to give it a title just below the end of the code block like this:

``` markdown
    ``` mermaid
    sequenceDiagram
        participant Alice
        participant Bob
        Alice->>John: Hello John, how are you?
        loop Healthcheck
            John->>John: Fight against hypochondria
        end
        Note right of John: Rational thoughts <br/>prevail!
        John-->>Alice: Great!
        John->>Bob: How about you?
        Bob-->>John: Jolly good!
    ```
    The title of the mermaid diagram go here
```

It will not work if there is a line between the diagram and the title.

I highly recommend using `mkdocs-material` to use `mermaid` diagrams. For more info about `mermaid` diagrams, I invite you to check `mkdocs-material` and `mermaid`'s official documentation.

## License

This project is under MIT license. See the `license` file for more details.

## See Also

- [GitLab Repo](http://www.gitlab.org/cfpt-mkdocs-plugins/mkdocs-annexes-integration/)
- [MkDocs Website](http://www.mkdocs.org/)
- [MkDocs-Material Documentation](https://squidfunk.github.io/mkdocs-material/)
- [Mermaid Documentation](https://mermaid.org/intro/)