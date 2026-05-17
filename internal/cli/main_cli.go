// internal/cli/main.go

package cli

import (
	"fmt"
	"io"

	"github.com/alecthomas/kong"
	"github.com/file-conversor/file_conversor/internal/env"
	"github.com/file-conversor/file_conversor/internal/logger"
)

type ConvertCmd struct {
	Input   string `arg:"" type:"existingfile" help:"Input file."`
	Output  string `arg:"" optional:""         help:"Output file."`
	Format  string `short:"f"                  help:"Target format."`
	Quality int    `short:"q" default:"90"     help:"Output quality."`
}

func (c *ConvertCmd) Run(ctx *kong.Context) error {
	// TODO: conversion logic here
	return nil
}

type MainCLI struct {
	Convert ConvertCmd `cmd:"" help:"Convert a file."`

	Verbose bool `short:"v" help:"Verbose output."`
	Install bool `short:"i" help:"Install dependencies (no user prompts)."`
}

func callback(appName string, ctx *MainCLI) (io.Closer, error) {
	// setup logging
	logfile, err := env.Logfile(appName)
	if err != nil {
		return nil, fmt.Errorf("logfile get: %w", err)
	}
	logCfg := logger.DefaultConfig(logfile)
	if ctx.Verbose {
		// set verbose logging to terminal
		logCfg.TerminalLevel = logger.DebugLevel
	}
	file, err := logger.SetupLogger(logCfg)
	if err != nil {
		return nil, fmt.Errorf("logger setup: %w", err)
	}
	if ctx.Verbose {
		logger.Infof("Verbose mode: ENABLED\n")
	}
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
