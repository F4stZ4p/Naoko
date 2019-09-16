package naoko

import "github.com/bwmarrin/discordgo"

// Command represents a single command
type Command struct {
	// Quick descripiton
	Usage string

	// Full description
	Help string

	// First alias is the main
	Aliases []string

	// We do not know what event Func will react to
	action func(message *discordgo.Message) error

	// If it is true, the command available only for Naoko's owners
	OwnerOnly bool

	naoko *Naoko

	// Categories []*Category
}

func (c *Command) Run(session *discordgo.Session, message *discordgo.Message) (err error) {
	return c.action(message)
}
