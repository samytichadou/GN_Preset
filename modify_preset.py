import bpy

class GNPRESET_OT_modify_preset(bpy.types.Operator):
    bl_idname = "gnpreset.modify_preset"
    bl_label = "Modify Informations"
    bl_description = "Modify active preset name and description"
    bl_options = {"INTERNAL","REGISTER","UNDO"}

    preset_name: bpy.props.StringProperty()

    temp_name: bpy.props.StringProperty(name="Name")
    temp_description: bpy.props.StringProperty(
        name="Description",
        description = "Description, Double space allows a line break",
        )

    active_preset=None

    @classmethod
    def poll(cls, context):
        if context.object.modifiers.active:
            active=context.object.modifiers.active
            if active.type=="NODES" and active.node_group:
                return not active.node_group.library\
                and not active.node_group.override_library

    def invoke(self, context, event):
        self.active_preset=context.object.modifiers.active.node_group.gnpreset.presets[self.preset_name]

        self.temp_name=self.active_preset.name
        self.temp_description=self.active_preset.description
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "temp_name")
        layout.prop(self, "temp_description")

    def execute(self, context):
        self.active_preset.name=self.temp_name
        self.active_preset.description=self.temp_description

        # Redraw ui
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}

### REGISTER ---
def register():
    bpy.utils.register_class(GNPRESET_OT_modify_preset)
def unregister():
    bpy.utils.unregister_class(GNPRESET_OT_modify_preset)
