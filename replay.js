const fetch = require("node-fetch");
const fs = require("fs");

const replay_time_start = "2023-7-10 6:11:28";
const replay_time_end = "2023-7-10 6:21:33";

let lock = false;

let rts_replay_time = new Date(replay_time_start).getTime();
const end_time = new Date(replay_time_end).getTime();

if (!fs.existsSync("./replay")) fs.mkdirSync("./replay");

const clock = setInterval(() => {
	if (rts_replay_time > end_time) clearInterval(clock);
	if (lock) return;
	lock = true;
	const controller = new AbortController();
	setTimeout(() => controller.abort(), 2500);
	const controller1 = new AbortController();
	setTimeout(() => controller1.abort(), 2500);
	const _replay_time = Math.round(rts_replay_time / 1000);
	rts_replay_time += 1000;
	fetch(`https://exptech.com.tw/api/v2/trem/rts?time=${_replay_time * 1000}`, { signal: controller.signal })
		.then((ans) => ans.json())
		.then((ans) => {
			fetch(`https://exptech.com.tw/api/v1/earthquake/info?time=${_replay_time}&type=all`, { signal: controller1.signal })
				.then((ans1) => ans1.json())
				.then((ans_eew) => {
					lock = false;
					fs.writeFile(`./replay/${_replay_time}.trem`, JSON.stringify({ rts: ans, eew: ans_eew }), () => void 0);
				})
				.catch((err) => {
					lock = false;
					console.log(err);
				});
		})
		.catch((err) => {
			lock = false;
			console.log(err);
		});
}, 200);