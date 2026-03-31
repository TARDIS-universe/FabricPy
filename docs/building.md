# Building

## Requirements

- Python 3.10+
- Java 17+
- Gradle 8.6+

`fabricpy` now prefers `JAVA_HOME` and a real JDK 17 installation when building generated projects.

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
- `.fabricpy_build\<modid>-forge\`

Built jars:

- `dist\<fabric-jar>`
- `dist\<forge-jar>`
