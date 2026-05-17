package main

import (
	"fmt"

	"github.com/file-conversor/file_conversor/internal/deps"
)

func main() {
	cmd, err := deps.FFmpegDep.EnsureInstalled(false, false)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}
	fmt.Printf("Path: %s\n", cmd)
}
