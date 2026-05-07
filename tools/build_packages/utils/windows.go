// tools/build_packages/utils/windows.go
// Windows-specific package building logic.

package utils

import (
	"os"
	"os/exec"

	gen_utils "github.com/file-conversor/file_conversor/tools/gen_packages/utils"
)

func buildInnoSetupInstaller() error {
	// build Inno Setup installer
	cmd := exec.Command("iscc.exe", "/Qp", "build\\packaging\\innosetup\\setup.iss")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	return cmd.Run()
}

func BuildWindowsPackages(meta *gen_utils.Metadata) error {
	// create zip package
	zipPackage := NewPackage(meta, meta.App.Zip.File, meta.App.Zip.Contents, CreateZipFile)
	if err := zipPackage.Build(); err != nil {
		return err
	}
	// build Inno Setup installer
	if err := buildInnoSetupInstaller(); err != nil {
		return err
	}
	return nil
}
