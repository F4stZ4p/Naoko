package naoko

import (
	"errors"
	"github.com/bwmarrin/discordgo"
	"os"
	"os/signal"
	"syscall"
)

var naoko *Naoko

// Naoko holds global stuff
type Naoko struct {
	commands []Command
	session  *discordgo.Session
	exitc    chan os.Signal
	prefix   string
}

// Start is used to connect Naoko to Discord
func (n *Naoko) Start(token string) (err error) {

	n.session, err = discordgo.New("Bot " + token)

	if err != nil {
		return errors.New("error creating session: " + err.Error())
	}

	naoko = n

	// Registering handlers
	n.session.AddHandler(messageCreateHandler)
	n.session.AddHandler(onReady)

	// Connecting session to Discord
	err = n.session.Open()

	if err != nil {
		return errors.New("error opening connection: " + err.Error())
	}

	defer n.session.Close()

	signal.Notify(n.exitc, syscall.SIGINT, syscall.SIGTERM, os.Interrupt, os.Kill)
	<-n.exitc

	return nil
}

// NewNaoko returns Naoko struct
func NewNaoko() *Naoko {
	return &Naoko{
		exitc:    make(chan os.Signal, 1),
		prefix:   "n.",
		commands: startupCommands,
	}

}
