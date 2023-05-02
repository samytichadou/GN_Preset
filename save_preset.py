import bpy

from . import remove_preset as remove

def return_nodegroup_inputs(modifier):
    input_list = []
    inputs=modifier.node_group.inputs
    for input in inputs:
        if not input.identifier=="Input_0":
            input_list.append([input.name, input.identifier, input.type, modifier[input.identifier]])
    return input_list

def remove_name_version(name):
    split=name.split(".")
    end=split[len(split)-1]
    try:
        int(end)
        return name.split(f".{end}")[0]
    except ValueError:
        return name

def find_unique_name(name, namecollection):
    try:
        namecollection[name]
    except KeyError:
        return name
    name_clean=remove_name_version(name)
    for i in range(1,1000):
        idx=str(i).zfill(3)
        new_name=f"{name_clean}.{idx}"
        try:
            namecollection[new_name]
        except KeyError:
            return new_name
    return name

def save_preset(name, collection, modifier):
    new_preset=modifier.node_group.gnpreset.presets.add()
    new_preset.name=name

    inputs=return_nodegroup_inputs(modifier)
    for input in inputs:
        # print(input)
        new_input=new_preset.inputs.add()
        new_input.name=input[0]
        new_input.identifier=input[1]
        new_input.type=input[2]
        setattr(new_input, input[2].lower(), input[3])

class GNPRESET_OT_save_preset(bpy.types.Operator):
    bl_idname = "gnpreset.save_preset"
    bl_label = "Save Preset"
    bl_description = "Add preset for this geometry nodegroup"
    bl_options = {"INTERNAL","REGISTER","UNDO"}

    preset_name: bpy.props.StringProperty(name="Name", default="New Preset")

    @classmethod
    def poll(cls, context):
        if context.object.modifiers.active:
            active=context.object.modifiers.active
            return active.type=="NODES" and active.node_group

    def invoke(self, context, event):
        self.preset_name=find_unique_name(
            self.preset_name,
            context.object.modifiers.active.node_group.gnpreset.presets
        )
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "preset_name")

    def execute(self, context):
        mod=context.object.modifiers.active
        preset_name=find_unique_name(
            self.preset_name,
            mod.node_group.gnpreset.presets
        )

        save_preset(
            preset_name,
            mod.node_group.gnpreset.presets,
            mod
        )

        mod.node_group.gnpreset.active_preset=preset_name

        self.report({'INFO'}, f"Preset {preset_name} saved")

        # Redraw ui
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}

class GNPRESET_OT_replace_preset(bpy.types.Operator):
    bl_idname = "gnpreset.replace_preset"
    bl_label = "Replace Preset"
    bl_description = "Replace active preset"
    bl_options = {"INTERNAL","REGISTER","UNDO"}

    preset_name: bpy.props.StringProperty(name="Name", default="New Preset")

    @classmethod
    def poll(cls, context):
        if context.object.modifiers.active:
            active=context.object.modifiers.active
            return active.type=="NODES" and active.node_group

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text=f"Replace {self.preset_name} ?")

    def execute(self, context):
        mod=context.object.modifiers.active
        presets=mod.node_group.gnpreset.presets

        remove.remove_collection_entry(
            self.preset_name,
            presets
        )

        save_preset(
            self.preset_name,
            presets,
            mod
        )

        mod.node_group.gnpreset.active_preset=self.preset_name

        self.report({'INFO'}, f"Preset {self.preset_name} saved")

        # Redraw ui
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}

### REGISTER ---
def register():
    bpy.utils.register_class(GNPRESET_OT_save_preset)
    bpy.utils.register_class(GNPRESET_OT_replace_preset)
def unregister():
    bpy.utils.unregister_class(GNPRESET_OT_save_preset)
    bpy.utils.unregister_class(GNPRESET_OT_replace_preset)
