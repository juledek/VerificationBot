const commando = require("discord.js-commando");
const fs = require("fs");
const config = require("dotenv").config({ path: __dirname + "/.env" });
const path = require("path");
const userManager = require("./models/managers/UserManager");

// Create the client for this bot and set common settings
const client = new commando.CommandoClient({
  owner: process.env.OWNER, //TODO change when bot ownership goes to admin account
  commandPrefix: "$",
  unknownCommandResponse: true,
});

client.registry
  .registerDefaults()
  .registerGroups([
    ["admin", "Admin commands"],
    ["user", "User commands"],
  ])
  .registerCommandsIn(path.join(__dirname, "commands")); //Registers where the command files can be find, separated by group in a folder with that groups nam

// Whenever bot is ready, display and wait for other setup to finish
client.on("ready", () => {
  console.log("Bot is up and running!");
});

client.login(process.env.TOKEN);