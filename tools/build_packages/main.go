// tools/build_packages/main.go
// Build packages for different platforms (zip, tar.gz, rpm, deb, etc.).

package main

import (
	"fmt"
	"strings"

	"github.com/file-conversor/file_conversor/tools/build_packages/utils"
	gen_utils "github.com/file-conversor/file_conversor/tools/gen_packages/utils"
)

func handleError(err error) {
	if err != nil {
		panic(err)
	}
}

func main() {
	var err error
	fmt.Println("Building packages ...")

	fmt.Println("   1. Reading metadata ...")
	meta, err := gen_utils.LoadMetadata()
	handleError(err)

	fmt.Println("   2. Detecting system ...")
	system := utils.NewSystem()
	fmt.Println("Detected system:", system)

	// Build packages for the detected system.
	fmt.Printf("   3. Building packages for %s ...\n", strings.ToUpper(system.OS))
	err = system.BuildPackages(meta)
	handleError(err)

	fmt.Println("Package building ... Done!")
}
