package naoko

import (
	"fmt"
	"github.com/bwmarrin/discordgo"
	"log"
	"strings"
)

// messageCreateHandler is called when new message comes
func messageCreateHandler(s *discordgo.Session, m *discordgo.MessageCreate) {

	if m.Author.ID == s.State.User.ID {
		return
	}
    
    // In DM, prefix is not needed
	if m.GuildID != "" && !strings.HasPrefix(m.Content, naoko.prefix) {
		return
	}

	content := strings.TrimLeft(strings.TrimSpace(m.Content), naoko.prefix)

	args := strings.Split(content, " ")

	for _, c := range naoko.commands {
		for _, alias := range c.Aliases() {
			if args[0] == alias {
				err := c.Run(s, m.Message)
				if err != nil {
					log.Println(err)
				}
			}
		}
	}

	return

}

// onReady is called when Naoko connects to Discord
func onReady(s *discordgo.Session, ready *discordgo.Ready) {
	fmt.Println("Naoko is running now")
	fmt.Println(ready.User.String())
	fmt.Println("ID: " + ready.User.ID)
	fmt.Println("\t" + strings.Repeat("-", 30) + "\t")
	return
}
