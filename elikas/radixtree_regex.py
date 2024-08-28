import re
from typing import Dict, Optional


class RadixNode:
    def __init__(self):
        self.children: Dict[str, RadixNode] = {}
        self.pattern: Optional[str] = None
        self.handler: Optional[callable] = None
        self.regex: Optional[re.Pattern] = None


class RadixTree:
    def __init__(self):
        self.root = RadixNode()

    def insert(self, pattern: str, handler: callable):
        node = self.root
        parts = pattern.strip("/").split("/")

        for part in parts:
            if part not in node.children:
                node.children[part] = RadixNode()
            node = node.children[part]

        node.pattern = pattern
        node.handler = handler
        node.regex = compile_pattern(pattern)

    def match(self, path: str) -> Optional[tuple]:
        node = self.root
        parts = path.strip("/").split("/")

        for part in parts:
            if part in node.children:
                node = node.children[part]
            elif any(child.startswith("{") for child in node.children):
                # Handle path parameter
                node = next(
                    node.children[child]
                    for child in node.children
                    if child.startswith("{")
                )
            else:
                return None

        if node.pattern and node.regex:
            match = node.regex.match(path)
            if match:
                return node.handler, match.groupdict()
        return None


def compile_pattern(pattern: str) -> re.Pattern:
    regex_pattern = "^"
    parts = pattern.strip("/").split("/")

    for part in parts:
        if part.startswith("{") and part.endswith("}"):
            # Extract the parameter name
            param_name = part[1:-1]
            regex_pattern += "/(?P<" + param_name + ">[^/]+)"
        else:
            regex_pattern += "/" + re.escape(part)

    regex_pattern += "$"
    return re.compile(regex_pattern)


class Router:
    def __init__(self):
        self.radix_tree = RadixTree()

    def add_route(self, pattern: str, handler: callable):
        self.radix_tree.insert(pattern, handler)

    def match(self, path: str) -> Optional[tuple]:
        return self.radix_tree.match(path)


# Example usage
def home_handler():
    return "Home Page"


def user_handler(user_id):
    return f"User Profile: {user_id}"


def category_handler(category, subcategory):
    return f"Category: {category}, Subcategory: {subcategory}"


router = Router()
router.add_route("/home", home_handler)
router.add_route("/user/{user_id}", user_handler)
router.add_route("/category/{category}/{subcategory}", category_handler)

# Test the router
test_paths = [
    "/home",
    "/user/123",
    "/category/electronics/smartphones",
    "/invalid/path",
]

for path in test_paths:
    result = router.match(path)
    if result:
        handler, params = result
        print(f"Path: {path}")
        print(f"Handler: {handler.__name__}")
        print(f"Params: {params}")
        print(f"Result: {handler(**params)}")
    else:
        print(f"No match found for path: {path}")
    print()
