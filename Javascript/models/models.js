class User {
  constructor(id, warnings = []) {
    this.id = id;
    this.warnings = warnings;
  }

  addWarning(reason) {
    console.log("DerpUser");
    this.warnings.push(new Warning(reason));
  }
}

class Warning {
  constructor(message, timestamp = Date.now()) {
    (this.timestamp = timestamp), (this.message = message);
  }
}

module.exports = {
  User: User,
  Warning: Warning,
};
