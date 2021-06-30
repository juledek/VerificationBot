const Commando = require("discord.js-commando");
const helper = require("../../models/CommandHelper");
const userManager = require("../../models/managers/UserManager");

module.exports = class WarnCommand extends (
  Commando.Command
) {
  constructor(client) {
    super(client, {
      name: "warn",
      memberName: "warn",
      group: "admin",
      description: "Gives a warning to a specific user",
      userPermissions: ["ADMINISTRATOR"],
    });
  }

  async run(message, args) {
    // Filter out if no args
    if (!!!args) {
      helper.replyThenDeleteBoth(
        message,
        "Geef de User ID mee als argument. This message will self-destruct in 10 seconds.",
        10000
      );
      return;
    }

    const argList = args.split(" ");

    // Filter out too many args
    if (args.length === 1) {
      helper.replyThenDeleteBoth(
        message,
        "Dit commando heeft meer dan 1 argument nodig, de User ID en de message. This message will self-destruct in 10 seconds.",
        10000
      );
      return;
    }

    const id = argList.shift();

    const warnMessage = argList.join(" ");

    const user = message.guild.members.resolve(id);

    if (!!!user) {
      helper.replyThenDeleteBoth(
        message,
        `User met ID ${id} kan niet worden gevonden. Geef een geldige ID in. This message will self-destruct in 5 seconds.`,
        5000
      );
      return;
    }
    userManager.addWarning(id, warnMessage);

  }
};
