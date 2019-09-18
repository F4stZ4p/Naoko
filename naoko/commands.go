package naoko

import "github.com/bwmarrin/discordgo"

// Command represents a single command
type Command interface {
	// Quick description
	Usage() string

	// Full description
	Help() string

	// First alias is the main
	Aliases() []string

	// If it is true, the command available only for Naoko's owners
	OwnerOnly() bool

	// We do not know what event action will react to
	Run(session *discordgo.Session, message *discordgo.Message) error

	// Categories []*Category
}

var Commands = []Command{
	&pingCommand{},
}
