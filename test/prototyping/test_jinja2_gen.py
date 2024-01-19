from jinja2 import Environment, meta, Undefined, DebugUndefined
from jinja2.nodes import Getattr, Filter
from omegaconf import OmegaConf


class CollectUndefined(Undefined):
    def __init__(self, name, parent=None, **kwargs):
        self.name = name
        self.parent = parent
        self.full_name = str(self)

    def __str__(self):
        if self.parent is not None:
            return f"{self.parent}.{self.name}"
        return self.name

    def __getattr__(self, name: str):
        return CollectUndefined(name, parent=self)


svg = """<rect x="{{a.c.d}}" y="{{a.b}}" z="{{a.c.e | default(a.c.d)}}" a="{{b | default(a.c.d)}}"  />"""

conf = OmegaConf.create({"a": {"b": 0, "c": {"d": 1}}})
OmegaConf.update(conf, key="a.c.d", value=2)

env = Environment()
# env = Environment(undefined=CollectUndefined)
t = env.from_string(svg)

for x in t.generate(OmegaConf.to_container(conf)):
    print("?", x)


# default_builtin = env.filters["default"]
# all_defaults = {}


# def default_record(element, default, *args, **kwargs):
#     print(type(element))
#     print("??", default, args, kwargs)
#     return default_builtin(element, default, *args, **kwargs)


# env.filters["default"] = default_record
# print(env.from_string(svg).render(conf))


def get_all_variables(ast):
    def recurse_getattr(g: Filter):
        if isinstance(g.node, Getattr):
            return recurse_getattr(g.node) + "." + g.attr
        return g.node.name + "." + g.attr

    all_fields = set()
    for g in ast.find_all(Getattr):
        all_fields.add(recurse_getattr(g))
    return all_fields


ast = env.parse(svg)
print(get_all_variables(ast))


# def get_default_filters(ast):
#     def get_filter_args(g):
#         # if isinstance(g.node, Getattr):
#         # return recurse_getattr(g.node) + "." + g.attr
#         print(g)

#         # return g.node.name + "." + g.attr

#     for g in ast.find_all(Filter):
#         args = get_filter_args(g)
#         print(args)


# print(get_default_filters(ast))


# # variables = {x: None for x in meta.find_undeclared_variables(ast)}
# print(variables)

# print(env.from_string(svg).render(OmegaConf.to_container(conf)))
# print(all_defaults)

# class InplaceUndefined(Undefined):
#     def __str__(self):
#         return f"{{{{{self._undefined_name}}}}}"


# def create_collector():
#     collected_variables = set()

#

#     return collected_variables, CollectUndefined


# def find_all_vars(template_content):
#     vars, undefined_cls = create_collector()
#     env = Environment(undefined=undefined_cls)
#     tpl = env.from_string(template_content)
#     tpl.render({})  # empty so all variables are undefined

#     return vars


# print(find_all_vars(svg))
