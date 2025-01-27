class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props == None:
            return ""
        props_string = ""
        for key, value in self.props.items():
            props_string += f' {key}="{value}"'
        return props_string

    def __repr__(self):
        print(f"the tag: {self.tag}")
        print(f"the value: {self.value}")
        print(f"the children: {self.children}")
        print(f"the props: {self.props}")
        # return (f"LeafNode(tag={self.tag}, value={self.value}, "
        #     f"children={self.children}, props={self.props})")


    def __eq__(self, other):
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)


class LeafNode(HTMLNode):
    def __init__(self,value,tag=None,props=None):
        super().__init__(tag=tag,value=value,children=None,props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        props_string = self.props_to_html()
        if self.tag == None:
            return f"{self.value}"
        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag=tag,value=None,children=children,props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("no tag")
        if self.children == None or len(self.children) < 1:
            raise ValueError("no children")
        children_html = "".join(child.to_html() for child in self.children)
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"


