from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, text=None, children=children, props=props)

    def to_html(self):
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have at least one child!")
        if self.tag is None:
            raise ValueError("ParentNode must have a tag!")
        children = ''.join([child.to_html() for child in self.children])
        if len(self.props) == 0:
            return f"<{self.tag}>{children}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{children}</{self.tag}>"

    def __repr__(self):
        return f'HTMLNode(tag="{self.tag}", text="{self.value}", children={self.children}, props={self.props})'

