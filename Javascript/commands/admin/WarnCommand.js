const Commando = require("discord.js-commando");

module.exports = class WarnCommand extends (
  Commando.Command
) {
  constructor(client) {
    super(client, {
      name: "warn",
      memberName: "warn",
      group: "admin",
      description: "Gives a warning to a specific user",
      argsCount: 1,
    });
  }

  async run(message, args) {
    // Logic
  }
};
