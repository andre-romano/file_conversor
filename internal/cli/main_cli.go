// internal/cli/main.go

package cli

import (
	"fmt"
	"io"

	"github.com/alecthomas/kong"
	"github.com/file-conversor/file_conversor/internal/env"
	"github.com/file-conversor/file_conversor/internal/logger"
)

type MainCLI struct {
	// Args:
	Pdf PdfCLI `cmd:"" help:"PDF conversion and manipulation commands."`

	// Flags :
	Quiet     bool `short:"q" help:"Quiet output (show errors only)."`
	Verbose   bool `short:"v" help:"Verbose output (show debug information)."`
	Overwrite bool `short:"O" help:"Overwrite output files."`
	Install   bool `short:"I" help:"Install dependencies, if needed (no user prompts)."`
}

func callback(appName string, ctx *MainCLI) (io.Closer, error) {
	// setup logging
	logfile, err := env.Logfile(appName)
	if err != nil {
		return nil, fmt.Errorf("logfile get: %w", err)
	}
	logCfg := logger.DefaultConfig(logfile)
	logMode := "Normal"
	if ctx.Verbose {
		// set verbose logging to terminal
		logMode = "Verbose"
		logCfg.TerminalLevel = logger.DebugLevel
	}
	if ctx.Quiet {
		// set quiet logging to terminal
		logMode = "Quiet"
		logCfg.TerminalLevel = logger.ErrorLevel
	}
	file, err := logger.SetupLogger(logCfg)
	if err != nil {
		return nil, fmt.Errorf("logger setup: %w", err)
	}
	logger.Debugf("Log mode: %s\n", logMode)
	return file, nil
}

// Run executes the main CLI logic.
func Run(appName string) error {
	var cli MainCLI
	ctx := kong.Parse(&cli,
		kong.Name(appName),
		kong.Description("Multi-format cross-platform file conversion and manipulation tool."),
		kong.UsageOnError(),
	)
	file, err := callback(appName, &cli)
	if err != nil {
		return fmt.Errorf("callback: %w", err)
	}
	if file != nil {
		defer file.Close()
	}
	return ctx.Run(&cli)
}
