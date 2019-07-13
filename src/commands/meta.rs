use serenity::prelude::*;
use serenity::model::prelude::*;
use serenity::framework::standard::{
    CommandResult,
    macros::command,
};

use std::time::{
    Instant,
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