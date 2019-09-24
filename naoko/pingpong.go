package naoko

import "github.com/bwmarrin/discordgo"

type pingCommand struct{}

func (pc pingCommand) Usage(prefix string) string {
	return "Usage: " + prefix + pc.Aliases()[0]
}

func (pingCommand) Help() string {
	return "Just pings the bot"
}

func (pingCommand) Aliases() []string {
	return []string{
		"ping",
		"pong",
	}
}

func (pingCommand) OwnerOnly() bool {
	return false
}

func (pc *pingCommand) Run(session *discordgo.Session, message *discordgo.Message) error {
	_, err := session.ChannelMessageSend(message.ChannelID, ":ping_pong: | **Pong!**")
	return err
}
