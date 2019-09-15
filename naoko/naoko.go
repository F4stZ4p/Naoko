package naoko

import (
	"github.com/bwmarrin/discordgo"
)

type Naoko struct {
	session *discordgo.Session
	exitc   chan int
}

func (n *Naoko) Start(token string) (err error) {
	// Creating new discord Session
	n.session, err = discordgo.New("Bot " + token)
	if err != nil {
		return err
	}

	// Registering handlers
	n.session.AddHandler(messageCreateHandler)

	n.exitc = make(chan int, 1)
	// Opening session
	err = n.session.Open()
	if err != nil {
		return err
	}
	defer n.session.Close()

	// waiting for exit signal
	<-n.exitc

	return nil
}

func NewBot() *Naoko {
	return &Naoko{}
}

func messageCreateHandler(s *discordgo.Session, m *discordgo.MessageCreate) {
	if m.Content == "ping" {
		s.ChannelMessageSend(m.ChannelID, "pong")
	}
}
