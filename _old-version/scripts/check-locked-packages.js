const fs = require("fs");
const path = require("path");

const packageJsonPath = path.join(process.cwd(), "package.json");
const packageJson = JSON.parse(
  fs.readFileSync(packageJsonPath, "utf8")
);

const invalidDeps = [];

function checkDeps(deps, sectionName) {
  if (!deps) return;

  Object.entries(deps).forEach(([name, version]) => {
    if (typeof version === "string" && /^[~^]/.test(version)) {
      invalidDeps.push(`${sectionName} -> ${name}: ${version}`);
    }
  });
}

checkDeps(packageJson.dependencies, "dependencies");
checkDeps(packageJson.devDependencies, "devDependencies");
checkDeps(packageJson.peerDependencies, "peerDependencies");

if (invalidDeps.length > 0) {
  console.error("fail: Unblocked dependencies found:\n");
  invalidDeps.forEach(dep => console.error(` - ${dep}`));
  console.error("\nRemove the ^ or ~ symbols from the versions in package.json. | OR | Run: `npm run package:lock` for easier execution.\n");
  process.exit(1);
}

console.log("pass: All dependencies are locked");
process.exit(0);
