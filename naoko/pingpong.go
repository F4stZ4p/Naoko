package naoko

import "github.com/bwmarrin/discordgo"

type pingpong struct {
}

func (pingpong) Usage() string {
	return "usage"
}

func (pingpong) Help() string {
	return "help"
}

func (pingpong) Aliases() []string {
	return []string{
		"ping",
		"pong",
	}
}

func (pingpong) OwnerOnly() bool {
	return true
}

func (p *pingpong) Run(session *discordgo.Session, message *discordgo.Message) error {
	_, err := session.ChannelMessageSend(message.ChannelID, "pong")
	return err
}
