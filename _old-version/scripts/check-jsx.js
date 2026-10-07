const fs = require("fs");
const path = require("path");

function findJsxFiles(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  
  list.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat && stat.isDirectory()) {
      results = results.concat(findJsxFiles(filePath));
    } else if (file.endsWith(".jsx")) {
      results.push(filePath);
    }
  });
  
  return results;
}

const srcDir = path.join(__dirname, "..", "src");
const jsxFiles = findJsxFiles(srcDir);

if (jsxFiles.length > 0) {
  console.error("fail: .jsx files found in the src directory:");
  jsxFiles.forEach(file => {
    console.error(`   - ${file}`);
  });
  console.error("\nfail: .jsx files are not allowed. Use .tsx, .ts, or .js files.\n");
  process.exit(1);
}

process.exit(0);