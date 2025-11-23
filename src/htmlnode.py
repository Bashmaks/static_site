class HTMLNode():
    def __init__(self, tag=None, text=None, children=None, props=None):
        self.tag = tag
        self.value = text
        self.props = {}
        self.children = None
        if self.value is None:
            self.children = []
        if children is not None:
            self.children = [*children]
        if props is not None:
            self.props.update(props)

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        props_list = [f'{prop}="{val}"' for prop,val in self.props.items()]
        return " ".join(props_list)

    def __repr__(self):
        return f'HTMLNode(tag="{self.tag}", text="{self.value}", children={self.children}, props={self.props})'
