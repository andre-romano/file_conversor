// tools/build_packages/utils/linux.go
// Linux-specific package building logic.

package utils

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"

	gen_utils "github.com/file-conversor/file_conversor/tools/gen_packages/utils"
)

func buildNfpmPackages(outputFile string) error {
	cmd := exec.Command(
		"nfpm", "package",
		"--config", "build/nfpm/nfpm.yaml",
		"--target", outputFile,
		"--packager", filepath.Ext(outputFile)[1:], // get the extension without dot
	)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	return cmd.Run()
}

func BuildLinuxPackages(meta *gen_utils.Metadata) error {
	// create targz package
	pkg := NewPackage(meta, meta.App.Targz.File, meta.App.Targz.Contents, CreateTarGzFile)
	if err := pkg.Build(); err != nil {
		return fmt.Errorf("failed to build tar.gz package: %w", err)
	}
	// create deb
	outputFile := filepath.Join(meta.App.Packaging.Dir, meta.App.Deb.File)
	if err := buildNfpmPackages(outputFile); err != nil {
		return fmt.Errorf("failed to build deb package: %w", err)
	}
	// create rpm
	outputFile = filepath.Join(meta.App.Packaging.Dir, meta.App.Rpm.File)
	if err := buildNfpmPackages(outputFile); err != nil {
		return fmt.Errorf("failed to build rpm package: %w", err)
	}
	return nil
}
