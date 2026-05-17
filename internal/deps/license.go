// internal/deps/license.go

package deps

import "fmt"

// license represents the license information for a dependency.
type license struct {
	LongName  string
	ShortName string
	Version   float64
}

func (l *license) String() string {
	return fmt.Sprintf("%s v%2.1f (%s)", l.LongName, l.Version, l.ShortName)
}

var LGPLv2 = license{
	LongName:  "GNU Lesser General Public License",
	ShortName: "LGPLv2",
	Version:   2.1,
}

var GPLv2 = license{
	LongName:  "GNU General Public License",
	ShortName: "GPLv2",
	Version:   2.0,
}

var GPLv3 = license{
	LongName:  "GNU General Public License",
	ShortName: "GPLv3",
	Version:   3.0,
}

var AGPLv3 = license{
	LongName:  "GNU Affero General Public License",
	ShortName: "AGPLv3",
	Version:   3.0,
}

var BSD2 = license{
	LongName:  "BSD 2-Clause License",
	ShortName: "BSD 2-Clause",
	Version:   1.0,
}

var BSD3 = license{
	LongName:  "BSD 3-Clause License",
	ShortName: "BSD 3-Clause",
	Version:   1.0,
}

var MPL2 = license{
	LongName:  "Mozilla Public License",
	ShortName: "MPL 2.0",
	Version:   2.0,
}

var MIT = license{
	LongName:  "MIT License",
	ShortName: "MIT",
	Version:   1.0,
}

var Apache2 = license{
	LongName:  "Apache License",
	ShortName: "Apache 2.0",
	Version:   2.0,
}
