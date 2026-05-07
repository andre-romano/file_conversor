// tools/build_packages/utils/system.go
// Utility functions for detecting the system and architecture.

package utils

import (
	"fmt"
	"os"
	"runtime"

	gen_utils "github.com/file-conversor/file_conversor/tools/gen_packages/utils"
)

type System struct {
	OS   string
	Arch string
}

func getOrDefault(envVar, defaultValue string) string {
	value := os.Getenv(envVar)
	if value != "" {
		return value
	}
	return defaultValue
}

func NewSystem() *System {
	s := &System{
		OS:   getOrDefault("GOOS", runtime.GOOS),
		Arch: getOrDefault("GOARCH", runtime.GOARCH),
	}
	return s
}

func (s *System) IsLinux() bool {
	return s.OS == "linux"
}

func (s *System) IsWindows() bool {
	return s.OS == "windows"
}

func (s *System) IsMacOS() bool {
	return s.OS == "darwin"
}

func (s *System) IsAMD64() bool {
	return s.Arch == "amd64"
}

func (s *System) IsArm64() bool {
	return s.Arch == "arm64"
}

func (s *System) BuildPackages(meta *gen_utils.Metadata) error {
	var err error
	if s.IsLinux() {
		err = BuildLinuxPackages(meta)
	} else if s.IsWindows() {
		err = BuildWindowsPackages(meta)
	} else if s.IsMacOS() {
		err = BuildMacOSPackages(meta)
	} else {
		err = fmt.Errorf("Unsupported system: %s", s.OS)
	}
	if err != nil {
		return err
	}
	return nil
}
