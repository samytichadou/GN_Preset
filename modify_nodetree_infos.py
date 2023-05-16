import bpy

class GNPRESET_OT_modify_nodetree_infos(bpy.types.Operator):
    bl_idname = "gnpreset.modify_nodetree_infos"
    bl_label = "Modify Nodetree Informations"
    bl_description = "Modify description and url of the nodetree"
    bl_options = {"INTERNAL","REGISTER","UNDO"}

    temp_description: bpy.props.StringProperty(
        name="Description",
        description="Description, Double space allows a line break",
        )
    temp_url: bpy.props.StringProperty(
        name="URL",
        )

    node_tree=None

    @classmethod
    def poll(cls, context):
        if context.object.modifiers.active:
            active=context.object.modifiers.active
            if active.type=="NODES" and active.node_group:
                return not active.node_group.library\
                and not active.node_group.override_library

    def invoke(self, context, event):
        self.node_tree=context.object.modifiers.active.node_group
        self.temp_description=self.node_tree.gnpreset.description
        self.temp_url=self.node_tree.gnpreset.url
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text=f"Nodetree : {self.node_tree.name}")
        layout.prop(self, "temp_description")
        layout.prop(self, "temp_url")

    def execute(self, context):
        self.node_tree.gnpreset.description=self.temp_description
        self.node_tree.gnpreset.url=self.temp_url

        # Redraw ui
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}

### REGISTER ---
def register():
    bpy.utils.register_class(GNPRESET_OT_modify_nodetree_infos)
def unregister():
    bpy.utils.unregister_class(GNPRESET_OT_modify_nodetree_infos)
