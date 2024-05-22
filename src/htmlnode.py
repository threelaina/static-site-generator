class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return None
        html_string = ""
        for key in self.props:
            html_string += " " + key + "=\"" + self.props[key] + "\""
        return html_string
    
    def __repr__(self) -> str:
        return f'HTMLNode(tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("no value provided for LeafNode")
        if self.tag is None:
            return self.value
        if self.props is None:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self) -> str:
        return f'LeafNode(tag = {self.tag}, value = {self.value}, props = {self.props})'
        

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("no tag provided for ParentNode")
        if self.children is None:
            raise ValueError("no children provided for ParentNode")
        if self.props is None:
            return f'<{self.tag}>{''.join([child.to_html() for child in self.children])}</{self.tag}>'
        return f'<{self.tag}{self.props_to_html()}{''.join([child.to_html() for child in self.children])}</{self.tag}>'
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
