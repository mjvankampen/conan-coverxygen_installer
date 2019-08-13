from conans import ConanFile, CMake, tools


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_paths"

    def test(self):
        if not tools.cross_building(self.settings):
            self.run("coverxygen --version", run_environment=True)