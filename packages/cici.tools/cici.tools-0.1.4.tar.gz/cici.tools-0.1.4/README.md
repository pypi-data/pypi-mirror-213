# cici.tools

<!-- BADGIE TIME -->

[![brettops tool](https://img.shields.io/badge/brettops-tool-209cdf?labelColor=162d50)](https://brettops.io)
[![pipeline status](https://img.shields.io/gitlab/pipeline-status/brettops/tools/cici?branch=main)](https://gitlab.com/brettops/tools/cici/-/commits/main)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![code style: black](https://img.shields.io/badge/code_style-black-000000.svg)](https://github.com/psf/black)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg)](https://github.com/prettier/prettier)

<!-- END BADGIE TIME -->

> **WARNING:** `cici` is experimental and I can't even decide on a name for it.
> Stay away!

## Usage

### `bundle`

### `build`

The `build` subcommand introduces BrettOps Pipeline format, a pipeline format
that compiles into other pipeline formats.

BrettOps Pipelines are simple and easy to write, and can be compiled to any
format.

They can also be executed locally with the included runner.

### `update`

## About BrettOps CI syntax

- All data is strictly ordered and evaluated sequentially.

- All jobs / pipelines are named.

- Scripts, variables, and other snippets can be loaded from disk at build time.

- Includes are evaluated at build time.

- Can convert to GitLab CI for use with GitLab.

- Uses Argo Workflow-style templating for vendor-neutral variables.

## Example

Here is a BrettOps pipeline, saved as `.brettops-pipeline.yml`:

```yaml
name: marp

stages:
  - name: test
  - name: build
  - name: deploy

inputs:
  - name: opts
  - name: footer
  - name: format_opts
  - name: svg_png_dpi
    default: "200"
  - name: theme_url

jobs:
  - name: build
    stage: build
    environment:
      image: registry.gitlab.com/brettops/containers/marp:main
    outputs:
      - type: path
        name: public
        value: public/
    scripts:
      - script:
          - marp --version
          - echo "${{input.format_opts}}"

          # inject a theme into the local environment if present
          - |-
            if [[ -n "${{input.theme_url}}" ]] ; then
              marp_theme_file="$(mktemp -u).css"
              wget -O "$marp_theme_file" "${{input.theme_url}}"
              {{input.opts}}="${{input.opts}} --theme $marp_theme_file"
            fi
          - echo "${{input.opts}}"
          # preprocess slides with marp-format
          - mapfile -t SLIDES < <(find . -name slides.md -type f -not -path "./public/*")
          - |-
            for slide in "${SLIDES[@]}"
            do
              preprocess="$(echo "$slide" | sed -e 's@slides\.md$@index.md@')"
              echo "preprocessing '$slide' to '$preprocess'"
              marp-format --output "$preprocess" "$slide" --metadata "footer=${{input.footer}}" ${{input.format_opts}}
            done

          # run marp on preprocessed slides
          - mapfile -t PREPROCESSED < <(find . -name index.md -type f)
          - marp ${{input.opts}} --html "${PREPROCESSED[@]}"
          - marp ${{input.opts}} --allow-local-files --pdf "${PREPROCESSED[@]}"

          # marshal into public directory
          - >-
            rsync -zarv
            --exclude ".git/"
            --exclude "public/"
            --include "*/"
            --include "index.html"
            --include "index.md"
            --include "index.pdf"
            --include "*.jpg"
            --include "*.png"
            --include "*.svg"
            --exclude "*"
            . public/
```

This format is intentionally verbose, as it is designed to transpile into other
formats. It is also designed to generate pipeline documentation in a literate
style. It is also intended to support being run locally using a built-in
pipeline orchestrator.

### Export to GitLab CI

```bash
cici build -t gitlab
```

```yaml
stages:
  - test
  - build
  - deploy

workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "push" && $CI_OPEN_MERGE_REQUESTS
      when: never
    - when: always

variables:
  MARP_OPTS: ""
  MARP_FOOTER: ""
  MARP_FORMAT_OPTS: ""
  MARP_SVG_PNG_DPI: "200"
  MARP_THEME_URL: ""

marp-build:
  stage: build
  image: registry.gitlab.com/brettops/containers/marp:main
  script:
    - marp --version
    - echo "$MARP_FORMAT_OPTS"
    - |-
      if [[ -n "$MARP_THEME_URL" ]] ; then
        marp_theme_file="$(mktemp -u).css"
        wget -O "$marp_theme_file" "$MARP_THEME_URL"
        MARP_OPTS="$MARP_OPTS --theme $marp_theme_file"
      fi
    - echo "$MARP_OPTS"
    - mapfile -t SLIDES < <(find . -name slides.md -type f -not -path "./public/*")
    - |-
      for slide in "${SLIDES[@]}"
      do
        preprocess="$(echo "$slide" | sed -e 's@slides\.md$@index.md@')"
        echo "preprocessing '$slide' to '$preprocess'"
        marp-format --output "$preprocess" "$slide" --metadata "footer=$MARP_FOOTER" $MARP_FORMAT_OPTS
      done
    - mapfile -t PREPROCESSED < <(find . -name index.md -type f)
    - marp $MARP_OPTS --html "${PREPROCESSED[@]}"
    - marp $MARP_OPTS --allow-local-files --pdf "${PREPROCESSED[@]}"
    - >-
      rsync -zarv --exclude ".git/" --exclude "public/" --include "*/" --include "index.html"
      --include "index.md" --include "index.pdf" --include "*.jpg" --include "*.png"
      --include "*.svg" --exclude "*" . public/
  artifacts:
    paths:
      - public/
```
