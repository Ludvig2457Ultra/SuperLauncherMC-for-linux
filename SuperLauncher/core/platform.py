import os
import platform
import shutil
import glob
import subprocess

class PlatformSupport:
    @staticmethod
    def get_minecraft_path():
        system = platform.system()
        if system == "Darwin":
            return os.path.expanduser("~/Library/Application Support/minecraft")
        elif system == "Windows":
            appdata = os.getenv('APPDATA')
            if appdata:
                return os.path.join(appdata, '.minecraft')
            return os.path.expanduser("~/.minecraft")
        return os.path.expanduser("~/.minecraft")

    @staticmethod
    def get_java_path():
        system = platform.system()
        common_paths = []
        if system == "Windows":
            pf = os.getenv("ProgramFiles", "C:\\Program Files")
            pfx86 = os.getenv("ProgramFiles(x86)", "C:\\Program Files (x86)")
            common_paths = [
                os.path.join(pf, "Java", "jdk-*", "bin", "java.exe"),
                os.path.join(pf, "Java", "jre-*", "bin", "java.exe"),
                os.path.join(pfx86, "Java", "jdk-*", "bin", "java.exe"),
                "C:\\ProgramData\\Oracle\\Java\\javapath\\java.exe",
            ]
        elif system == "Darwin":
            common_paths = ["/usr/bin/java", "/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java"]
        else:
            common_paths = ["/usr/bin/java", "/usr/lib/jvm/default-java/bin/java"]

        for p in common_paths:
            if "*" in p:
                matches = glob.glob(p)
                if matches:
                    return matches[0]
            elif os.path.exists(p):
                return p
        return shutil.which("java") or ""
