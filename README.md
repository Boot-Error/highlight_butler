# Highlight Butler

Higlight Butler collects highlights from different services and creates notes for reference in your note taking system.

# Usage

Highlight Butler is installed as a Python Package using `pip`

```sh
# install using pip
pip install git+https://github.com/Boot-Error/highlight_butler

# create a config file
curl https://github.com/Boot-Error/highlight_butler/blob/main/highlight_butler/resources/config.yaml -O config.yaml

# add hypothesis API keys
# add notes directory
# add markdown template
highlight_butler --config config.yaml
```