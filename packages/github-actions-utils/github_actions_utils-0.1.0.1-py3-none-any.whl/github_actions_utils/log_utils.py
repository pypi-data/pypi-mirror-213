import inspect
import re
from string import Template


def github_group(group_name):
    def wrapper(f):
        objects_attributes = []
        for var in re.findall(r"\$\([\w.]+\)", group_name):
            attribute = re.sub(r"\$\(([\w.]+)\)", "\\1", var)
            # attribute_template = attribute.replace(".", "_")
            objects_attributes.append(attribute)

        def inner_wrapper(*args, **kwargs):
            inner_group_name = group_name
            template_dict = kwargs.copy()
            for index, name in enumerate(inspect.signature(f).parameters):
                template_dict[name] = args[index]

            for object_attribute in objects_attributes:
                value = template_dict
                for attr in object_attribute.split("."):
                    if isinstance(value, dict):
                        value = value.get(attr, None)
                    else:
                        value = getattr(value, attr, None)
                attribute_template = object_attribute.replace(".", "_")
                template_dict[attribute_template] = value
                inner_group_name = re.sub(rf"\$\({attribute}\)", f"${attribute_template}", inner_group_name)

            print(f"::group::{Template(inner_group_name).safe_substitute(**template_dict)}")
            resp = f(*args, **kwargs)
            print("::endgroup::")
            return resp

        return inner_wrapper

    return wrapper
