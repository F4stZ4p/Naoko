use typemap::{
    Key,
};

use std::{
    sync::Arc,
};

use serenity::{
    client::bridge::gateway::ShardManager,
    prelude::{
        Mutex,
        TypeMapKey,
    },
};

use reqwest;

pub struct ReqwestClient;
pub struct ShardManagerContainer;

impl Key for ReqwestClient {
    type Value = Arc<reqwest::Client>; 
}

impl TypeMapKey for ShardManagerContainer {
    type Value = Arc<Mutex<ShardManager>>;
}