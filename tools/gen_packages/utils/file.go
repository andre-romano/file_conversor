// tools/gen_packages/utils/file.go

package utils

import (
	"bufio"
	"fmt"
	"os"
)

func ReadFile(path string, lineHandler func(string) error) error {
	file, err := os.Open(path)
	if err != nil {
		return err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := scanner.Text()
		if err := lineHandler(line); err != nil {
			return fmt.Errorf("line handler error: %w", err)
		}
	}

	if err := scanner.Err(); err != nil {
		return fmt.Errorf("scanner error: %w", err)
	}
	return nil
}
