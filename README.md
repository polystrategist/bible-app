# Believers Sword

<div align="center">

**A Bible study companion for reading, prayer, notes, highlights, and deeper daily devotion.**

[![Version](https://img.shields.io/badge/version-1.1.8-2563eb.svg)](https://github.com/JenuelDev/Believers-Sword/releases/latest)
[![Electron](https://img.shields.io/badge/Electron-41.0.3-47848F.svg)](https://www.electronjs.org/)
[![Vue 3](https://img.shields.io/badge/Vue-3-42B883.svg)](https://vuejs.org/)
[![License](https://img.shields.io/badge/license-GPL--3.0-16a34a.svg)](./LICENSE)

<br />
<br />


</div>

> "Your word is a lamp to my feet and a light to my path."
>
> Psalm 119:105

<div align="center">
  <img src="./design-assets/App%20for%20daily%20spiritual%20growth.png" alt="Believers Sword hero artwork" width="900" />
</div>

## Overview

Believers Sword is a desktop Bible app built to help believers stay close to Scripture throughout the day. It combines Bible reading, study tools, notes, highlights, prayer tracking, sermons, and offline-friendly access in one focused experience.

## Downloads

Desktop downloads are published through GitHub Releases. Microsoft Store installs are also available for Windows users.

- Windows installer: `NSIS` setup package
- Windows Portable: no-install portable executable
- macOS: `DMG`
- Linux: `AppImage`
- Microsoft Store: Store-managed Windows installation and updates

If a direct asset link changes on a future release, use the latest releases page:

- https://github.com/JenuelDev/Believers-Sword/releases/latest

## Features

- Read multiple Bible translations in a focused reader
- Highlight verses and organize them by color
- Create notes and clip notes while studying
- Save bookmarks for quick return
- Manage prayer lists and answered prayers
- Use Study Space to keep research organized
- Search verses quickly across installed modules
- Listen with audio and TTS features
- Explore commentary and verse comparison tools
- Work offline with local resources

## Screenshots

### Desktop

<div align="center">
  <img src="./design-assets/screenshots/desktop/desktop-hero-01.png" alt="Believers Sword desktop hero screenshot" width="300" />
  <img src="./design-assets/screenshots/desktop/desktop-preview-01.png" alt="Believers Sword desktop preview screenshot 1" width="300" />
  <img src="./design-assets/screenshots/desktop/desktop-preview-02.png" alt="Believers Sword desktop preview screenshot 2" width="300" />
</div>

<div align="center">
  <img src="./design-assets/screenshots/desktop/desktop-01.png" alt="Believers Sword desktop screenshot 1" width="300" />
  <img src="./design-assets/screenshots/desktop/desktop-02.png" alt="Believers Sword desktop screenshot 2" width="300" />
  <img src="./design-assets/screenshots/desktop/desktop-03.png" alt="Believers Sword desktop screenshot 3" width="300" />
</div>

<div align="center">
  <img src="./design-assets/screenshots/desktop/desktop-04.png" alt="Believers Sword desktop screenshot 4" width="300" />
  <img src="./design-assets/screenshots/desktop/desktop-05.png" alt="Believers Sword desktop screenshot 5" width="300" />
  <img src="./design-assets/screenshots/desktop/desktop-06.png" alt="Believers Sword desktop screenshot 6" width="300" />
</div>

<div align="center">
  <img src="./design-assets/screenshots/desktop/desktop-07.png" alt="Believers Sword desktop screenshot 7" width="300" />
</div>

### Mobile

<div align="center">
  <img src="./design-assets/screenshots/mobile/mobile-preview-01.jpg" alt="Believers Sword mobile preview screenshot 1" width="220" />
  <img src="./design-assets/screenshots/mobile/mobile-preview-02.jpg" alt="Believers Sword mobile preview screenshot 2" width="220" />
  <img src="./design-assets/screenshots/mobile/mobile-01.jpg" alt="Believers Sword mobile screenshot 1" width="220" />
  <img src="./design-assets/screenshots/mobile/mobile-02.jpg" alt="Believers Sword mobile screenshot 2" width="220" />
</div>

<div align="center">
  <img src="./design-assets/screenshots/mobile/mobile-03.jpg" alt="Believers Sword mobile screenshot 3" width="220" />
  <img src="./design-assets/screenshots/mobile/mobile-04.jpg" alt="Believers Sword mobile screenshot 4" width="220" />
  <img src="./design-assets/screenshots/mobile/mobile-05.jpg" alt="Believers Sword mobile screenshot 5" width="220" />
  <img src="./design-assets/screenshots/mobile/mobile-06.jpg" alt="Believers Sword mobile screenshot 6" width="220" />
</div>

## System Requirements

- Windows 10 or newer
- macOS build support when release assets are published
- Linux support through `AppImage`
- 2 GB RAM minimum
- Around 500 MB of free storage recommended

## Development

### Prerequisites

- Node.js
- Yarn

### Setup

```bash
git clone https://github.com/JenuelDev/Believers-Sword.git
cd Believers-Sword
yarn setup
```

### Run locally

```bash
yarn start
```

### Build desktop packages

```bash
yarn app:build
```

### Build Microsoft Store package

```bash
yarn app:build:msix
```

## Support

If the app blesses you and you want to support development:

<div align="center">

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20coffee&emoji=☕&slug=jenuel.dev&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/jenuel.dev)

</div>

- One-time donation: https://buymeacoffee.com/jenuel.dev
- Membership: https://buymeacoffee.com/jenuel.dev/membership
- GitHub Sponsors: https://github.com/sponsors/JenuelDev

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a branch for your change.
3. Commit your work.
4. Push the branch.
5. Open a pull request.

### PR Labels

When opening a pull request, please add one of the following labels so your change is categorized correctly in the release notes:

| Label | Use when |
|---|---|
| `feature` or `enhancement` | Adding new functionality |
| `bug` or `fix` | Fixing a bug |
| `improvement`, `refactor`, or `performance` | Improving existing code without adding features |
| `documentation` or `docs` | Updating documentation only |

**Examples:**

- Adding a new "verse of the day" feature → label: `feature`
- Fixing a crash when opening bookmarks → label: `bug`
- Speeding up Bible module loading → label: `performance`
- Updating the README → label: `docs`

If no label is added, your PR will appear under "Other Changes" in the release notes.

## License

This project is licensed under the GPL-3.0 license. See [LICENSE](./LICENSE).
