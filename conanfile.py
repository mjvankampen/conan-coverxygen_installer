from conans import ConanFile
from conans import tools
import PyInstaller.__main__
import os
import codecs

class CoverxygenConan(ConanFile):
    name = "coverxygen_installer"
    version = "1.5.0"
    url = "https://github.com/mjvk/conan-covergygen_installer"
    homepage = "https://github.com/psycofdj/coverxygen"
    topics = ("coverage", "documentation", "doxygen")
    author = "mjvk <>"
    description = ("Covergygen can generate documentation coverage statistics")
    license = "MIT"
    settings = "os_build", "arch_build"
    _source_subfolder = "sourcefolder"
    
    def _makeAbsoluteImport(self,input_name):
        tmp_name = input_name + ".bak"
        with codecs.open(input_name, 'r', encoding='utf8') as fi, \
            codecs.open(tmp_name, 'w', encoding='utf8') as fo:

            for line in fi:
                fo.write(line.replace("from .", "from coverxygen."))

        os.remove(input_name) # remove original
        os.rename(tmp_name, input_name) # rename temp to original name
                
    def source(self):
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version))
        os.rename("coverxygen-%s" % self.version, self._source_subfolder)
        
    def build(self):
        import pip
        #if hasattr(pip, "main"):
        #    pip.main(["install","lxml"])
        #else:
        #    from pip._internal import main
        #    main(["install", "PyInstaller","lxml"])
        mainfilename = os.path.join(self._source_subfolder,"coverxygen","__main__.py")
        self._makeAbsoluteImport(mainfilename)
        PyInstaller.__main__.run([  '--name=%s' % "coverxygen", 
                                    '--onefile', \
                                    '--workpath', os.path.join(self.build_folder,"build"),\
                                    '--distpath', os.path.join(self.build_folder,"bin"),\
                                    '--specpath', self.build_folder,\
                                    mainfilename])

    def package(self):
        self.copy("*coverxygen", dst="bin", src="bin", keep_path=False)
        self.copy("*coverxygen.exe", dst="bin", src="bin", keep_path=False)

    def deploy(self):
        self.copy("*", src="bin", dst="bin")
        
    def package_id(self):
        self.info.include_build_settings()
    
    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        