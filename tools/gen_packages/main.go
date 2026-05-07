// tools/gen_packages/main.go

package main

import (
	"fmt"
	"os"
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
		switch filename {
		case meta.App.Installer.File:
			meta.App.Installer.Hash = hash
			fmt.Printf("Checksum for installer: %s\n", hash)
		case meta.App.Zip.File:
			meta.App.Zip.Hash = hash
			fmt.Printf("Checksum for zip: %s\n", hash)
		case meta.App.Targz.File:
			meta.App.Targz.Hash = hash
			fmt.Printf("Checksum for targz: %s\n", hash)
		case meta.App.Deb.File:
			meta.App.Deb.Hash = hash
			fmt.Printf("Checksum for deb: %s\n", hash)
		case meta.App.Rpm.File:
			meta.App.Rpm.Hash = hash
			fmt.Printf("Checksum for rpm: %s\n", hash)
		}
		return nil
	})
}

func main() {
	fmt.Println("Generating packaging files ...")

	fmt.Println("    1. Reading metadata ...")
	meta, err := utils.LoadMetadata()
	handleError(err)

	fmt.Println("    2. Parsing checksums.txt ...")
	checksum_file := filepath.Join(
		meta.App.Packaging.Dir,
		meta.App.Checksum.File,
	)
	if _, err := os.Stat(checksum_file); err == nil {
		err = ReadChecksums(meta, checksum_file)
		handleError(err)
	} else {
		fmt.Printf("[SKIP] checksum parsing ... Checksum file '%s' not found\n", checksum_file)
	}

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
