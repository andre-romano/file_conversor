
# File Conversor v0.4.0

**Summary**:
- [File Conversor v0.4.0](#file-conversor-v040)
  - [Feature-set available](#feature-set-available)
    - [Office files (doc, xls, ppt, etc)](#office-files-doc-xls-ppt-etc)
    - [Audio / Video files](#audio--video-files)
    - [Image files](#image-files)
    - [PDF files](#pdf-files)
    - [Text files (json, yaml, ini, etc)](#text-files-json-yaml-ini-etc)
    - [Hash files (sha256, md5, etc)](#hash-files-sha256-md5-etc)
    - [Windows utilities](#windows-utilities)
    - [App configuration](#app-configuration)
    - [Processing pipelines](#processing-pipelines)

## Feature-set available

### Office files (doc, xls, ppt, etc)

| Command     | Description                        | Input formats  | Output formats                 |
| ----------- | ---------------------------------- | -------------- | ------------------------------ |
| doc convert | Converts document file formats     | doc, docx, odt | doc, docx, odt, pdf, html      |
| ppt convert | Converts presentation file formats | ppt, pptx, odp | ppt, pptx, odp, pdf            |
| xls convert | Converts spreadsheet file formats  | xls, xlsx, ods | xls, xlsx, ods, csv, pdf, html |

### Audio / Video files

| Command             | Description                       | Input formats                                                                                                 | Output formats                                 |
| ------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| audio-video info    | Gets information about file       | aac, ac3, flac, m4a, mp3, ogg, opus, wav, 3gp, asf, avi, flv, h264, hevc, m4v, mkv, mov, mp4, mpeg, mpg, webm | No output file                                 |
| audio-video convert | Converts audio/video file formats | aac, ac3, flac, m4a, mp3, ogg, opus, wav, 3gp, asf, avi, flv, h264, hevc, m4v, mkv, mov, mp4, mpeg, mpg, webm | mp4, avi, mkv, webm, mp3, m4a, ogg, opus, flac |

### Image files


| Command        | Description                                                 | Input formats                                                  | Output formats                                                 |
| -------------- | ----------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------- |
| image info     | Get EXIF information about a image file                     | bmp, gif, ico, jfif, jpg, jpeg, jpe, png, psd, tif, tiff, webp | No output file                                                 |
| image convert  | Converts image file formats                                 | bmp, gif, ico, jfif, jpg, jpeg, jpe, png, psd, tif, tiff, webp | bmp, gif, ico, jpg, apng, png, pdf, tif, webp                  |
| image render   | Render image vector file into bitmap image                  | svg                                                            | png, jpg                                                       |
| image to-pdf   | Convert list of images into a PDF file (one image per page) | bmp, gif, jpeg, jpg, png, tiff, tif                            | pdf                                                            |
| image compress | Compresses image files                                      | gif, jpg, jpeg, png                                            | gif, jpg, jpeg, png                                            |
| image mirror   | Mirror an image file (vertically or horizontally)           | bmp, gif, ico, jfif, jpg, jpeg, jpe, png, psd, tif, tiff, webp | bmp, gif, ico, jfif, jpg, jpeg, jpe, png, psd, tif, tiff, webp |
| image resize   | Resize an image file.                                       | bmp, gif, ico, jfif, jpg, jpeg, jpe, png, psd, tif, tiff, webp | bmp, gif, ico, jfif, jpg, jpeg, jpe, png, psd, tif, tiff, webp |
| image rotate   | Rotate a image file (clockwise or anti-clockwise)           | bmp, gif, ico, jfif, jpg, jpeg, jpe, png, psd, tif, tiff, webp | bmp, gif, ico, jfif, jpg, jpeg, jpe, png, psd, tif, tiff, webp |


### PDF files


| Command         | Description                                                      | Input formats | Output formats     |
| --------------- | ---------------------------------------------------------------- | ------------- | ------------------ |
| pdf encrypt     | Protect PDF file with a password (create encrypted PDF file)     | pdf           | pdf                |
| pdf decrypt     | Remove password protection from a PDF file  (decrypted PDF file) | pdf           | pdf                |
| pdf compress    | Compress a PDF file                                              | pdf           | pdf                |
| pdf extract     | Extract pages from a PDF file                                    | pdf           | pdf                |
| pdf merge       | Merge (join) input PDFs into a single PDF file                   | pdf           | pdf                |
| pdf rotate      | Rotate PDF pages (clockwise or anti-clockwise)                   | pdf           | pdf                |
| pdf split       | Split PDF pages into separate PDF files (one per page)           | pdf           | pdf                |
| pdf convert     | Convert each PDF page into an image                              | pdf           | png, jpg           |
| pdf extract-img | Extract images from a PDF file                                   | pdf           | png, jpg, jpx, gif |
| pdf repair      | Repair (lightly) corrupted PDF files                             | pdf           | pdf                |


### Text files (json, yaml, ini, etc)


| Command       | Description                          | Input formats              | Output formats             |
| ------------- | ------------------------------------ | -------------------------- | -------------------------- |
| text check    | Checks if text file has valid format | json, xml, yaml, toml, ini | No output file             |
| text compress | Compress / minify text file formats  | json, xml, yaml, toml, ini | json, xml, yaml, toml, ini |
| text convert  | Convert text file formats            | json, xml, yaml, toml, ini | json, xml, yaml, toml, ini |


### Hash files (sha256, md5, etc)


| Command     | Description                                       | Input formats                                                   | Output formats                                                  |
| ----------- | ------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- |
| hash create | Calculates hashes and creates a hash file         | Any file format (*)                                             | md5, sha1, sha256, sha384, sha512, sha3_256, sha3_384, sha3_512 |
| hash check  | Check if hashes contained in input file are valid | md5, sha1, sha256, sha384, sha512, sha3_256, sha3_384, sha3_512 | No output file                                                  |


### Windows utilities


| Command              | Description                                                   | Input formats  | Output formats  |
| -------------------- | ------------------------------------------------------------- | -------------- | --------------- |
| win install-menu     | Installs app context menu (right click in Windows Explorer)   | No input files | No output files |
| win uninstall-menu   | Uninstalls app context menu (right click in Windows Explorer) | No input files | No output files |
| win restart-explorer | Restarts explorer.exe                                         | No input files | No output files |



### App configuration


| Command     | Description                                       | Input formats  | Output formats  |
| ----------- | ------------------------------------------------- | -------------- | --------------- |
| config show | Show the current configuration of the application | No input files | No output files |
| config set  | Configure the default options for the application | No input files | No output files |



### Processing pipelines 


| Command          | Description                                                                       | Input formats   | Output formats                               |
| ---------------- | --------------------------------------------------------------------------------- | --------------- | -------------------------------------------- |
| pipeline create  | Creates a file processing pipeline (input path => pipeline stages => output path) | No input files  | Pipeline directory                           |
| pipeline execute | Execute file processing pipeline                                                  | Pipeline folder | Output files (inside pipeline output folder) |