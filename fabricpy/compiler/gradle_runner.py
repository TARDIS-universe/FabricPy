"""
Gradle runner - sets up the Gradle wrapper and runs the build.

Requirements:
  - Java 17+ must be installed
  - Gradle must be installed for first-time wrapper setup,
    OR the wrapper jar can be copied from another project.

After setup, ./gradlew handles everything automatically.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

GRADLE_VERSION = "8.6"


def _find_java_executable() -> str | None:
    """Find a Java 17+ executable, preferring JAVA_HOME over PATH."""
    candidates: list[Path] = []

    java_home = os.environ.get("JAVA_HOME")
    if java_home:
        candidates.append(Path(java_home) / "bin" / ("java.exe" if sys.platform == "win32" else "java"))

    if sys.platform == "win32":
        program_files = Path(os.environ.get("ProgramFiles", r"C:\Program Files"))
        jdk_root = program_files / "Java"
        if jdk_root.exists():
            for candidate in sorted(jdk_root.glob("jdk-*"), reverse=True):
                candidates.append(candidate / "bin" / "java.exe")

    which_java = shutil.which("java")
    if which_java:
        candidates.append(Path(which_java))

    seen: set[str] = set()
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except FileNotFoundError:
            continue
        if str(resolved) in seen or not resolved.exists():
            continue
        seen.add(str(resolved))
        try:
            result = subprocess.run(
                [str(resolved), "-version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
        output = result.stderr or result.stdout
        if any(f'version "{version}' in output for version in ("17", "18", "19", "20", "21", "22", "23")):
            return str(resolved)

    return None


def _build_env(java_exe: str | None = None) -> dict[str, str]:
    """Build an environment that prefers the selected Java executable."""
    env = os.environ.copy()
    if not java_exe:
        return env

    java_bin = str(Path(java_exe).parent)
    java_home = str(Path(java_exe).parent.parent)
    path_parts = [java_bin] + [
        part for part in env.get("PATH", "").split(os.pathsep)
        if part and part != java_bin
    ]
    env["JAVA_HOME"] = java_home
    env["PATH"] = os.pathsep.join(path_parts)
    return env


def _check_java() -> str | None:
    """Verify Java 17+ is available and return its executable path."""
    java_exe = _find_java_executable()
    if java_exe:
        return java_exe

    which_java = shutil.which("java")
    if which_java:
        try:
            result = subprocess.run(
                [which_java, "-version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            output = (result.stderr or result.stdout).strip()
        except (FileNotFoundError, subprocess.TimeoutExpired):
            output = ""
        if output:
            print(f"[fabricpy] Warning: Java 17+ required. Found: {output[:120]}")
        else:
            print("[fabricpy] Warning: Java 17+ required, but the detected 'java' could not be used.")
        return None

    print("[fabricpy] Error: Java 17+ not found. Set JAVA_HOME or install a JDK.")
    return None


def _setup_gradle_wrapper(project_dir: Path, env: dict[str, str]) -> bool:
    """
    Set up the Gradle wrapper in project_dir.

    Strategy:
    1. If `gradle` is on PATH, run `gradle wrapper --gradle-version 8.4`
    2. Otherwise, try to copy wrapper from another project.
    """
    wrapper_script = project_dir / ("gradlew.bat" if sys.platform == "win32" else "gradlew")
    wrapper_props = project_dir / "gradle" / "wrapper" / "gradle-wrapper.properties"

    if wrapper_script.exists() and wrapper_props.exists():
        props_text = wrapper_props.read_text(encoding="utf-8", errors="ignore")
        if f"gradle-{GRADLE_VERSION}-bin.zip" in props_text:
            print("[fabricpy] Gradle wrapper already present.")
            return True
        print(f"[fabricpy] Updating Gradle wrapper to {GRADLE_VERSION}...")
    elif wrapper_script.exists():
        print("[fabricpy] Gradle wrapper already present.")
        return True

    gradle_bin = shutil.which("gradle", path=env.get("PATH"))
    if gradle_bin:
        print("[fabricpy] Setting up Gradle wrapper via system Gradle...")
        result = subprocess.run(
            [gradle_bin, "wrapper", "--gradle-version", GRADLE_VERSION],
            cwd=project_dir,
            capture_output=True,
            text=True,
            env=env,
        )
        if result.returncode == 0:
            print("[fabricpy] Gradle wrapper ready.")
            return True
        print(f"[fabricpy] gradle wrapper failed:\n{result.stderr}")

    print("[fabricpy] Generating minimal Gradle wrapper scripts...")
    _write_wrapper_scripts(project_dir)

    jar_path = project_dir / "gradle" / "wrapper" / "gradle-wrapper.jar"
    jar_path.parent.mkdir(parents=True, exist_ok=True)

    jar_candidates = list(Path.home().rglob("gradle-wrapper.jar"))
    if jar_candidates:
        shutil.copy2(jar_candidates[0], jar_path)
        print(f"[fabricpy] Copied gradle-wrapper.jar from {jar_candidates[0]}")
        return True

    print("[fabricpy] Could not find gradle-wrapper.jar.")
    print("[fabricpy] Please install Gradle (https://gradle.org/install/) and run:")
    print(f"    cd {project_dir} && gradle wrapper --gradle-version {GRADLE_VERSION}")
    return False


def _write_wrapper_scripts(project_dir: Path):
    """Write gradlew and gradlew.bat scripts."""
    wrapper_dir = project_dir / "gradle" / "wrapper"
    wrapper_dir.mkdir(parents=True, exist_ok=True)

    (wrapper_dir / "gradle-wrapper.properties").write_text(
        "distributionBase=GRADLE_USER_HOME\n"
        "distributionPath=wrapper/dists\n"
        f"distributionUrl=https\\://services.gradle.org/distributions/gradle-{GRADLE_VERSION}-bin.zip\n"
        "networkTimeout=10000\n"
        "validateDistributionUrl=true\n"
        "zipStoreBase=GRADLE_USER_HOME\n"
        "zipStorePath=wrapper/dists\n"
    , encoding="utf-8")

    gradlew = r"""#!/bin/sh
##############################################################################
# Gradle start up script for UN*X
# Generated by fabricpy
##############################################################################
APP_HOME=$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")")
if [ -n "$JAVA_HOME" ]; then
  exec "$JAVA_HOME/bin/java" -jar "$APP_HOME/gradle/wrapper/gradle-wrapper.jar" "$@"
fi
exec java -jar "$APP_HOME/gradle/wrapper/gradle-wrapper.jar" "$@"
"""
    gradlew_path = project_dir / "gradlew"
    gradlew_path.write_text(gradlew)
    gradlew_path.chmod(0o755)

    (project_dir / "gradlew.bat").write_text(
        "@rem Generated by fabricpy\r\n"
        "@echo off\r\n"
        "if defined JAVA_HOME (\r\n"
        "  \"%JAVA_HOME%\\bin\\java.exe\" -jar \"%~dp0gradle\\wrapper\\gradle-wrapper.jar\" %*\r\n"
        ") else (\r\n"
        "  java -jar \"%~dp0gradle\\wrapper\\gradle-wrapper.jar\" %*\r\n"
        ")\r\n"
    )


def run_build(project_dir: Path, clean: bool = False, output_dir: Path = None) -> bool:
    """
    Run the Gradle build in project_dir and copy output .jar to output_dir.

    Returns True if build succeeded.
    """
    java_exe = _check_java()
    if not java_exe:
        return False

    env = _build_env(java_exe)

    if not _setup_gradle_wrapper(project_dir, env):
        print("[fabricpy] Build skipped - Gradle wrapper not set up.")
        print(f"[fabricpy] Source was generated at: {project_dir}")
        print("[fabricpy] Once you have Gradle installed, run:")
        print(f"    cd {project_dir} && gradle wrapper && ./gradlew build")
        return False

    gradlew = str(project_dir / ("gradlew.bat" if sys.platform == "win32" else "gradlew"))
    task = "clean build" if clean else "build"
    cmd = [gradlew] + task.split()

    print(f"[fabricpy] Running: {' '.join(cmd)}")
    print("[fabricpy] (This will download Minecraft and Fabric/Forge on first run - may take a few minutes)")

    try:
        result = subprocess.run(
            cmd,
            cwd=project_dir,
            timeout=600,
            env=env,
        )
    except subprocess.TimeoutExpired:
        print("[fabricpy] Build timed out after 10 minutes.")
        return False
    except KeyboardInterrupt:
        print("\n[fabricpy] Build cancelled.")
        return False

    if result.returncode != 0:
        print(f"[fabricpy] Build FAILED (exit code {result.returncode})")
        print("[fabricpy] Check the output above for Java compiler errors.")
        print(f"[fabricpy] Generated source is at: {project_dir / 'src'}")
        return False

    libs_dir = project_dir / "build" / "libs"
    if output_dir and libs_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        jars = [f for f in libs_dir.glob("*.jar") if "sources" not in f.name]
        for jar in jars:
            dest = output_dir / jar.name
            shutil.copy2(jar, dest)
            print(f"[fabricpy] Built: {dest}")

    return True
