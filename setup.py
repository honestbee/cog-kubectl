from distutils.core import setup

setup (
    name = "kubectl",
    version = "0.0.9",
    description = "Cog commands for kubectl",
    author = "Vincent De Smet",
    author_email = "vincent.desmet@honestbee.com",
    url = "https://github.com/honestbee/cog-kubectl",
    packages = ["kubectl", "kubectl.commands"],
    requires = ["pycog3 (>=0.1.25)"],
    keywords = ["cog", "kubernetes", "bot", "devops", "chatops", "automation"],
    classifiers = [
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
