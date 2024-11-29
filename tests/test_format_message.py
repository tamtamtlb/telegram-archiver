import unittest
from telethon.tl.types import (
    MessageEntityBold,
    MessageEntityItalic,
    MessageEntityUnderline,
    MessageEntityStrike,
    MessageEntityCode,
    MessageEntityPre,
    MessageEntityUrl,
    MessageEntityTextUrl,
)
from telegram_exporter.main import format_message_to_html


class MockMessage:
    """
    A mock class to simulate a Telegram message with entities.
    """

    def __init__(self, message, entities):
        """
        Initializes a mock message object.

        Args:
            message (str): The text of the message.
            entities (list): A list of entity objects
            that represent text formatting or hyperlinks.
        """
        self.message = message
        self.entities = entities


class TestFormatMessageToHtml(unittest.TestCase):
    """
    Unit tests for the `format_message_to_html` function.
    """

    def test_format_bold(self):
        """
        Tests formatting bold text.
        """
        message = MockMessage(
            message="This is bold",
            entities=[MessageEntityBold(offset=8, length=4)],
        )
        expected_result = "This is <b>bold</b>"

        result = format_message_to_html(message)

        self.assertEqual(result, expected_result)

    def test_format_italic(self):
        """
        Tests formatting italic text.
        """
        message = MockMessage(
            message="This is italic",
            entities=[MessageEntityItalic(offset=8, length=6)],
        )
        expected_result = "This is <i>italic</i>"

        result = format_message_to_html(message)

        self.assertEqual(result, expected_result)

    def test_format_underline(self):
        """
        Tests formatting underlined text.
        """
        message = MockMessage(
            message="This is underlined",
            entities=[MessageEntityUnderline(offset=8, length=10)],
        )
        expected_result = "This is <u>underlined</u>"

        result = format_message_to_html(message)

        self.assertEqual(result, expected_result)

    def test_format_strikethrough(self):
        """
        Tests formatting strikethrough text.
        """
        message = MockMessage(
            message="This is strikethrough",
            entities=[MessageEntityStrike(offset=8, length=13)],
        )
        expected_result = "This is <s>strikethrough</s>"

        result = format_message_to_html(message)

        self.assertEqual(result, expected_result)

    def test_format_code(self):
        """
        Tests formatting inline code.
        """
        message = MockMessage(
            message="This is code",
            entities=[MessageEntityCode(offset=8, length=4)],
        )
        expected_result = "This is <code>code</code>"

        result = format_message_to_html(message)

        self.assertEqual(result, expected_result)

    def test_format_pre(self):
        """
        Tests formatting preformatted text.
        """
        message = MockMessage(
            message="This is preformatted text",
            entities=[MessageEntityPre(offset=8, length=17, language="")],
        )
        expected_result = "This is <pre>preformatted text</pre>"

        result = format_message_to_html(message)

        self.assertEqual(result, expected_result)

    def test_format_url(self):
        """
        Tests formatting plain URLs.
        """
        message = MockMessage(
            message="Visit https://example.com",
            entities=[MessageEntityUrl(offset=6, length=19)],
        )
        expected_result = (
            'Visit <a href="https://example.com">https://example.com</a>'
        )

        result = format_message_to_html(message)

        self.assertEqual(result, expected_result)

    def test_format_text_url(self):
        """
        Tests formatting hyperlinked text with a URL.
        """
        message = MockMessage(
            message="Click here",
            entities=[
                MessageEntityTextUrl(
                    offset=0, length=10, url="https://example.com"
                )
            ],
        )
        expected_result = '<a href="https://example.com">Click here</a>'

        result = format_message_to_html(message)

        self.assertEqual(result, expected_result)

    def test_format_multiple_entities(self):
        """
        Tests formatting text with multiple entities.
        """
        message = MockMessage(
            message="Bold and italic text",
            entities=[
                MessageEntityBold(offset=0, length=4),
                MessageEntityItalic(offset=9, length=6),
            ],
        )
        expected_result = "<b>Bold</b> and <i>italic</i> text"

        result = format_message_to_html(message)

        self.assertEqual(result, expected_result)

    def test_no_entities(self):
        """
        Tests formatting plain text without any entities.
        """
        message = MockMessage(
            message="Plain text without entities",
            entities=[],
        )
        expected_result = "Plain text without entities"

        result = format_message_to_html(message)

        self.assertEqual(result, expected_result)

    def test_empty_message(self):
        """
        Tests formatting an empty message.
        """
        message = MockMessage(
            message="",
            entities=[],
        )
        expected_result = ""

        result = format_message_to_html(message)

        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
