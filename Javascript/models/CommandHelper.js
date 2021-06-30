module.exports = class CommandHelper {
    static replyThenDeleteBoth(message, string, time) {
      message
        .reply(string)
        .then((s) => s.delete({ timeout: time }).then((t) => message.delete()))
        .catch((s) => console.log(s))
        .catch((s) => console.log(s));
    }
  };
  