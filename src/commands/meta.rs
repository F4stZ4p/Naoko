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

    let u = User::from(
        &ctx.cache.read().user      
    );

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
                &u.created_at()
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
                    &u.face()
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
                    ),

                    (
                        ":video_game: **Guilds count**",
                        format!(
                            "**{}** guilds",
                            ctx.cache.read().guilds.len(),
                        ),
                        true,
                    ),

                    (
                        ":tropical_drink: **Users count**",
                        format!(
                            "**{}** users",
                            ctx.cache.read().users.len(),
                        ),
                        true,
                    ),

                    (
                        ":notepad_spiral: **Channel count**",
                        format!(
                            "**{}** channels",
                            ctx.cache.read().channels.len(),
                        ),
                        true,
                    ),

                    (
                        ":key: **Authorization**",
                        format!(
                            "**{}**",
                            u.tag(),
                        ),
                        true,
                    )
                ]
            )
        
        })

    })?;

    Ok(())

}