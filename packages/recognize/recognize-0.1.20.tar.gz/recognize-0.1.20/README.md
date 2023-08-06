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
recognize upload directory path/to/directory/of/videos --tag some_custom_tag
```

The tag is useful for if you want to organise the uploads. You can search for labels associated with the tag and you can
upload files using this tag at a later stage, and they will be automatically grouped.

After uploading videos it will take a few minutes to process them all. After which you can start querying.

```bash
recognize search keywords --output results.csv some interesting words
```

The `--output` argument is optional, if ommited you will be asked what to name the output interactively instead.

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

For keyword and entry search the columns in the csv (or keys in the records for the json output) will be:

| Column             | Description                                                           |
|--------------------|-----------------------------------------------------------------------|
| id                 | The unique identifier for the entry.                                  |
| average_confidence | The average confidence score.                                         |
| confidences        | The list of confidence scores.                                        |
| entry_type         | The type of entry. Either label, alias, category, parent, moderation. |
| name               | The value associated with the entry.                                  |
| timestamps         | The timestamps related to the entry.                                  |
| url                | The S3 bucket URL of the associated video.                            |
| tag                | The tag related to the entry.                                         |

The faces search will have the following columns (or keys):

| Column                 | Description                                              |
|------------------------|----------------------------------------------------------|
| faceId                 | The unique identifier for the face.                      |
| imageId                | The unique identifier for the image.                     |                                                          |
| externalImageId        | The path to the resource in the S3 bucket with metadata. |
| similarity             | The similarity of the face to the input image.           |
| searchedFaceConfidence | Confidence in whether a face was detected in the input.  |
| timestamp              | The timestamp of the face. In milliseconds.              |





