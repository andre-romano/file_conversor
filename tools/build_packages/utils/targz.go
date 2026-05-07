// tools/build_packages/utils/zip.go
// Utility functions for creating zip packages.

package utils

import (
	"archive/tar"
	"compress/gzip"
	"fmt"
	"io"
	"os"
)

func addFileToTar(tw *tar.Writer, path string) error {
	f, err := os.Open(path)
	if err != nil {
		return fmt.Errorf("failed to open file %s: %w", path, err)
	}
	defer f.Close()

	info, err := f.Stat()
	if err != nil {
		return fmt.Errorf("failed to get file info for %s: %w", path, err)
	}

	header, err := tar.FileInfoHeader(info, "")
	if err != nil {
		return fmt.Errorf("failed to create tar header for %s: %w", path, err)
	}

	header.Name = info.Name()

	if err := tw.WriteHeader(header); err != nil {
		return fmt.Errorf("failed to write header for %s: %w", path, err)
	}

	_, err = io.Copy(tw, f)
	return fmt.Errorf("failed to copy file %s: %w", path, err)
}

func CreateTarGzFile(outName string, files []string) error {
	out, err := os.Create(outName)
	if err != nil {
		return fmt.Errorf("failed to create tar.gz file %s: %w", outName, err)
	}
	defer out.Close()

	gz := gzip.NewWriter(out)
	defer gz.Close()

	tw := tar.NewWriter(gz)
	defer tw.Close()

	for _, file := range files {
		if err := addFileToTar(tw, file); err != nil {
			return fmt.Errorf("failed to add file %s to tar.gz: %w", file, err)
		}
	}

	return nil
}
