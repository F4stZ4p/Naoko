package main

import (
	"./naoko"
	"log"
	"os"
)

var token = os.Getenv("DISCORD_TOKEN")

func main() {

	bot := naoko.NewNaoko()
	err := bot.Start(token)

	if err != nil {
		log.Fatal(err)
	}
}
