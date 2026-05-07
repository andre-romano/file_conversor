// tools/build_packages/utils/file.go
// Common file handling utilities for package building.

package utils

import (
	"io"
	"os"
)

func CopyFile(src, dst string, mode os.FileMode) error {
	fSrc, err := os.Open(src)
	if err != nil {
		return err
	}
	defer fSrc.Close()

	fDst, err := os.Create(dst)
	if err != nil {
		return err
	}
	defer fDst.Close()
	_, err = io.Copy(fDst, fSrc)
	fDst.Sync()
	fDst.Chmod(mode)
	return err
}
