// tools/build_packages/utils/file.go
// Common file handling utilities for package building.

package utils

import (
	"fmt"
	"io"
	"os"
)

func CopyFile(src, dst string, mode os.FileMode) error {
	fSrc, err := os.Open(src)
	if err != nil {
		return fmt.Errorf("failed to open file %s: %w", src, err)
	}
	defer fSrc.Close()

	fDst, err := os.Create(dst)
	if err != nil {
		return fmt.Errorf("failed to create file %s: %w", dst, err)
	}
	defer fDst.Close()

	if _, err := io.Copy(fDst, fSrc); err != nil {
		return fmt.Errorf("failed to copy from %s to %s: %w", src, dst, err)
	}

	if err := fDst.Sync(); err != nil {
		return fmt.Errorf("failed to sync file %s: %w", dst, err)
	}
	if err := fDst.Chmod(mode); err != nil {
		return fmt.Errorf("failed to set permissions for file %s: %w", dst, err)
	}

	return nil
}
