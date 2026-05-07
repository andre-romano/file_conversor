// tools/gen_packages/utils/hashable.go
// Defines a reusable Hashable struct for file and hash information.

package utils

import "fmt"

type Hashable struct {
	File string `yaml:"file"`
	Hash string `yaml:"hash"`
}

func (h *Hashable) SetHashIfMatch(basename string, hash string) {
	if h.File == basename {
		h.Hash = hash
		fmt.Printf("Found hash for %s: \n\t%s\n", h.File, h.Hash)
	}
}
