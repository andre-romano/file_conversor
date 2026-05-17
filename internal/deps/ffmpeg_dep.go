// internal/deps/ffmpeg_dep.go

package deps

var FFmpegDep = &Dependency{
	Name:     "FFmpeg",
	Binary:   "ffmpeg",
	Homepage: "https://ffmpeg.org/",
	License:  GPLv2,
	MapPkgToPkgMgr: map[string]pkgMgrs{
		"ffmpeg": {
			BrewPkgMgr,
			ScoopPkgMgr,
		},
	},
}
