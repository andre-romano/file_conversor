// internal/env/dirs.go

package env

import (
	"fmt"
	"os"
	"path/filepath"
)

var dirs *Dirs

type Dirs struct {
	appName string
}

// SetupDirs initializes the Dirs struct with the application name. This should be called before using any of the directory functions.
func SetupDirs(appName string) {
	dirs = &Dirs{appName: appName}
}

// Config — user settings, ini/yaml/toml files
// Windows:  %APPDATA%\AppName
// macOS:    ~/Library/Application Support/AppName
// Linux:    $XDG_CONFIG_HOME/AppName  (~/.config/AppName)
func Config() (string, error) {
	base, err := os.UserConfigDir()
	if err != nil {
		return "", fmt.Errorf("config dir: %w", err)
	}
	return dirs.mkdirAll(base)
}

// Cache — expendable data, can be deleted safely
// Windows:  %LOCALAPPDATA%\AppName\Cache
// macOS:    ~/Library/Caches/AppName
// Linux:    $XDG_CACHE_HOME/AppName  (~/.cache/AppName)
func Cache() (string, error) {
	base, err := os.UserCacheDir()
	if err != nil {
		return "", fmt.Errorf("cache dir: %w", err)
	}
	return dirs.mkdirAll(base)
}

// Logs — application logs
func Logs() (string, error) {
	return Cache()
}

// Temp — ephemeral files, cleared on reboot
// All OSes: os.TempDir()/AppName
func Temp() (string, error) {
	return dirs.mkdirAll(os.TempDir())
}

// Logfile returns the path to the log file for the application.
func Logfile(appName string) (string, error) {
	logDir, err := Logs()
	if err != nil {
		return "", fmt.Errorf("log folder: %w", err)
	}
	return filepath.Join(logDir, appName+".log"), nil
}

// --- internal ---
func (a *Dirs) mkdirAll(base string) (string, error) {
	return a.ensure(filepath.Join(base, a.appName))
}

func (a *Dirs) ensure(dir string) (string, error) {
	if err := os.MkdirAll(dir, 0o755); err != nil {
		return "", fmt.Errorf("mkdir %s: %w", dir, err)
	}
	return dir, nil
}
