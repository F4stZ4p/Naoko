package naoko

import (
	"github.com/bwmarrin/discordgo"
	"strings"
)

type helpCommand struct{}

func (hc helpCommand) Usage(prefix string) string {
	return "Usage: " + prefix + hc.Aliases()[0] + " [command]"
}

func (helpCommand) Help() string {
	return `Help shows info about specified command.`
}

func (helpCommand) Aliases() []string {
	return []string{
		"help",
		"h",
	}
}

func (helpCommand) OwnerOnly() bool {
	return false
}

func (hc *helpCommand) Run(session *discordgo.Session, message *discordgo.Message) error {
	var newMessage string

	naoko.Lock()
	args := tokenizeContent(naoko.prefix, message.Content)
	if len(args) < 2 {
		for _, c := range naoko.commands {
			newMessage += c.Usage(naoko.prefix) + "\n" +
				"Aliases: " + strings.Join(c.Aliases(), ", ") + "\n\n"
		}
	} else if len(args) == 2 {
		for _, c := range naoko.commands {
			for _, alias := range c.Aliases() {
				if strings.HasPrefix(strings.TrimLeft(strings.TrimSpace(message.Content), naoko.prefix), alias) {
					newMessage = c.Usage(naoko.prefix) + "\n" +
						c.Help()
				}
			}
		}
	}
	naoko.Unlock()
	_, err := session.ChannelMessageSend(message.ChannelID, newMessage)
	return err
}
