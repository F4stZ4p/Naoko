package naoko

import "github.com/bwmarrin/discordgo"

// messageCreateHandler is called when new message comes
func messageCreateHandler(s *discordgo.Session, m *discordgo.MessageCreate) {
	if m.Content == "ping" {
		s.ChannelMessageSend(m.ChannelID, "pong")
	}

}
