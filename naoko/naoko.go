package naoko

import (
	"errors"
	"github.com/bwmarrin/discordgo"
	"os"
	"os/signal"
	"syscall"
)

// Naoko holds global stuff
type Naoko struct {
	session *discordgo.Session
	exitc   chan os.Signal
}

// Start is used to connect Naoko to Discord
func (n *Naoko) Start(token string) (err error) {
	n.session, err = discordgo.New("Bot " + token)
	if err != nil {
		return errors.New("error creating Discord session: " + err.Error())
	}

	// Registering handlers
	n.session.AddHandler(messageCreateHandler)

	// Connecting session to Discord
	err = n.session.Open()
	if err != nil {
		return errors.New("error opening connection: " + err.Error())
	}
	defer n.session.Close()

	// waiting for exit signal
	signal.Notify(n.exitc, syscall.SIGINT, syscall.SIGTERM, os.Interrupt, os.Kill)
	<-n.exitc

	return nil
}

// NewNaoko returns Naoko struct
func NewNaoko() *Naoko {
	return &Naoko{
		exitc: make(chan os.Signal, 1),
	}

}

func messageCreateHandler(s *discordgo.Session, m *discordgo.MessageCreate) {
	if m.Content == "ping" {
		s.ChannelMessageSend(m.ChannelID, "pong")
	}

}
