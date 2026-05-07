// tools/gen_packages/utils/metadata.go

package utils

import (
	"bytes"
	"fmt"
	"html/template"
	"os"
	"os/exec"
	"reflect"
	"runtime"
	"strings"

	"gopkg.in/yaml.v3"
)

// METADATA FILE - project.yml

type Author struct {
	Name  string `yaml:"name"`
	Email string `yaml:"email"`
}

type License struct {
	Spdx string `yaml:"spdx"`
	Url  string `yaml:"url"`
}

type Entrypoints struct {
	Cli string `yaml:"cli"`
	Gui string `yaml:"gui"`
}

type Repository struct {
	Owner string `yaml:"owner"`
	Name  string `yaml:"name"`
	Tag   string `yaml:"tag"`
}

type Urls struct {
	Homepage   string `yaml:"homepage"`
	Repository string `yaml:"repository"`
	Releases   string `yaml:"releases"`
	Blob       string `yaml:"blob"`
	Raw        string `yaml:"raw"`
}

type Icon struct {
	Png string `yaml:"png"`
	Ico string `yaml:"ico"`
	Url string `yaml:"url"`
}

type Source struct {
	Dir string `yaml:"dir"`
}

type Build struct {
	Platform string `yaml:"platform"`
	Arch     string `yaml:"arch"`
	Dir      string `yaml:"dir"`
}

type Packaging struct {
	Fileprefix string `yaml:"fileprefix"`
	Dir        string `yaml:"dir"`
}

type Checksum struct {
	File string `yaml:"file"`
	Url  string `yaml:"url"`
}

type Installer struct {
	File string `yaml:"file"`
	Url  string `yaml:"url"`
	Hash string `yaml:"hash"`
}

type Targz struct {
	File     string   `yaml:"file"`
	Url      string   `yaml:"url"`
	Hash     string   `yaml:"hash"`
	Contents []string `yaml:"contents"`
}

type Zip struct {
	File     string   `yaml:"file"`
	Url      string   `yaml:"url"`
	Hash     string   `yaml:"hash"`
	Contents []string `yaml:"contents"`
}

type Deb struct {
	File string `yaml:"file"`
	Url  string `yaml:"url"`
	Hash string `yaml:"hash"`
}

type Rpm struct {
	File string `yaml:"file"`
	Url  string `yaml:"url"`
	Hash string `yaml:"hash"`
}

type App struct {
	Title       string      `yaml:"title"`
	Name        string      `yaml:"name"`
	Version     string      `yaml:"version"`
	Authors     []Author    `yaml:"authors"`
	License     License     `yaml:"license"`
	Tags        []string    `yaml:"tags"`
	Summary     string      `yaml:"summary"`
	Description string      `yaml:"description"`
	Entrypoints Entrypoints `yaml:"entrypoints"`
	Repository  Repository  `yaml:"repository"`
	Urls        Urls        `yaml:"urls"`
	Icon        Icon        `yaml:"icon"`
	Source      Source      `yaml:"source"`
	Build       Build       `yaml:"build"`
	Packaging   Packaging   `yaml:"packaging"`
	Checksum    Checksum    `yaml:"checksum"`
	Installer   Installer   `yaml:"installer"`
	Targz       Targz       `yaml:"targz"`
	Zip         Zip         `yaml:"zip"`
	Deb         Deb         `yaml:"deb"`
	Rpm         Rpm         `yaml:"rpm"`
}

type Env struct {
	GOOS    string
	GOARCH  string
	VERSION string
	PWD     string
}

type Metadata struct {
	App App `yaml:"app"`
	Env Env `yaml:"env"`
}

type TemplateOption string

const (
	OptionMissingKeyError   TemplateOption = "missingkey=error"
	OptionMissingKeyDefault TemplateOption = "missingkey=default"
)

func renderString(input string, data any, option TemplateOption) (string, error) {
	if option == "" {
		option = OptionMissingKeyError
	}
	tmpl, err := template.New("x").Option(string(option)).Parse(input)
	if err != nil {
		return "", fmt.Errorf("renderString: %w", err)
	}

	var buf bytes.Buffer

	err = tmpl.Execute(&buf, data)
	if err != nil {
		return "", fmt.Errorf("renderString: %w", err)
	}

	return buf.String(), nil
}

func resolveValue(rootValue reflect.Value, data any, option TemplateOption) (bool, error) {
	changed := false

	switch rootValue.Kind() {

	case reflect.String:
		if !rootValue.CanSet() {
			return false, nil
		}

		oldVal := rootValue.String()

		newVal, err := renderString(oldVal, data, option)
		if err != nil {
			return false, fmt.Errorf("resolveValue: %w", err)
		}

		if newVal != oldVal {
			rootValue.SetString(newVal)
			changed = true
		}

	case reflect.Struct:
		for i := 0; i < rootValue.NumField(); i++ {
			c, err := resolveValue(rootValue.Field(i), data, option)
			if err != nil {
				return false, fmt.Errorf("resolveValue: %w", err)
			}
			changed = changed || c
		}

	case reflect.Slice, reflect.Array:
		for i := 0; i < rootValue.Len(); i++ {
			c, err := resolveValue(rootValue.Index(i), data, option)
			if err != nil {
				return false, fmt.Errorf("resolveValue: %w", err)
			}
			changed = changed || c
		}

	case reflect.Pointer:
		if !rootValue.IsNil() {
			return resolveValue(rootValue.Elem(), data, option)
		}
	}

	return changed, nil
}

func getVersion() string {
	var out bytes.Buffer

	cmd := exec.Command("git", "describe", "--tags", "--always")
	cmd.Stdout = &out
	cmd.Stderr = nil

	err := cmd.Run()
	if err != nil {
		return "dev"
	}

	res := strings.TrimSpace(out.String())
	res = strings.TrimPrefix(res, "v")
	return res
}

func getCurrentDir() string {
	dir, err := os.Getwd()
	if err != nil {
		panic(err)
	}
	return dir
}

func (meta *Metadata) injectEnv() {
	GetOrDefault := func(envKey, defaultValue string) string {
		val := os.Getenv(envKey)
		if val != "" {
			return val
		}
		fmt.Printf("Not found 'Env.%s' , using default '%s'\n", envKey, defaultValue)
		return defaultValue
	}

	meta.Env.GOOS = GetOrDefault("GOOS", runtime.GOOS)
	meta.Env.GOARCH = GetOrDefault("GOARCH", runtime.GOARCH)
	meta.Env.VERSION = GetOrDefault("VERSION", getVersion())
	meta.Env.PWD = GetOrDefault("PWD", getCurrentDir())
}

func (meta *Metadata) resolve(maxIter int) error {
	if maxIter <= 0 {
		// default max iter (prevent infinite loop in case of circular references)
		maxIter = 10
	}

	// inject env variables before resolution, so they can be used in templates
	meta.injectEnv()

	for i := 0; i < maxIter; i++ {
		changed, err := resolveValue(reflect.ValueOf(meta).Elem(), meta, OptionMissingKeyError)
		if err != nil {
			return fmt.Errorf("resolve metadata: %w", err)
		}

		if !changed {
			return nil
		}
	}

	return fmt.Errorf("no converge: exceeded %d iterations for metadata resolution", maxIter)
}

func (meta *Metadata) Read(filename string, maxIter int) (err error) {
	data, err := os.ReadFile(filename)
	if err != nil {
		return err
	}

	err = yaml.Unmarshal(data, meta)
	if err != nil {
		return err
	}

	err = meta.resolve(maxIter)
	if err != nil {
		return err
	}
	return nil
}

func LoadMetadata() (*Metadata, error) {
	var meta Metadata
	err := meta.Read("project.yml", -1)
	if err != nil {
		return nil, err
	}
	return &meta, nil
}
