// internal/logger/setup.go

package logger

import (
	"fmt"
	"io"
	"log/slog"
)

var log *slog.Logger

func SetupLogger(cfg *Config) io.Closer {
	var file io.Closer
	var err error
	log, file, err = cfg.New()
	if err != nil {
		defer file.Close()
		panic(fmt.Errorf("logger setup: %v\n", err))
	}
	slog.SetDefault(log)
	return file
}

func Debugf(msg string, args ...any) {
	log.Debug(fmt.Sprintf(msg, args...))
}

func Infof(msg string, args ...any) {
	log.Info(fmt.Sprintf(msg, args...))
}

func Warnf(msg string, args ...any) {
	log.Warn(fmt.Sprintf(msg, args...))
}

func Errorf(msg string, args ...any) {
	log.Error(fmt.Sprintf(msg, args...))
}
