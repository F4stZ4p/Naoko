package main

import (
	"./naoko"
	"log"
	"os"
)

var token string = os.Getenv("DISCORD_TOKEN")

func main() {

	bot := naoko.NewBot()
	err := bot.Start(token)

	if err != nil {
		log.Fatal(err)
	}

}
