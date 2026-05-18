// internal/cli/custom_types.go

package cli

import (
	"fmt"

	"github.com/alecthomas/kong"
)

type Quality int

func (q *Quality) Decode(ctx *kong.DecodeContext) error {
	err := ctx.Scan.PopValueInto("quality", q)
	if err != nil {
		return err
	}

	if *q < 1 || *q > 100 {
		return fmt.Errorf("quality must be 1-100")
	}

	return nil
}
