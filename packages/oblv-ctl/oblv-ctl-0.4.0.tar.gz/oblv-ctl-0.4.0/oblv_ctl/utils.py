


class bcolors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    BLACK = "\033[99m"

    @staticmethod
    def green(message: str) -> str:
        return bcolors.GREEN + message + bcolors.ENDC

    @staticmethod
    def red(message: str) -> str:
        return bcolors.RED + message + bcolors.ENDC

    @staticmethod
    def yellow(message: str) -> str:
        return bcolors.YELLOW + message + bcolors.ENDC

    @staticmethod
    def bold(message: str, end_color: bool = False) -> str:
        msg = bcolors.BOLD + message
        if end_color:
            msg += bcolors.ENDC
        return msg

    @staticmethod
    def underline(message: str, end_color: bool = False) -> str:
        msg = bcolors.UNDERLINE + message
        if end_color:
            msg += bcolors.ENDC
        return msg

    @staticmethod
    def warning(message: str) -> str:
        return bcolors.bold(bcolors.yellow(message))

    @staticmethod
    def success(message: str) -> str:
        return bcolors.green(message)

    @staticmethod
    def failure(message: str) -> str:
        return bcolors.red(message)