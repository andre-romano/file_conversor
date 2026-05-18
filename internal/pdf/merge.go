// internal/pdf/merge.go

package pdf

import (
	"fmt"

	"github.com/pdfcpu/pdfcpu/pkg/api"
)

// Merge merges multiple PDF files into a single PDF file.
func Merge(output string, inputs []string, append bool) error {
	if len(inputs) < 1 {
		return fmt.Errorf("pdf merge: requires at least one input file")
	}
	if output == "" {
		return fmt.Errorf("pdf merge: output file is required")
	}
	if append {
		return api.MergeAppendFile(inputs, output, false, nil)
	}
	return api.MergeCreateFile(inputs, output, false, nil)
}
