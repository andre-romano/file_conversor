// internal/logger/logger.go
package logger

import (
	"context"
	"fmt"
	"io"
	"log/slog"
	"time"
)

// PrettyHandler is a human-readable handler with colour and aligned output.
// Wraps slog internals — no external dependencies.
type PrettyHandler struct {
	w      io.Writer
	opts   slog.HandlerOptions
	attrs  []slog.Attr
	groups []string
}

func NewPrettyHandler(w io.Writer, opts *slog.HandlerOptions) *PrettyHandler {
	return &PrettyHandler{w: w, opts: *opts}
}

func (h *PrettyHandler) Enabled(_ context.Context, l slog.Level) bool {
	min := h.opts.Level
	if min == nil {
		min = slog.LevelInfo
	}
	return l >= min.Level()
}

func (h *PrettyHandler) Handle(_ context.Context, r slog.Record) error {
	// level
	lvl := r.Level.String()

	// Timestamp
	ts := r.Time.Format(time.DateTime) // "01/05 15:04:05"

	// Build attr string
	attrs := ""
	fn := func(a slog.Attr) bool {
		attrs += " " + a.Key + " " + a.Value.String()
		return true
	}
	for _, a := range h.attrs {
		fn(a)
	}
	r.Attrs(fn)

	_, err := fmt.Fprintf(h.w, "%s - [%s] - %s%s",
		ts,
		lvl,
		r.Message,
		attrs,
	)
	return err
}

func (h *PrettyHandler) WithAttrs(attrs []slog.Attr) slog.Handler {
	newH := *h
	newH.attrs = append(h.attrs, attrs...)
	return &newH
}

func (h *PrettyHandler) WithGroup(name string) slog.Handler {
	newH := *h
	newH.groups = append(h.groups, name)
	return &newH
}
