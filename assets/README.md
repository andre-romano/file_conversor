# assets/ folder

Store static assets here (images, icons, etc). that are used in the application.

Will be embedded into the binary using Go's embed package, allowing for easy access to these resources at runtime without needing to read from the filesystem.