from jinja2 import Environment, nodes
from jinja2.environment import Template


def render_without_context(template_source):
    env = Environment()
    ast = env.parse(template_source)

    def render_node(node):
        print(type(node))
        if isinstance(node, nodes.Template):
            return "".join(render_node(n) for n in node.body)
        elif isinstance(node, nodes.Output):
            return "".join(render_node(n) for n in node.nodes)
        elif isinstance(node, nodes.Const):
            return node.value
        elif isinstance(node, nodes.For):
            loop_body = "".join(render_node(n) for n in node.body)
            return "".join(
                loop_body for _ in range(4)
            )  # Assuming a loop of 4 iterations as an example
        else:
            return ""  # Skip or replace nodes that require context

    return render_node(ast)


# Example usage
template_source = """
            {{a.b * 2}} + {{b}} - {{c}} + {{a}}
            {% for j in range(0, 4) %}
                <!-- Vertical rectangle -->
                <rect id="{{b}}-{{j}}" x="{{ 10 + j * 50 }}" y="70" width="30" height="220" fill="#add9e6" svgre:clickable="true"/>
            {% endfor %}
"""

rendered_template = render_without_context(template_source)
print(rendered_template)
