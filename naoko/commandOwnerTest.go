package naoko

import "github.com/bwmarrin/discordgo"

type testOwnerCommand struct{}

func (c testOwnerCommand) Usage(prefix string) string {
	return "Usage: " + prefix + c.Aliases()[0]
}

func (testOwnerCommand) Help() string {
	return ""
}

func (testOwnerCommand) Aliases() []string {
	return []string{
		"ot",
		"to",
	}
}

func (testOwnerCommand) OwnerOnly() bool {
	return true
}

func (pc *testOwnerCommand) Run(session *discordgo.Session, message *discordgo.Message) error {
	_, err := session.ChannelMessageSend(message.ChannelID, "you are owner")
	return err
}

