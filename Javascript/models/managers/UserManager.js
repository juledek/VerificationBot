const data = require("../../data/users.json");
const fs = require("fs");
const { Warning, User } = require("../models");

class UserManager {
  constructor() {
    this.users = [];
    this._loadData();
  }

  _loadData() {
    data.forEach((s) => {
      let warnings = s.warnings.map(
        (t) => new Warning(t.message, Date.parse(t.timestamp))
      );
      this.users.push(new User(s.id, warnings));
    });
  }

  addWarning(userID, reason) {
    let user = this.users.find((s) => s.id === userID);
    if (!!!user) {
      user = new User(userID);
      this.users.push(user);
    }
    user.addWarning(reason);
    this._persist();
  }

  _persist() {
    fs.writeFileSync("./data/users.json", JSON.stringify(this.users));
  }
}

module.exports = new UserManager();
