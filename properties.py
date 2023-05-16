import bpy

type_items = [
    ('STRING', 'String', ""),
    ('BOOLEAN', 'Boolean', ""),
    ('MATERIAL', 'Material', ""),
    ('VECTOR', 'Vector', ""),
    ('INT', 'Integer', ""),
    ('COLLECTION', 'Collection', ""),
    ('TEXTURE', 'Texture', ""),
    ('VALUE', 'Float', ""),
    ('RGBA', 'Color', ""),
    ('OBJECT', 'Object', ""),
    ('IMAGE', 'Image', ""),
]

class GNPRESET_PR_input(bpy.types.PropertyGroup):
    identifier: bpy.props.StringProperty()
    type: bpy.props.EnumProperty(items = type_items)

    string: bpy.props.StringProperty()
    boolean: bpy.props.BoolProperty()
    value: bpy.props.FloatProperty()
    rgba: bpy.props.FloatVectorProperty(subtype="COLOR", size=4)
    vector: bpy.props.FloatVectorProperty(subtype="XYZ")
    int: bpy.props.IntProperty()

    material: bpy.props.PointerProperty(type=bpy.types.Material)
    collection: bpy.props.PointerProperty(type=bpy.types.Collection)
    texture: bpy.props.PointerProperty(type=bpy.types.Texture)
    object: bpy.props.PointerProperty(type=bpy.types.Object)
    image: bpy.props.PointerProperty(type=bpy.types.Image)

class GNPRESET_PR_preset(bpy.types.PropertyGroup):
    inputs: bpy.props.CollectionProperty(
        type = GNPRESET_PR_input,
        name="Inputs",
        )
    description: bpy.props.StringProperty(
        name = "Preset Description",
        description = "Description, Double space allows a line break",
        )

def get_presets_items(self, context):
    items = []
    for p in self.presets:
        items.append((p.name, p.name, ""))
    items=sorted(items)
    return items

class GNPRESET_PR_main(bpy.types.PropertyGroup):
    presets: bpy.props.CollectionProperty(
        type = GNPRESET_PR_preset, name="Presets",
        )
    active_preset: bpy.props.EnumProperty(
        name="Active Presets",
        items=get_presets_items,
        override = {"LIBRARY_OVERRIDABLE"},
        )
    description: bpy.props.StringProperty(name="Description")
    url: bpy.props.StringProperty(name="URL")

### REGISTER ---
def register():
    bpy.utils.register_class(GNPRESET_PR_input)
    bpy.utils.register_class(GNPRESET_PR_preset)
    bpy.utils.register_class(GNPRESET_PR_main)

    bpy.types.GeometryNodeTree.gnpreset= \
        bpy.props.PointerProperty(
            type = GNPRESET_PR_main, name="GN Presets",
            override = {"LIBRARY_OVERRIDABLE"},
            )
def unregister():
    bpy.utils.unregister_class(GNPRESET_PR_input)
    bpy.utils.unregister_class(GNPRESET_PR_preset)
    bpy.utils.unregister_class(GNPRESET_PR_main)

    del bpy.types.GeometryNodeTree.gnpreset
