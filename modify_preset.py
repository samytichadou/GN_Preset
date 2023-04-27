import bpy

class GNPRESET_OT_modify_preset(bpy.types.Operator):
    bl_idname = "gnpreset.modify_preset"
    bl_label = "Modify Preset"
    bl_description = "Modify active preset"
    bl_options = {"INTERNAL","REGISTER","UNDO"}

    preset_name: bpy.props.StringProperty()

    temp_name: bpy.props.StringProperty(name="Name")
    temp_description: bpy.props.StringProperty(name="Description")
    temp_url: bpy.props.StringProperty(name="URL")

    active_preset=None

    @classmethod
    def poll(cls, context):
        if context.object.modifiers.active:
            active=context.object.modifiers.active
            return active.type=="NODES" and active.node_group

    def invoke(self, context, event):
        self.active_preset=context.object.modifiers.active.node_group.gnpreset_presets[self.preset_name]

        self.temp_name=self.active_preset.name
        self.temp_description=self.active_preset.description
        self.temp_url=self.active_preset.url
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "temp_name")
        layout.prop(self, "temp_description")
        layout.prop(self, "temp_url")

    def execute(self, context):
        self.active_preset.name=self.temp_name
        self.active_preset.description=self.temp_description
        self.active_preset.url=self.temp_url

        # Redraw ui
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}

### REGISTER ---
def register():
    bpy.utils.register_class(GNPRESET_OT_modify_preset)
def unregister():
    bpy.utils.unregister_class(GNPRESET_OT_modify_preset)