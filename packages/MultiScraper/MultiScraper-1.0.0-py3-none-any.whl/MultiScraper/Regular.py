import re

class RegexExtractor:
    @staticmethod
    def extract_numbers(string):
        numbers = re.findall(r'\d+', string)
        return numbers

    @staticmethod
    def extract_symbols(string):
        symbols = re.findall(r'\D', string)
        return symbols

    @staticmethod
    def extract_emails(string):
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', string)
        return emails

    @staticmethod
    def extract_urls(string):
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
        return urls

    @staticmethod
    def extract_dates(string):
        dates = re.findall(r'\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b', string)
        return dates

    @staticmethod
    def extract_phone_numbers(string):
        phone_numbers = re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', string)
        return phone_numbers

    @staticmethod
    def extract_times(string):
        times = re.findall(r'\b\d{1,2}:\d{2}\b', string)
        return times

    @staticmethod
    def extract_ipv4_addresses(string):
        ipv4_addresses = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', string)
        return ipv4_addresses

    @staticmethod
    def extract_hex_colors(string):
        hex_colors = re.findall(r'#[a-fA-F0-9]{6}\b', string)
        return hex_colors

    @staticmethod
    def extract_credit_card_numbers(string):
        credit_card_numbers = re.findall(r'\b\d{4}[-.]?\d{4}[-.]?\d{4}[-.]?\d{4}\b', string)
        return credit_card_numbers

    @staticmethod
    def extract_hashtags(string):
        hashtags = re.findall(r'#\w+', string)
        return hashtags

    @staticmethod
    def extract_mentions(string):
        mentions = re.findall(r'@\w+', string)
        return mentions