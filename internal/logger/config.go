// internal/logger/setup.go

package logger

import (
	"fmt"
	"io"
	"log/slog"
	"os"
)

type Config struct {
	// Terminal
	TerminalLevel  Level
	TerminalFormat Format // pretty | text | json

	// File
	LogFile    string // "" = no file logging
	FileLevel  Level
	FileFormat Format // text | json recommended

	// AddSource adds file:line to every log entry — useful in debug builds
	AddSource bool
}

func (cfg *Config) New() (*slog.Logger, io.Closer, error) {
	var handlers []slog.Handler

	// --- Terminal handler ---
	termHandler := cfg.newHandler(os.Stderr, cfg.TerminalFormat, cfg.TerminalLevel)
	handlers = append(handlers, termHandler)

	// --- File handler ---
	var fileCloser io.Closer = io.NopCloser(nil)
	if cfg.LogFile != "" {
		f, err := os.OpenFile(
			cfg.LogFile,
			os.O_CREATE|os.O_APPEND|os.O_WRONLY,
			0o644,
		)
		if err != nil {
			return nil, nil, fmt.Errorf("open log file: %w", err)
		}
		fileCloser = f

		// Files almost always want JSON or text, never pretty
		fileFmt := cfg.FileFormat
		if fileFmt == PrettyFormat || fileFmt == "" {
			fileFmt = JSONFormat
		}
		fileHandler := cfg.newHandler(f, fileFmt, cfg.FileLevel)
		handlers = append(handlers, fileHandler)
	}

	logger := slog.New(NewFanoutHandler(handlers...))
	return logger, fileCloser, nil
}

func (cfg *Config) newHandler(out io.Writer, format Format, level Level) slog.Handler {
	opts := slog.HandlerOptions{
		Level:     level.Get(),
		AddSource: cfg.AddSource,
	}
	return format.GetHandler(out, opts)
}
