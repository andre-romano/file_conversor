// tools/build_packages/utils/zip.go
// Utility functions for creating zip packages.

package utils

import (
	"archive/tar"
	"compress/gzip"
	"io"
	"os"
)

func addFileToTar(tw *tar.Writer, path string) error {
	f, err := os.Open(path)
	if err != nil {
		return err
	}
	defer f.Close()

	info, err := f.Stat()
	if err != nil {
		return err
	}

	header, err := tar.FileInfoHeader(info, "")
	if err != nil {
		return err
	}

	header.Name = info.Name()

	if err := tw.WriteHeader(header); err != nil {
		return err
	}

	_, err = io.Copy(tw, f)
	return err
}

func CreateTarGzFile(outName string, files []string) error {
	out, err := os.Create(outName)
	if err != nil {
		return err
	}
	defer out.Close()

	gz := gzip.NewWriter(out)
	defer gz.Close()

	tw := tar.NewWriter(gz)
	defer tw.Close()

	for _, file := range files {
		if err := addFileToTar(tw, file); err != nil {
			return err
		}
	}

	return nil
}
