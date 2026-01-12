from typing import Callable, Optional


class AlertHandler:
    def __init__(self, page):
        self.page = page

    def accept_next(self):
        """
        Sets up a listener to automatically accept the next dialog that appears.
        Useful for simple success messages or confirmations.
        """
        self.page.once("dialog", lambda dialog: dialog.accept())

    def dismiss_next(self):
        """
        Sets up a listener to automatically dismiss (cancel) the next dialog.
        """
        self.page.once("dialog", lambda dialog: dialog.dismiss())

    def get_text_and_accept(self, trigger_action: Callable) -> str:
        """
        Sets up a listener, executes the trigger action (like clicking a button),
        captures the dialog message, accepts the dialog, and returns the message.

        Args:
            trigger_action: A function/lambda that triggers the alert (e.g., lambda: self.page.click(btn))

        Returns:
            str: The text content of the alert.
        """
        # Use expect_event context manager to WAIT for the dialog to appear.
        # This handles the timing gap between the click and the async fetch alert.
        with self.page.expect_event("dialog") as event_info:
            trigger_action()

        # event_info.value contains the actual Dialog object
        dialog = event_info.value
        message = dialog.message

        # Accept the dialog to close it
        dialog.accept()

        return message