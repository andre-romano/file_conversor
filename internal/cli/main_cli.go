// internal/cli/main.go

package cli

import (
	"fmt"
	"io"
	"path/filepath"

	"github.com/file-conversor/file_conversor/internal/env"
	"github.com/file-conversor/file_conversor/internal/logger"
)

type MainCLI struct {
}

// Run executes the main CLI logic.
func Run(appName string) error {
	file, err := setupLogger(appName)
	if err != nil {
		return fmt.Errorf("setup logger: %w", err)
	}
	defer file.Close()

	logger.Infof("Running %s CLI...\n", appName)
	return nil
}

// setupLogger initializes the logger with a file in the logs directory.
// Prints the log file path to the console for debugging purposes.
func setupLogger(appName string) (io.Closer, error) {
	env.SetupDirs(appName)
	logDir, err := env.Logs()
	if err != nil {
		return nil, fmt.Errorf("log folder: %w", err)
	}
	logfile := filepath.Join(logDir, appName+".log")
	file, err := logger.SetupLogger(logger.DefaultConfig(logfile))
	if err != nil {
		return nil, fmt.Errorf("logger setup: %w", err)
	}
	fmt.Printf("Logfile: %s\n", logfile)
	return file, nil
}
