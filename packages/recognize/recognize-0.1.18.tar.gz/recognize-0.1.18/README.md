# Recognizes

This CLI allows you to upload files to the ML Pipeline and query results.

## First Steps

You first need to make sure that you have the requirements needed to install the CLI as well as install the CLI itself.

Make sure that you have `python` and `pip` installed. It is recommended that you use a virtual environment although not
a requirement.

Then to install the CLI run the following command in your shell:

```bash
pip install recognize
```

## Usage

After installing the CLI run the following command:

```bash
recognize --help
```

This should show you a list of all the available commands with a short description of what they do. You can append
the `--help` option to each command for more details about the command. For example:

```bash
recognize upload --help
```

This should give you a list of all the subcommands for this command, the options, and the order in which to write them.

### Examples

To upload a directory of videos, accepted file types are `mp4` and `mov`:

```bash
recognize upload directory --output results.csv path/to/directory/of/videos
```

After uploading videos it will take a few minutes to process them all. After which you can start querying.

```bash
recognize search keywords --output results.csv some interesting words
```

You can also search for specific entry types returned by AWS Rekognition. For example to which resources might have
potentially harmful, violent, or offensive content run the following command:

```bash
recognize search entries --output results.csv moderation
```

Finally, to search for a particular face run the following command, accepted file types are `png` and `jpeg`:

```bash
recognize search faces --output results.csv file/path/to/image/of/face
```

### Results




