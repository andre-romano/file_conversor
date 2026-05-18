// internal/env/dirs.go

package env

import (
	"fmt"
	"os"
	"path/filepath"
)

// Config — user settings, ini/yaml/toml files
// Windows:  %APPDATA%\AppName
// macOS:    ~/Library/Application Support/AppName
// Linux:    $XDG_CONFIG_HOME/AppName  (~/.config/AppName)
func Config(appName string) (string, error) {
	base, err := os.UserConfigDir()
	if err != nil {
		return "", fmt.Errorf("config dir: %w", err)
	}
	return mkdirAll(base, appName)
}

// Cache — expendable data, can be deleted safely
// Windows:  %LOCALAPPDATA%\AppName\Cache
// macOS:    ~/Library/Caches/AppName
// Linux:    $XDG_CACHE_HOME/AppName  (~/.cache/AppName)
func Cache(appName string) (string, error) {
	base, err := os.UserCacheDir()
	if err != nil {
		return "", fmt.Errorf("cache dir: %w", err)
	}
	return mkdirAll(base, appName)
}

// Logs — application logs
func Logs(appName string) (string, error) {
	return Cache(appName)
}

// Temp — ephemeral files, cleared on reboot
// All OSes: os.TempDir()/AppName
func Temp(appName string) (string, error) {
	return mkdirAll(os.TempDir(), appName)
}

// Logfile returns the path to the log file for the application.
func Logfile(appName string) (string, error) {
	logDir, err := Logs(appName)
	if err != nil {
		return "", fmt.Errorf("log folder: %w", err)
	}
	return filepath.Join(logDir, appName+".log"), nil
}

// --- internal ---
func mkdirAll(base string, appName string) (string, error) {
	dir := filepath.Join(base, appName)
	if err := os.MkdirAll(dir, 0o755); err != nil {
		return "", fmt.Errorf("mkdir %s: %w", dir, err)
	}
	return dir, nil
}
