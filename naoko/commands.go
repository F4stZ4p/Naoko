package naoko

import "github.com/bwmarrin/discordgo"

// Command represents a single command
type Command interface {

	// Both are formatters that returns complete usage with prefix, data, etc
	Usage(prefix string) string // Quick description
	Help() string               // Full description

	// First alias is the main
	Aliases() []string

	// If it is true, the command available only for Naoko's owners
	OwnerOnly() bool

	// We do not know what event action will react to
	Run(session *discordgo.Session, message *discordgo.Message) error

	// Categories []*Category
}

var commands = []Command{
	&pingCommand{},
	&helpCommand{},
	&testOwnerCommand{},
}
