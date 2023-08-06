def inherit(child_obj, parent_obj, attributes):
    for attribute in attributes:
        if hasattr(parent_obj, attribute):
            parent_value = getattr(parent_obj, attribute)
            attempt_attribute_inheritance(child_obj, parent_value, attribute)

def attempt_attribute_inheritance(child_obj, parent_value, attribute):
    if hasattr(child_obj, attribute):
        child_has_attribute(child_obj, parent_value, attribute)
    else:
        setattr(child_obj, attribute, parent_value)

def child_has_attribute(child_obj, parent_value, attribute):
    if getattr(child_obj, attribute) is None:
        setattr(child_obj, attribute, parent_value)
