package naoko

import "github.com/bwmarrin/discordgo"

type pingCommand struct{}

func (pingCommand) Usage() string {
	return "Just pings the bot"
}

func (pingCommand) Help() string {
	return "n.ping"
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

func (p *pingCommand) Run(session *discordgo.Session, message *discordgo.Message) error {
	_, err := session.ChannelMessageSend(message.ChannelID, ":ping_pong: | **Pong!**")
	return err
}
