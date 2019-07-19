mod commands;
mod utils;

use std::{
    collections::HashSet,
    sync::Arc,
    fs,
};

use serenity::{
    framework::{
        StandardFramework,
        standard::macros::group,
    },
    prelude::*,
    model::{
        event::ResumedEvent, 
        gateway::Ready, 
        gateway::Activity, 
        user::OnlineStatus
    },
};

use log::{
    error, 
    info,
};

use commands::{
    meta::*,
};

use utils::{
    keys::*,
};

struct Handler;

impl EventHandler for Handler {

    fn ready(&self, context: Context, ready: Ready) {

        let activity = Activity::streaming(
            &"https://naoko-butt-is-me.ga | Rust Rewrite", "https://twitch.tv/404"
        );
        
        context.set_presence(
            Some(
                activity
            ), 
            OnlineStatus::DoNotDisturb
        );

        info!(
            "[INFO] Ready. Logged as in {}", 
            ready.user.name
        );

    }

    fn resume(&self, _context: Context, _: ResumedEvent) {

        info!(
            "[INFO] Resumed"
        );

    }
}

group!({
    name: "general",
    options: {},
    commands: [ping, about]
});

fn main() {

    let real_token = fs::read_to_string("config.ini").expect(
        "[ERROR] Failed to obtain token"
    );

    let mut client = Client::new(&real_token, Handler).expect(
        "[ERROR] Failed creating client"
    );

    {
        let mut data = client.data.write();

        data.insert::<ShardManagerContainer>(
            Arc::clone(
                &client.shard_manager
            )
        );

    }

    let owners = match client.cache_and_http.http.get_current_application_info() {
        Ok(info) => {
            let mut set = HashSet::new();
            set.insert(
                info.owner.id
            );

            set
        },

        Err(
            why
        ) => panic!(
            "Couldn't get application info: {:?}", 
            why
        ),
    };

    client.with_framework(StandardFramework::new()
        .configure(|c| c
            .owners(owners)
            .prefix("n."))
        .group(&GENERAL_GROUP));

    if let Err(why) = client.start() {
        error!(
            "[ERROR] Client error: {:?}", 
            why
        );
    }
}
