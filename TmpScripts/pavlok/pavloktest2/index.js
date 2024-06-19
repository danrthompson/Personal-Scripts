const pavlok = require("pavlok");

CLIENT_ID = "30f28d0653ba917815116cc647910fced7ee702903c177ac45532a203801d6a2";
CLIENT_SECRET =
    "ef020fab33c95372a72e828b4680e524699b064d0349085c496915c9093d2b91";

pavlok.init(CLIENT_ID, CLIENT_SECRET);
pavlok.login(function (result, code) {
    console.log(result);
    if (result) {
        console.log("Code is " + code);
        pavlok.vibrate({ value: 255 }); // or you can call other methods like beep() or zap()
    }
});
