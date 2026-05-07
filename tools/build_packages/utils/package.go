// tools/build_packages/utils/actions.go
// Common actions for building packages across different platforms.

package utils

import (
	"path/filepath"

	gen_utils "github.com/file-conversor/file_conversor/tools/gen_packages/utils"
)

type Package struct {
	Meta               *gen_utils.Metadata
	OutputFileBasename string
	InputFiles         []string
	CreateFunc         func(output string, inputFiles []string) error
}

func NewPackage(
	meta *gen_utils.Metadata,
	outputFileBasename string,
	inputFiles []string,
	createFunc func(output string, inputFiles []string) error,
) *Package {
	return &Package{
		Meta:               meta,
		OutputFileBasename: outputFileBasename,
		InputFiles:         inputFiles,
		CreateFunc:         createFunc,
	}
}

func (p *Package) Build() error {
	outputFile := filepath.Join(p.Meta.App.Packaging.Dir, p.OutputFileBasename)
	if err := p.CreateFunc(outputFile, p.InputFiles); err != nil {
		return err
	}
	return nil
}
