find ~/Obsidian/Synced\ Vault/ -type f -and -name '*.md' -and -not -path '/Users/danthompson/Obsidian/Synced Vault/.obsidian' -and -not -path '*.trash*' -and -not -path '*.history*' -and -not -path '*Apple Notes*' -and -not -path '*Readwise*' -and -not -path '*Roam/*' -and -not -path '*.obsidian*' -print0  | xargs -0 cat | wc -w | awk '{printf "%s",$1}'