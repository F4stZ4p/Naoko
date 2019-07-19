use serenity::{
    framework::standard::CommandResult,
    framework::standard::macros::command,
    model::prelude::*,
    prelude::*,
    model::user::User,
    utils::Colour,
};

use std::{
    time::Instant,
};


#[command]
#[description = "Want to know my latency?"]

fn ping(ctx: &mut Context, msg: &Message) -> CommandResult {

    let t = Instant::now();

    let mut msg = msg.channel_id.say(
        &ctx, 
        ":ping_pong: | Pinging..."
    )?;
    let f = t.elapsed();

    msg.edit(&ctx, |msgs| {
        msgs.content(
            &format!(
                ":ping_pong: | Pong! It took **{}**ms to respond",
                f.as_millis()
            )
        )
    })?;

    Ok(())
}

#[command]
#[description = "Some stats about the bot"]

fn about(ctx: &mut Context, msg: &Message) -> CommandResult {

    let funsince = User::from(
        &ctx.cache.read().user      
    )
    .created_at();

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

            embed.timestamp(
                &funsince
            );

            embed.colour(
                Colour::new(
                    0xA575FF
                )
            );

            embed.footer(|footer| {
                footer.text(
                    "Bringing fun to Discord since"
                );
                footer.icon_url(
                    "https://i.imgur.com/fYWEGhE.gif"
                )
            });

            embed.author(|author| {
                author.name(name);
                author.icon_url(avatar)
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