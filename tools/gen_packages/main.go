// tools/gen_packages/main.go

package main

import (
	"fmt"
	"path/filepath"
	"strings"

	"github.com/file-conversor/file_conversor/tools/gen_packages/utils"
)

func handleError(err error) {
	if err != nil {
		panic(err)
	}
}

func ReadChecksums(meta *utils.Metadata, checksums string) error {
	return utils.ReadFile(checksums, func(line string) error {
		parts := strings.Fields(line)
		if len(parts) < 2 {
			return fmt.Errorf("invalid checksum line: %s", line)
		}
		hash, filename := parts[0], parts[1]
		filename = strings.TrimPrefix(filename, "*")
		filename = filepath.Base(filename) // get the base name of the file
		// match the file paths in metadata, and set the corresponding hash field
		meta.App.Installer.SetHashIfMatch(filename, hash)
		meta.App.Zip.SetHashIfMatch(filename, hash)
		meta.App.Targz.SetHashIfMatch(filename, hash)
		meta.App.Deb.SetHashIfMatch(filename, hash)
		meta.App.Rpm.SetHashIfMatch(filename, hash)
		return nil
	})
}

func main() {
	fmt.Println("Generating packaging files ...")

	fmt.Println("    1. Reading metadata ...")
	meta, err := utils.LoadMetadata()
	handleError(err)

	fmt.Println("    2. Parsing checksums.txt ...")
	err = ReadChecksums(meta,
		filepath.Join(
			meta.App.Packaging.Dir,
			meta.App.Checksum.File,
		),
	)
	handleError(err)

	fmt.Println("    3. Parsing templates ...")
	template := utils.Template{
		Data:      *meta,
		InputDir:  "packaging",
		OutputDir: "build/packaging",
		FuncMaps: utils.TemplateFuncMap{
			"winpath": utils.WinPath,
			"join":    strings.Join,
			"escape":  utils.EscapeXml,
			"replace": strings.ReplaceAll,
		},
	}
	err = template.ParseTemplates()
	handleError(err)

	fmt.Println("Generating packaging files ... Done.")
}
