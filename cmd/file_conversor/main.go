package main

import (
	"github.com/file-conversor/file_conversor/internal/deps"
	"github.com/file-conversor/file_conversor/internal/logger"
)

func main() {
	// Set as default so third-party libs using slog.Info() etc. also use it
	file := logger.SetupLogger(&logger.Config{
		TerminalLevel:  logger.InfoLevel,    // less noise on terminal
		TerminalFormat: logger.PrettyFormat, // human-friendly for terminal

		LogFile:    "file_conversor.log",
		FileLevel:  logger.DebugLevel, // capture everything to disk
		FileFormat: logger.JSONFormat, // structured logs are easier to analyze and query
	})
	defer file.Close()

	cmd, err := deps.FFmpegDep.EnsureInstalled(false, false)
	if err != nil {
		logger.Errorf("Error: %v\n", err)
		return
	}
	logger.Infof("Path: %s\n", cmd)
}
