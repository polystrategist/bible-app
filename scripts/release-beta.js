// Tags and pushes a beta release: v<version>-beta.<n>
//
// Usage:
//   node scripts/release-beta.js        -> auto-increments to the next free number
//   node scripts/release-beta.js 3      -> uses beta number 3 explicitly
//
// The base version comes from package.json ("version"). The next number is found by
// scanning the remote tags (git ls-remote) so it never collides with a beta already
// pushed from another machine. Pushing the tag triggers .github/workflows/build-beta.yml.
const cp = require('child_process');
const pkg = require('../package.json');

const base = `v${pkg.version}-beta.`;

function nextNumber() {
    const out = cp.execSync(`git ls-remote --tags origin "${base}*"`, { encoding: 'utf8' });
    const nums = out
        .split('\n')
        .map((line) => line.split('refs/tags/')[1])
        .filter(Boolean)
        .map((tag) => tag.replace(/\^\{\}$/, '')) // strip annotated-tag deref suffix
        .filter((tag) => tag.startsWith(base))
        .map((tag) => parseInt(tag.slice(base.length), 10))
        .filter((n) => Number.isInteger(n));
    return nums.length ? Math.max(...nums) + 1 : 1;
}

const arg = process.argv[2];
const n = arg ? parseInt(arg, 10) : nextNumber();

if (!Number.isInteger(n) || n < 1) {
    console.error(`Invalid beta number: ${arg}`);
    process.exit(1);
}

const tag = `${base}${n}`;
console.log(`Releasing ${tag}`);
cp.execSync(`git tag ${tag}`, { stdio: 'inherit' });
cp.execSync(`git push origin ${tag}`, { stdio: 'inherit' });
