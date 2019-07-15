use std::sync::{
    Arc,
};

use serenity::prelude::{
    Context,
};

use reqwest::{
    Client,
};

pub fn get_session(ctx: &Context) -> Arc<Client> {
    let d = ctx.data.lock();
    d.get::<ReqwestClient>().unwrap().clone()
}