import bpy

class GNPRESET_OT_remove_preset(bpy.types.Operator):
    bl_idname = "gnpreset.remove_preset"
    bl_label = "Remove Preset"
    bl_description = ""
    bl_options = {"INTERNAL","REGISTER","UNDO"}

    preset_name: bpy.props.StringProperty(name="Name", default="New Preset")

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Remove Preset, are you sure ?")

    def execute(self, context):
        mod=context.object.modifiers.active
        presets=mod.node_group.gnpreset_presets

        self.report({'INFO'}, f"Preset {self.preset_name} removed")

        return {'FINISHED'}

### REGISTER ---
def register():
    bpy.utils.register_class(GNPRESET_OT_remove_preset)
def unregister():
    bpy.utils.unregister_class(GNPRESET_OT_remove_preset)
