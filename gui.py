import bpy

def draw_modifier_menu(self, context):
    layout = self.layout
    row=layout.row(align=True)
    row.label(text="Presets", icon="GEOMETRY_NODES")
    row.operator('gnpreset.save_preset', text="Create", icon="ADD")

    if context.object.modifiers.active:
        active=context.object.modifiers.active
        if active.type=="NODES" and active.node_group:
            if active.node_group.gnpreset_presets:
                row.separator()
                row.prop(active.node_group, "gnpreset_active_preset", text="")
                op=row.operator('gnpreset.load_preset', text="", icon="CHECKMARK")
                op.preset_name=active.node_group.gnpreset_active_preset
                op=row.operator('gnpreset.remove_preset', text="", icon="X")
                op.preset_name=active.node_group.gnpreset_active_preset

### REGISTER ---
def register():
    bpy.types.DATA_PT_modifiers.prepend(draw_modifier_menu)
def unregister():
    bpy.types.DATA_PT_modifiers.remove(draw_modifier_menu)
