class FileParsingResult:
    def __init__(self, file_name: str):
        self.file_name = file_name


    @property
    def has_errors(self) -> bool:
        return False


    @property
    def errors_count(self) -> int:
        return 0


    @property
    def has_warnings(self) -> bool:
        return False


    @property
    def warnings_count(self) -> int:
        return 0
