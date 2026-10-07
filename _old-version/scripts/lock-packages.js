const fs = require("fs");
const path = require("path");

const packageJsonPath = path.join(process.cwd(), "package.json");

const packageJson = JSON.parse(
  fs.readFileSync(packageJsonPath, "utf8")
);

let changed = false;

function lockDeps(deps) {
  if (!deps) return;

  Object.keys(deps).forEach(dep => {
    const version = deps[dep];

    if (typeof version === "string" && /^[~^]/.test(version)) {
      deps[dep] = version.replace(/^[~^]/, "");
      changed = true;
    }
  });
}

lockDeps(packageJson.dependencies);
lockDeps(packageJson.devDependencies);
lockDeps(packageJson.peerDependencies);
lockDeps(packageJson.optionalDependencies);

if (changed) {
  fs.writeFileSync(
    packageJsonPath,
    JSON.stringify(packageJson, null, 2) + "\n"
  );

  console.log("pass: package.json updated: locked versions");
} else {
  console.log("pass: No version with ^ or ~ found.");
}
