package naoko

import "github.com/bwmarrin/discordgo"

type PingCommand struct {}

func (PingCommand) Usage() string {
	return "Just pings the bot"
}

func (PingCommand) Help() string {
	return "n.ping"
}

func (PingCommand) Aliases() []string {
	return []string{
		"ping",
		"pong",
	}
}

func (PingCommand) OwnerOnly() bool {
	return false
}

func (p *PingCommand) Run(session *discordgo.Session, message *discordgo.Message) error {
	_, err := session.ChannelMessageSend(message.ChannelID, ":ping_pong: | **Pong!**")
	return err
}
