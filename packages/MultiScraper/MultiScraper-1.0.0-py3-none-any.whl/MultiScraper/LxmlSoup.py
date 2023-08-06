from lxml import etree

class LxmlSoup:
    def __init__(self, html_content):
        self.root = etree.HTML(html_content)

    def findel(self, tag=None, **attrs):
        xpath = self._build_xpath(tag, **attrs)
        elements = self.root.xpath(xpath)
        return [LxmlElement(element) for element in elements]

    def find_all(self, tag=None, **attrs):
        xpath = self._build_xpath(tag, **attrs)
        elements = self.root.xpath(xpath)
        return [LxmlElement(element) for element in elements]

    def find(self, tag=None, **attrs):
        elements = self.findel(tag, **attrs)
        if elements:
            return elements[0]
        return None

    def _build_xpath(self, tag=None, **attrs):
        xpath = "//"
        if tag:
            xpath += tag
        if attrs:
            predicates = []
            for key, value in attrs.items():
                if key == 'class_':
                    key = key[0:-1]
                predicates.append(f'[@{key}="{value}"]')
            xpath += "".join(predicates)
        return xpath

    def text(self):
        return ''.join(etree.XPath("//text()")(self.root))


class LxmlElement:
    def __init__(self, element):
        self.element = element

    def findel(self, tag=None, **attrs):
        xpath = self._build_xpath(tag, **attrs)
        elements = self.element.xpath(xpath)
        return [LxmlElement(element) for element in elements]

    def find_all(self, tag=None, **attrs):
        xpath = self._build_xpath(tag, **attrs)
        elements = self.element.xpath(xpath)
        return [LxmlElement(element) for element in elements]

    def find(self, tag=None, **attrs):
        elements = self.findel(tag, **attrs)
        if elements:
            return elements[0]
        return None

    def _build_xpath(self, tag=None, **attrs):
        xpath = ".//"
        if tag:
            xpath += tag
        if attrs:
            predicates = []
            for key, value in attrs.items():
                if key == 'class_':
                    key = key[0:-1]
                predicates.append(f'[@{key}="{value}"]')
            xpath += "".join(predicates)
        return xpath

    def text(self):
        return ''.join(self.element.xpath(".//text()")).strip()

    def attribute(self, name):
        return self.element.get(name)

    def get(self, name, default=None):
        return self.element.get(name, default)

    def to_html(self):
        return etree.tostring(self.element, encoding='unicode')

    def __str__(self):
        return etree.tostring(self.element, encoding='unicode')

    def __repr__(self):
        return str(self)

    def __call__(self):
        return self.element.text_content()


