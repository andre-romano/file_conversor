// tools/build_packages/utils/zip.go
// Utility functions for creating zip packages.

package utils

import (
	"archive/zip"
	"io"
	"os"
)

func addFileToZip(zw *zip.Writer, path string) error {
	f, err := os.Open(path)
	if err != nil {
		return err
	}
	defer f.Close()

	info, err := f.Stat()
	if err != nil {
		return err
	}

	header, err := zip.FileInfoHeader(info)
	if err != nil {
		return err
	}

	header.Name = info.Name()
	header.Method = zip.Deflate

	w, err := zw.CreateHeader(header)
	if err != nil {
		return err
	}

	_, err = io.Copy(w, f)
	return err
}

func CreateZipFile(outName string, files []string) error {
	out, err := os.Create(outName)
	if err != nil {
		return err
	}
	defer out.Close()

	zw := zip.NewWriter(out)
	defer zw.Close()

	for _, file := range files {
		if err := addFileToZip(zw, file); err != nil {
			return err
		}
	}
	return nil
}
