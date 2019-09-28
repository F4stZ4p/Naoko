package main

import (
	"github.com/NaokoDiscordBot/Naoko/naoko"
	"github.com/NaokoDiscordBot/Naoko/config"
	"log"
	"os"
)

var token = os.Getenv("DISCORD_TOKEN")

var owner1 = os.Getenv("owner1")

func main() {

	if token == "" {
		log.Fatalln("DISCORD_TOKEN environment variable is not set")
	}
	
	var conv = &config.Config{
	    Owners: []string{
	        owner1,
	    },
	}
	
	

	bot := naoko.NewNaoko(conf)
	err := bot.Start(token)

	if err != nil {
		log.Fatal(err)
	}
}
