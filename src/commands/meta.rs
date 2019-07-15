use serenity::{
    framework::standard::CommandResult,
    framework::standard::macros::command,
    model::prelude::*,
    prelude::*,
    utils::Colour,
};

use std::{
    time::Instant,
};

#[command]
#[description = "Want to know my latency?"]

fn ping(ctx: &mut Context, msg: &Message) -> CommandResult {

    let t = Instant::now();

    let mut msg = msg.channel_id.say(&ctx, ":ping_pong: | Pinging...")?;
    let f = t.elapsed();

    msg.edit(&ctx, |msgs| {
        msgs.content(&format!(
            ":ping_pong: | Pong! It took **{}**ms",
            f.as_millis()
        ))
    })?;

    Ok(())
}

#[command]
#[description = "Some stats about the bot"]

fn about(ctx: &mut Context, msg: &Message) -> CommandResult {


    let name = msg.author.name.clone();
    let avatar = msg.author.face();
    
    let t = Instant::now();

    let mut msg = msg.channel_id.say(
        &ctx,
        "<a:loading:600340020397735942> | Fetching latest data..."
    )?;

    let f = t.elapsed();

    msg.edit(&ctx, |m| {

        m.content(
            ""
        );
        
        m.embed(|embed| {
            
            embed.title(
                ":bar_chart: Naoko Statistics"
            );

            embed.colour(
                Colour::new(
                    0xA575FF
                )
            );

            embed.author(|mut author| {
                author = author.name(name);
                author = author.icon_url(avatar);
                author
            });
            
            embed.fields(
                vec![
                    (
                        ":ping_pong: **Latency**", 
                        format!(
                            "**{}** ms", 
                            f.as_millis()
                        ), 
                        true,
                    ),

                    (
                        "<:ferris:600338761624059923> **Powered by**",
                        "**Rust** and **Serenity**".to_string(),
                        true,
                    )
                ]
            )
        
        })

    })?;

    Ok(())

}