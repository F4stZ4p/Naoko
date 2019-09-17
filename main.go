package main

import (
	"github.com/NaokoDiscordBot/Naoko/naoko"
	"log"
	"os"
)

var token = os.Getenv("DISCORD_TOKEN")

func main() {

	if token == "" {
		log.Fatalln("DISCORD_TOKEN environment variable is not set")
	}

	bot := naoko.NewNaoko()
	err := bot.Start(token)

	if err != nil {
		log.Fatal(err)
	}
}
