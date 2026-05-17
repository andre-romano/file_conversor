package main

import (
	"fmt"
	"os"

	"github.com/file-conversor/file_conversor/internal/cli"
)

const appName = "file_conversor"

func main() {
	// Run the application and handle any errors
	if err := cli.Run(appName); err != nil {
		fmt.Printf("Error: %v\n", err)
		os.Exit(1)
	}
}
