const { User } = require("discord.js");

const data = require("../../data/users.json");
const fs = require("fs");

class UserManager {
  constructor() {
    this.users = data;
  }

  addWarning(user, reason) {
    this.users.find((s) => s.id === user).addWarning(reason);
    this._persist();
  }

  _persist() {
    fs.writeFileSync("../../data/users.json", JSON.stringify(this.users));
  }
}

module.exports = new UserManager();
