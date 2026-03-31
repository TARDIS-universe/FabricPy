# Building

## Requirements

- Python 3.10+
- Java 17+ for `1.20.1`
- Java 21+ for `1.21.1`
- Gradle available for first-time wrapper setup, or an existing `gradle-wrapper.jar`

`fabricpy` now prefers a matching installed JDK for the selected Minecraft version.

JDK selection:

- `1.20.1` prefers Java 17
- `1.21.1` prefers Java 21
- if both are installed side by side, `fabricpy` will try to pick the matching one automatically
- `JAVA_HOME` still works, but it no longer has to be the only way to switch versions

## Supported Matrix

- `1.20.1`: Fabric, Quilt, Forge
- `1.21.1`: Fabric, Quilt, Forge, NeoForge

Gradle wrapper selection:

- Fabric, Quilt, and NeoForge projects use Gradle `8.8`
- Forge `1.21.1` projects use Gradle `9.3.0`
- `fabricpy` selects the wrapper version automatically per generated loader project

What this means in practice:

- you do not need to manually swap Gradle versions between loaders
- you can keep Java 17 and Java 21 installed side by side
- `fabricpy` chooses Java by Minecraft version and Gradle by loader/version combination
- `JAVA_HOME` still overrides the shell, but `fabricpy` will try to pick a matching JDK on its own

## Commands

Build the example mod:

```powershell
python .\examples\tardis_mod.py
```

Clean build:

```powershell
python .\examples\tardis_mod.py --clean
```

Generate source only:

```powershell
python .\examples\tardis_mod.py --dry-run
```

Custom output directory:

```powershell
python .\examples\tardis_mod.py --output .\out
```

## Output

Generated projects:

- `.fabricpy_build\<modid>-fabric\`
- `.fabricpy_build\<modid>-quilt\`
- `.fabricpy_build\<modid>-forge\`
- `.fabricpy_build\<modid>-neoforge\`

Built jars:

- `dist\<fabric-jar>`
- `dist\<quilt-jar>`
- `dist\<forge-jar>`
- `dist\<neoforge-jar>`

## Troubleshooting

- Fabric or Quilt `1.21.1` item texture is missing:
  check the generated or overridden item model and make sure it points at `<modid>:item/...`
- block renders but break particles are wrong:
  check the final block model JSON for a `particle` texture entry
- Python fields look correct but Minecraft still uses the wrong model:
  a repo file under `assets/<modid>/models/...` or `assets/<modid>/blockstates/...` may be overriding the generated JSON
- build uses the wrong Java:
  verify both JDKs are installed and let `fabricpy` pick by version, or set `JAVA_HOME` explicitly for that shell
