const commando = require("discord.js-commando");
const fs = require("fs");
const path = require("path");
const userManager = require("./models/managers/UserManager");

// Create the client for this bot and set common settings
const client = new commando.CommandoClient({
  owner: process.env.OWNER, //TODO change when bot ownership goes to admin account
  commandPrefix: "$",
  unknownCommandResponse: true,
});



// Whenever bot is ready, display and wait for other setup to finish
client.on("on", () => {
  console.log("Bot is up and running!");
  wait(1000);
});

client.login(process.env.TOKEN);
