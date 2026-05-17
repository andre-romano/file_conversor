// internal/deps/pkg_manager.go

package deps

import (
	"fmt"
	"os"
	"os/exec"
	"runtime"
	"strings"
	"sync"
	"time"
)

// defines an interface for pkg mgrs that can be used to install dependencies.
type pkgMgr struct {
	Name              string
	AvailableInOS     map[string]struct{}
	InstallPkgMgrFunc func(dry_run bool) error
	UpdateCmd         []string
	InstallCmd        []string
	lastUpdated       time.Time
	lock              sync.Mutex
}

// isAvailable checks if the pkg mgr is available on the system.
func (p *pkgMgr) IsAvailable() error {
	if p.Name == "" {
		return fmt.Errorf("pkg mgr name is not defined")
	}
	if _, err := exec.LookPath(p.Name); err != nil {
		return fmt.Errorf("pkg mgr '%s' not found in PATH: %w", p.Name, err)
	}
	return nil
}

func (p *pkgMgr) IsAvailableForCurrOS() error {
	if _, exists := p.AvailableInOS[runtime.GOOS]; !exists {
		return fmt.Errorf("pkg mgr '%s' not available on '%s' OS", p.Name, runtime.GOOS)
	}
	return nil
}

// installPkgManager installs the pkg mgr if it is not already available on the system.
func (p *pkgMgr) installPkgManager(dry_run bool) error {
	if err := p.IsAvailableForCurrOS(); err != nil {
		return err
	}
	if p.InstallPkgMgrFunc == nil {
		return fmt.Errorf("pkg mgr '%s' is not installable on this system", p.Name)
	}
	if err := p.InstallPkgMgrFunc(dry_run); err != nil {
		return fmt.Errorf("install pkg mgr '%s': %w", p.Name, err)
	}
	return nil
}

// update pkg mgr's package metadata
func (p *pkgMgr) update(dry_run bool) error {
	if len(p.UpdateCmd) == 0 {
		return nil
	}
	if dry_run {
		fmt.Printf("  $ %s\n", strings.Join(p.UpdateCmd, " "))
		return nil
	}
	if time.Since(p.lastUpdated) < 24*time.Hour {
		fmt.Printf("[SKIP] Skipping update: pkg mgr '%s' was updated less than 24 hours ago ...\n", p.Name)
		return nil
	}
	cmd := exec.Command(p.UpdateCmd[0], p.UpdateCmd[1:]...)
	cmd.Stdout, cmd.Stderr = os.Stdout, os.Stderr
	if err := cmd.Run(); err != nil {
		return fmt.Errorf("update pkg mgr '%s': %w", p.Name, err)
	}
	p.lastUpdated = time.Now()
	return nil
}

// install installs the specified package using the pkg mgr.
func (p *pkgMgr) install(pkgName string, dry_run bool) error {
	if len(p.InstallCmd) == 0 {
		return fmt.Errorf("install command not defined for pkg mgr '%s'", p.Name)
	}
	if dry_run {
		fmt.Printf("  $ %s %s\n", strings.Join(p.InstallCmd, " "), pkgName)
		return nil
	}
	cmd := exec.Command(
		p.InstallCmd[0],
		append(p.InstallCmd[1:], pkgName)...,
	)
	cmd.Stdout, cmd.Stderr = os.Stdout, os.Stderr
	if err := cmd.Run(); err != nil {
		return fmt.Errorf("install pkg '%s' using '%s': %w", pkgName, p.Name, err)
	}
	return nil
}

func (p *pkgMgr) InstallAll(dry_run bool, pkgName ...string) error {
	// Lock to ensure that only one goroutine can attempt issuing pkg mgr
	// commands at a time, preventing potential race conditions.
	p.lock.Lock()
	defer p.lock.Unlock()

	// check pkg mgr availability and install if not available
	if err := p.IsAvailable(); err != nil {
		if err := p.installPkgManager(dry_run); err != nil {
			return err
		}
	}

	// update pkg mgr metadata
	if err := p.update(dry_run); err != nil {
		return err
	}

	// install packages
	for _, pkg := range pkgName {
		if err := p.install(pkg, dry_run); err != nil {
			return err
		}
	}
	return nil
}

// Linux pkg mgr is not provided, as it can vary widely between distributions.
// Further, pkg name mappings can also vary widely, so we will not attempt to provide a universal pkg mgr for Linux.
// The user will need to install dependencies manually on Linux.

// Brew pkg mgr for macOS
var BrewPkgMgr = &pkgMgr{
	Name: "brew",
	AvailableInOS: map[string]struct{}{
		"darwin": {},
	},
	InstallPkgMgrFunc: nil, // Homebrew installation is more complex and typically requires user interaction, so we won't implement it here.
	UpdateCmd:         []string{"brew", "update"},
	InstallCmd:        []string{"brew", "install"},
}

// Scoop pkg mgr for Windows
var ScoopPkgMgr = &pkgMgr{
	Name: "scoop",
	AvailableInOS: map[string]struct{}{
		"windows": {},
	},
	InstallPkgMgrFunc: func(dry_run bool) error {
		cmdSlice := []string{"powershell", "-Command", "iwr -useb get.scoop.sh | iex"}
		if dry_run {
			fmt.Printf("  $ %s\n", strings.Join(cmdSlice, " "))
			return nil
		}
		cmd := exec.Command(cmdSlice[0], cmdSlice[1:]...)
		cmd.Stdout, cmd.Stderr = os.Stdout, os.Stderr
		return cmd.Run()
	},
	UpdateCmd:  []string{"scoop", "update"},
	InstallCmd: []string{"scoop", "install"},
}
