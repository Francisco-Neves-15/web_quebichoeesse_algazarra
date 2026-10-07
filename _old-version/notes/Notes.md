


### Commit's:

not added yet, optional:

Check for any "^" or "~" in `package.json` to see if there are any blocked dependencies.

```terminal
npx husky add .husky/pre-commit "npm run package:check"
```