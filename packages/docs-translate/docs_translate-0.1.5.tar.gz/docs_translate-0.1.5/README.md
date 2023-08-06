# Docs Translate

CLI tool to translate `.md` and `.rst` files from English to Korea and back.

Can use Yandex Translation API and Google Cloud translation.

## Installation

Install project:

```bash
$ pip install docs-translate
```

## Settings file

You can store your default settings in `.json` file.

Settings file content example:

```.json
{
  "target_dir":"D:\\{language_convert_dir}",
  "source_lang": "ko",
  "target_lang": "en",
  "service_name": "Google_v2",
}
```

If you set config file, you should specify it with `-c CONFIG_PATH` argument!

## Usage

```bash
$ docs-translate [-h] [-c CONFIG_PATH]
               [-s {Google,Google_v2}] [-S] [-T]
               [-path {source_path}] [-d {target_dir}]
```

If you set config file, you can override any of settings by arguments

### Positional arguments:
* `path` Path to folder to process. If not set, uses current folder
* `-d TARGET_DIR, --target_dir TARGET_DIR`, If not set, the target_dir in config.json is set

### Optional arguments:
* `-h, --help`, show this help message and exit
* `-c CONFIG_PATH, --config_path CONFIG_PATH`, Path to config_file
* `-s {Yandex,Google,Bing,Deepl}, --service_name {Yandex,Google,Bing,Deepl}`, Translating service
* `-S SOURCE_LANG, --source_lang SOURCE_LANG`, Source language code
* `-T TARGET_LANG, --target_lang TARGET_LANG`, Target language code

### Translation services:
Now used `Yandex`, `Google`, `Bing`, `Deepl`, `Google_v2`

Some of them can be not working, try it and find the most suitable for you  

`Google --> It's free, but the translation isn't good.`  
`Google_v2 --> need to google Cloud Translation API key.` 