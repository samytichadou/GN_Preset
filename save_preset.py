import bpy

def return_nodegroup_inputs(modifier):
    input_list = []
    inputs=modifier.node_group.inputs
    for input in inputs:
        if not input.identifier=="Input_0":
            input_list.append([input.name, input.identifier, input.type, modifier[input.identifier]])
    return input_list

def find_unique_name(name, namecollection):
    try:
        namecollection[name]
    except KeyError:
        return name
    for i in range(1,1000):
        idx=str(i).zfill(3)
        new_name=f"{name}.{idx}"
        try:
            namecollection[new_name]
        except KeyError:
            return new_name
    return name

class GNPRESET_OT_save_preset(bpy.types.Operator):
    bl_idname = "gnpreset.save_preset"
    bl_label = "Save Preset"
    bl_description = ""
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
        layout.prop(self, "preset_name")

    def execute(self, context):
        mod=context.object.modifiers.active

        new_preset=mod.node_group.gnpreset_presets.add()
        new_preset.name=find_unique_name(
            self.preset_name,
            mod.node_group.gnpreset_presets
        )

        inputs=return_nodegroup_inputs(mod)
        for input in inputs:
            # print(input)
            new_input=new_preset.inputs.add()
            new_input.name=input[0]
            new_input.identifier=input[1]
            new_input.type=input[2]
            setattr(new_input, input[2].lower(), input[3])

        self.report({'INFO'}, f"Preset {new_preset.name} saved")

        # Redraw ui
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}

### REGISTER ---
def register():
    bpy.utils.register_class(GNPRESET_OT_save_preset)
def unregister():
    bpy.utils.unregister_class(GNPRESET_OT_save_preset)
