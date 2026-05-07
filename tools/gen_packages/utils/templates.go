// tools/gen_packages/utils/templates.go

package utils

import (
	"bytes"
	"encoding/xml"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"text/template"
)

type TemplateFuncMap template.FuncMap

type Template struct {
	Data      any
	InputDir  string
	OutputDir string
	FuncMaps  TemplateFuncMap
}

func WinPath(p string) string {
	return strings.ReplaceAll(filepath.ToSlash(p), "/", "\\")
}

func EscapeXml(s string) string {
	var buf bytes.Buffer
	xml.EscapeText(&buf, []byte(s))
	return buf.String()
}

func (t *Template) ParseTemplate(inputFile string) error {
	// get relative path to template file
	inputFileRel, err := filepath.Rel(t.InputDir, inputFile)
	if err != nil {
		return fmt.Errorf("relative path error '%s': %w", inputFile, err)
	}

	// Remove .tmpl suffix from output path
	outPath := filepath.Join(t.OutputDir, inputFileRel)
	outPath = strings.TrimSuffix(outPath, ".tmpl")

	// create output directory if it doesn't exist
	err = os.MkdirAll(filepath.Dir(outPath), 0755)
	if err != nil {
		return err
	}

	// create output file
	dst, err := os.Create(outPath)
	if err != nil {
		return fmt.Errorf("create output %s: %w", outPath, err)
	}
	defer dst.Close()

	// copy file without parsing template
	if !strings.HasSuffix(inputFile, ".tmpl") {
		src, err := os.Open(inputFile)
		if err != nil {
			return fmt.Errorf("open source file %s: %w", inputFile, err)
		}
		defer src.Close()

		_, err = io.Copy(dst, src)
		if err != nil {
			return fmt.Errorf("copy file %s -> %s: %w", inputFile, outPath, err)
		}
		return nil
	}

	// parse template file
	tmpl, err := template.
		New(filepath.Base(inputFile)).
		Funcs(template.FuncMap(t.FuncMaps)).
		ParseFiles(inputFile)
	if err != nil {
		return fmt.Errorf("parse template %s: %w", inputFile, err)
	}

	// execute template with metadata
	err = tmpl.Execute(dst, t.Data)
	if err != nil {
		return fmt.Errorf("execute template %s: %w", inputFile, err)
	}

	return nil
}

func (t *Template) ParseTemplates() error {
	return filepath.Walk(t.InputDir, func(path string, info os.FileInfo, walkErr error) error {
		// handle walk error
		if walkErr != nil {
			return walkErr
		}

		// skip directories
		if info.IsDir() {
			return nil
		}

		return t.ParseTemplate(path)
	})
}
