import bpy

def remove_collection_entry(entry_name, collection):
    index=collection.find(entry_name)
    collection.remove(index)
    return index

class GNPRESET_OT_remove_preset(bpy.types.Operator):
    bl_idname = "gnpreset.remove_preset"
    bl_label = "Remove Preset"
    bl_description = "Remove active preset"
    bl_options = {"INTERNAL","REGISTER","UNDO"}

    preset_name: bpy.props.StringProperty(name="Name", default="New Preset")

    @classmethod
    def poll(cls, context):
        if context.object.modifiers.active:
            active=context.object.modifiers.active
            if active.type=="NODES" and active.node_group:
                return not active.node_group.library\
                and not active.node_group.override_library

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Are you sure ?")

    def execute(self, context):
        mod=context.object.modifiers.active
        presets=mod.node_group.gnpreset.presets

        index=remove_collection_entry(self.preset_name, presets)

        # Correct active preset prop
        if index!=0:
            index-=1
        if presets:
            mod.node_group.gnpreset.active_preset=presets[index].name

        self.report({'INFO'}, f"Preset {self.preset_name} removed")

        # Redraw ui
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}

### REGISTER ---
def register():
    bpy.utils.register_class(GNPRESET_OT_remove_preset)
def unregister():
    bpy.utils.unregister_class(GNPRESET_OT_remove_preset)
