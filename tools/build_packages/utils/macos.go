// tools/build_packages/utils/macos.go
// macOS-specific package building logic.

package utils

import (
	"fmt"

	gen_utils "github.com/file-conversor/file_conversor/tools/gen_packages/utils"
)

func BuildMacOSPackages(meta *gen_utils.Metadata) error {
	// create targz package
	pkg := NewPackage(meta, meta.App.Targz.File, meta.App.Targz.Contents, CreateTarGzFile)
	if err := pkg.Build(); err != nil {
		return fmt.Errorf("failed to build tar.gz package: %w", err)
	}
	return nil
}
