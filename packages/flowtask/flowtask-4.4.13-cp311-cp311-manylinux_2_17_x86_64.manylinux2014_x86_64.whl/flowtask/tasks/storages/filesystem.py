from typing import Union
from pathlib import Path, PurePath
from flowtask.exceptions import (
    FlowTaskError,
    TaskNotFound,
    TaskParseError,
    TaskDefinition
)
from flowtask.parsers import (
    JSONParser,
    TOMLParser,
    YAMLParser
)
from .abstract import AbstractTaskStorage


class FileTaskStorage(AbstractTaskStorage):
    """Saving Tasks on Filesystem.
    """
    def __init__(self, path: PurePath, *args, **kwargs):
        super(FileTaskStorage, self).__init__(*args, **kwargs)
        if not path:
            ## Default Task Path
            raise FlowTaskError(
                "Required Task Path for Filesystem Task Storage"
            )
        else:
            self.path = path
            if isinstance(path, str):
                self.path = Path(path)

    async def open_task(
        self,
        taskname: str,
        program: str
    ) -> Union[dict, str]:
        """open_task.
            Open A Task from FileSystem, support json, yaml and toml formats.
        """
        if not program:
            program = 'navigator'
        taskpath = self.path.joinpath(program, 'tasks')
        self.logger.notice(
            f'Program Task Path: {taskpath}'
        )
        for f in ('json', 'yaml', 'toml', ):
            filename = taskpath.joinpath(f'{taskname}.{f}')
            self.logger.info(f'Task File: {filename}')
            if filename.exists():
                try:
                    if f == 'json':
                        parse = JSONParser(str(filename))
                    elif f == 'yaml':
                        parse = YAMLParser(str(filename))
                    elif f == 'toml':
                        parse = TOMLParser(str(filename))
                    return await parse.run()
                except TaskParseError as err:
                    raise TaskParseError(
                        f"Task Parse Error for {filename}: {err}"
                    ) from err
                except Exception as err:
                    raise TaskDefinition(
                        f'DI: Error Parsing {f} Task in {taskname} \
                            for filename: {filename.name}: {err}'
                    ) from err
            else:
                raise TaskNotFound(
                    f'DI: Task {program}.{taskname} Not Found on file > {filename}'
                )
