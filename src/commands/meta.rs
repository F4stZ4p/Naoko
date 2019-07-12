use serenity::prelude::*;
use serenity::model::prelude::*;
use serenity::framework::standard::{
    CommandResult,
    macros::command,
};

use chrono::Utc;

#[command]
#[description = "Want to know my latency?"]

fn ping(ctx: &mut Context, msg: &Message) -> CommandResult {

    let t = Utc::now();

    let mut msg = msg.channel_id.say(&ctx, ":ping_pong: | Pinging...")?;

    let f = Utc::now();
    let ping = ((f.timestamp() - t.timestamp()) * 1000) 
        + (i64::from(f.timestamp_subsec_millis()) 
        - i64::from(t.timestamp_subsec_millis()));

    msg.edit(&ctx, |msgs| {
        msgs.content(&format!(
            ":ping_pong: | Pong! It took **{}**ms",
            ping
        ))
    })?;

    Ok(())
}