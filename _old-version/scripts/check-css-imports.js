const fs = require('fs');
const path = require('path');

function resolvePath(importPath, currentFile) {
  // Remove aspas se houver
  importPath = importPath.replace(/['"]/g, '');
  
  // Se começa com @/, resolve usando o alias
  if (importPath.startsWith('@/')) {
    const relativePath = importPath.replace('@/', 'src/');
    return path.join(__dirname, '..', relativePath);
  }
  
  // Se é relativo, resolve em relação ao arquivo atual
  if (importPath.startsWith('./') || importPath.startsWith('../')) {
    return path.resolve(path.dirname(currentFile), importPath);
  }
  
  // Se é absoluto a partir de src
  if (importPath.startsWith('src/')) {
    return path.join(__dirname, '..', importPath);
  }
  
  // Tenta resolver como node_modules ou outros
  return path.join(__dirname, '..', importPath);
}

function checkCssImports(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const importRegex = /@import\s+['"]([^'"]+)['"]/g;
  const errors = [];
  
  let match;
  while ((match = importRegex.exec(content)) !== null) {
    const importPath = match[1];
    
    // Ignora imports de node_modules ou pacotes
    if (!importPath.startsWith('@/') && 
        !importPath.startsWith('./') && 
        !importPath.startsWith('../') &&
        !importPath.startsWith('src/')) {
      continue; // Provavelmente é tailwindcss ou outro pacote
    }
    
    const resolvedPath = resolvePath(importPath, filePath);
    
    // Tenta diferentes extensões
    const possiblePaths = [
      resolvedPath,
      resolvedPath + '.css',
      resolvedPath.replace(/\.css$/, '') + '.css'
    ];
    
    const exists = possiblePaths.some(p => {
      try {
        return fs.existsSync(p) && fs.statSync(p).isFile();
      } catch {
        return false;
      }
    });
    
    if (!exists) {
      errors.push({
        file: filePath,
        import: importPath,
        resolved: resolvedPath
      });
    }
  }
  
  return errors;
}

function findCssFiles(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  
  list.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat && stat.isDirectory()) {
      results = results.concat(findCssFiles(filePath));
    } else if (file.endsWith('.css')) {
      results.push(filePath);
    }
  });
  
  return results;
}

const srcDir = path.join(__dirname, '..', 'src');
const cssFiles = findCssFiles(srcDir);
const allErrors = [];

cssFiles.forEach(file => {
  const errors = checkCssImports(file);
  allErrors.push(...errors);
});

if (allErrors.length > 0) {
  console.error('fail: Errors found in CSS imports:');
  allErrors.forEach(error => {
    console.error(`   - ${error.file}`);
    console.error(`     Import: ${error.import}`);
    console.error(`     Arquivo não encontrado: ${error.resolved}`);
  });
  console.error('\nfail: Check that the imported CSS files exist and that the aliases (@) are correct.');
  process.exit(1);
}

process.exit(0);