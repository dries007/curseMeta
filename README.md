# CurseMeta

CurseMeta a CurseForge integration platform powered by [alpacka-meta](https://github.com/NikkyAI/alpacka-meta).

The output is post processed by the [CurseMeta](docker/CurseMeta) python package.

This repository will also server for any issues with the web service associated with this project.

A hosted version is available at [cursemeta.dries007.net](https://cursemeta.dries007.net/).

The static HTML is generated with the [Markdown.py](Markdown.py) script.

Need to contact me? GH issues work, but [Discord (also good for updates)](https://discord.gg/zCQaCAA) or [Twitter](https://twitter.com/driesk007) are good too.

Documentation
-------------

- [API v1](api/v1/README.md)
- [DevInfo](static_md/devinfo.md)

A note on docker
----------------

If you want to tail a file to do the keep-alive, like we do in /docker/Dockerfile, be sure the file is created in by the CMD instruction.
Otherwise the file will exists in a different layer of the file system and tail will not get any updates...
