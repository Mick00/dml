const util = require('util');
const exec = util.promisify(require('child_process').exec);
const { subtask } = require("hardhat/config");
const { TASK_NODE_SERVER_READY } = require("hardhat/builtin-tasks/task-names");

async function deploy() {
  console.log("Running ape deployment")
  const { stdout, stderr } = await exec("ape run deploy --network ::hardhat")
  console.log(stdout ?? stderr)
  console.log("Ape deployment completed")
}

subtask(TASK_NODE_SERVER_READY)
  .setAction(
    async (
      args,
      hre,
      runSuper
    ) => {
      await deploy()
      return runSuper(args)
    }
  );
// See https://hardhat.org/config/ for config options.
module.exports = {
  networks: {
    hardhat: {
      hardfork: "london",
      // Base fee of 0 allows use of 0 gas price when testing
      initialBaseFeePerGas: 0,
      accounts: {
        mnemonic: "test test test test test test test test test test test junk",
        path: "m/44'/60'/0'",
        count: 10
      }
    },
  },
};
