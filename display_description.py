import bpy

def cut_long_text(text, line_length=50):
    rough_lines=text.split("  ")
    lines=[]
    for l in rough_lines:
        words=l.split(" ")
        temp_line=""
        for w in words:
            test=f"{temp_line}{w} "
            if len(test)>line_length:
                lines.append(temp_line)
                temp_line=f"{w} "
            else:
                temp_line=test
        if temp_line not in lines:
            lines.append(temp_line)
    return lines

class GNPRESET_OT_display_description(bpy.types.Operator):
    bl_idname = "gnpreset.display_description"
    bl_label = "Description"
    bl_description = "Display nodetree/preset description"
    bl_options = {"INTERNAL","REGISTER","UNDO"}

    description: bpy.props.StringProperty()
    url: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        if context.object.modifiers.active:
            active=context.object.modifiers.active
            return active.type=="NODES" and active.node_group

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        col=layout.column(align=True)
        if self.description:
            for line in cut_long_text(self.description):
                col.label(text=line)
        if self.url:
            op=layout.operator(
                'wm.url_open',
                text=f"Open {self.url}",
                icon="URL"
                )
            op.url=self.url

    def execute(self, context):
        return {'FINISHED'}

### REGISTER ---
def register():
    bpy.utils.register_class(GNPRESET_OT_display_description)
def unregister():
    bpy.utils.unregister_class(GNPRESET_OT_display_description)
