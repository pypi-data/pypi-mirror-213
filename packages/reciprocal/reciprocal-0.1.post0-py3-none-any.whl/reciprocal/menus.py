from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Callable
from typing import Optional
from typing import Tuple

import click

from reciprocal import config
from reciprocal import utils

OptionType = Callable[[], Any]
InputOptionType = str | OptionType


@dataclass
class Action:
    """An action allows you to specify a descriptive name and a handler which will
    be called with the specified args and kwargs (if present)

        :param name: a descriptive name for the action, which will be shown on menus
        :param handler: callable which will be called if the action is chosen for execution
        :param args: positional arguments to be passed to the handler
        :param kwargs: keyword arguments to be passed to the handler
    """
    name: str
    handler: Callable[..., Any]
    args: list[Any] = field(default_factory=list)
    kwargs: dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return self.name

    def __call__(self) -> Any:
        return self.handler(*self.args, **self.kwargs)


class LiteralAction(Action):
    """An action that returns a literal"""

    def __init__(self, literal: str, display_name: str | None = None) -> None:
        if display_name:
            return super().__init__(name=display_name, handler=lambda: literal)
        return super().__init__(name=literal, handler=lambda: literal)


class ExitCode:
    pass


EXIT_CODE = ExitCode()
EXIT_ACTION = Action("Exit", lambda: EXIT_CODE)


class Menu():
    """Menu used to display a list of options for the user to choose.

        :param name: a name for the menu, will be used in the __str__ method. Useful to nest menus!
        :param options: options from which the user will be able to choose
        :param handler: callable which will be called with the result from the chosen option
        :param hide_cursor: whether to hide the console cursor while the menu is being displayed, defaults to True
        :param prompt: prompt shown next to the hovered option, defaults to ">"
        :param prefix: prefix for each option, defaults to "[{i}] "
        :param header: header message shown before the options, defaults to ""
        :param hovered_fg: text color for the hovered option, defaults to None
        :param hovered_bg: background color for the hovered option, defaults to None
        :param clip_prompt: _description_, defaults to True
    """
    name: str
    options: list[OptionType]
    handler: Optional[Callable[[Any], Any]]
    hide_cursor: bool
    prompt: str
    prefix: str
    header: str
    hovered_fg: Optional[int | Tuple[int, int, int] | str]
    hovered_bg: Optional[int | Tuple[int, int, int] | str]
    _selected_option: int = -1
    _longest_option: int = 0

    def __init__(
        self,
        name: str,
        options: list[InputOptionType],
        handler: Optional[Callable[[Any], Any]] = None,
        hide_cursor: bool = True,
        prompt: str = ">",
        prefix: str = "[{i}] ",
        header: str = "",
        hovered_fg: Optional[int | Tuple[int, int, int] | str] = None,
        hovered_bg: Optional[int | Tuple[int, int, int] | str] = None
    ) -> None:
        self.options = self._build_options(options)
        self.name = name
        self.handler = handler
        self.hide_cursor = hide_cursor
        self.prompt = prompt
        self.prefix = prefix
        self.header = header
        self.hovered_fg = hovered_fg or config.SELECTED_FG
        self.hovered_bg = hovered_bg or config.SELECTED_BG

    def _build_options(self, input: list[InputOptionType]) -> list[OptionType]:
        options: list[OptionType] = []
        for option in input:
            if isinstance(option, str):
                options.append(LiteralAction(option))
            else:
                options.append(option)
        options.append(EXIT_ACTION)
        return options

    def _display(self) -> None:
        if self.header:
            click.echo(self.header)
        self._display_options()

    def _display_options(self) -> None:
        for (i, option) in enumerate(self.options):
            ind = "X" if option == EXIT_ACTION else i + 1
            if i == self._selected_option:
                option_str = f"{self.prompt}{self.prefix.format(i=ind)}{option}"
                click.secho(option_str, fg=self.hovered_fg, bg=self.hovered_bg)
            else:
                option_str = f"{' ' * len(self.prompt)}{self.prefix.format(i=ind)}{option}"
                click.echo(option_str)

    def _restore_cursor(self) -> None:
        utils.cursor_up(len(self.options) + 1)

    def _clear_console(self) -> None:
        self._restore_cursor()
        utils.clear_after_cursor()

    def _await_selection(self) -> OptionType:
        while True:
            pressed_key = click.getchar()
            if pressed_key == utils.ARROW_UP:
                if self._selected_option > 0:
                    self._selected_option -= 1
                    self._restore_cursor()
                    self._display_options()
            elif pressed_key == utils.ARROW_DOWN:
                if self._selected_option < len(self.options) - 1:
                    self._selected_option += 1
                    self._restore_cursor()
                    self._display_options()
            elif pressed_key == '\r':  # ENTER
                self._clear_console()
                return self.options[self._selected_option]

    def execute(self) -> Any:
        """Displays the menu and returns once the user has made their choice
        AND the handler has completed its execution.

            :return the return value of the selected action's handler
        """
        self._selected_option = 0
        self._display()
        try:
            if self.hide_cursor:
                utils.hide_cursor()
            callable = self._await_selection()
            if self.handler:
                return self.handler(callable())
            return callable()
        except: # noqa E722
            raise
        finally:
            if self.hide_cursor:
                utils.show_cursor()

    def __call__(self) -> Any:
        return self.execute()

    def __str__(self) -> str:
        return self.name

    def add_option(self, option: OptionType) -> None:
        self.options.insert(len(self.options) - 1, option)
