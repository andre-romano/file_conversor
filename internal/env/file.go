// internal/env/file.go

package env

import (
	"errors"
	"os"
	"path/filepath"
	"runtime"
	"strings"
)

func EnsureParentDirExists(path string) error {
	dir := Dirname(path)
	if err := os.MkdirAll(dir, os.ModePerm); err != nil {
		return err
	}
	return nil
}

func Dirname(path string) string {
	return filepath.Dir(path)
}

func BaseName(path string) string {
	return filepath.Base(path)
}

func FileStem(path string) string {
	return filepath.Base(path[:len(path)-len(filepath.Ext(path))])
}

func FileExt(path string) string {
	return filepath.Ext(path)
}

func FileExists(path string) bool {
	info, err := os.Stat(path)
	if err != nil {
		return false
	}
	return !info.IsDir()
}

func DirExists(path string) bool {
	info, err := os.Stat(path)
	if err != nil {
		return false
	}
	return info.IsDir()
}

func IsEqualPath(path1, path2 string) (bool, error) {
	abs1, err1 := filepath.Abs(path1)
	abs2, err2 := filepath.Abs(path2)
	if err1 != nil || err2 != nil {
		return false, errors.Join(err1, err2)
	}
	if runtime.GOOS == "windows" {
		return strings.EqualFold(abs1, abs2), nil
	}
	return abs1 == abs2, nil
}

func IsFileExt(path string, ext ...string) bool {
	fileExt := FileExt(path)
	for _, e := range ext {
		if strings.EqualFold(fileExt, e) {
			return true
		}
	}
	return false
}
