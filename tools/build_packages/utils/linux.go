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

func buildNfpmPackages(meta *gen_utils.Metadata, outputFile string) error {
	// nfpm package
	cmd := exec.Command(
		"nfpm", "package",
		"--config", "build/nfpm/nfpm.yaml",
		"--target", outputFile,
		"--packager", filepath.Ext(outputFile)[1:],
	)
	cmd.Stdout, cmd.Stderr = os.Stdout, os.Stderr
	if err := cmd.Run(); err != nil {
		return fmt.Errorf("run nfpm: %w", err)
	}
	return nil
}

func BuildLinuxPackages(meta *gen_utils.Metadata) error {
	// create targz package
	pkg := NewPackage(meta, meta.App.Targz.File, meta.App.Targz.Contents, CreateTarGzFile)
	if err := pkg.Build(); err != nil {
		return fmt.Errorf("build tar.gz package: %w", err)
	}
	// create deb
	outputFile := filepath.Join(meta.App.Packaging.Dir, meta.App.Deb.File)
	if err := buildNfpmPackages(meta, outputFile); err != nil {
		return fmt.Errorf("build deb package: %w", err)
	}
	// create rpm
	outputFile = filepath.Join(meta.App.Packaging.Dir, meta.App.Rpm.File)
	if err := buildNfpmPackages(meta, outputFile); err != nil {
		return fmt.Errorf("build rpm package: %w", err)
	}
	return nil
}
