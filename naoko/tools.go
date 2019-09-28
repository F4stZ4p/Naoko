package naoko

import "strings"

func tokenizeContent(prefix, content string) []string {
	return strings.Split(strings.TrimLeft(strings.TrimSpace(content), prefix), " ")
}
