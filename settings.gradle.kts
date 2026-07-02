rootProject.name = "CNCVerse"

// This file sets what projects are included. All new projects should get automatically included unless specified in "disabled" variable.

val disabled = listOf<String>()

File(rootDir, ".").eachDir { dir ->
    if (!disabled.contains(dir.name) && File(dir, "build.gradle.kts").exists()) {
        // Sanitise the project name: replace spaces with underscores so Gradle
        // can reference the project by a valid identifier, then point the
        // project directory at the actual folder (which may contain spaces).
        val projectName = dir.name.replace(" ", "_")
        include(projectName)
        project(":$projectName").projectDir = dir
    }
}

fun File.eachDir(block: (File) -> Unit) {
    listFiles()?.filter { it.isDirectory }?.forEach { block(it) }
}

// To only include a single project, comment out the previous lines (except the first one), and include your plugin like so:
// include("PluginName")
