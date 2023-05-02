import bpy

class GNPRESET_MT_load_menu(bpy.types.Menu):
    bl_label = "Load Preset"

    def draw(self, context):
        active=context.object.modifiers.active
        preset_name=active.node_group.gnpreset.active_preset

        layout = self.layout

        op=layout.operator(
            'gnpreset.load_preset_multiple',
            text="Selection",
            )
        op.preset_name=preset_name
        op.selection=True
        op=layout.operator(
            'gnpreset.load_preset_multiple',
            text="All",
            )
        op.preset_name=preset_name
        op.selection=False

class GNPRESET_MT_manage_preset_menu(bpy.types.Menu):
    bl_label = "Manage Preset"

    def draw(self, context):
        active=context.object.modifiers.active
        preset_name=active.node_group.gnpreset.active_preset
        preset=active.node_group.gnpreset.presets[preset_name]

        layout = self.layout
        op=layout.operator(
            'gnpreset.modify_preset',
            text="Modify",
            icon="GREASEPENCIL",
            )
        op.preset_name=preset_name
        op=layout.operator(
            'gnpreset.replace_preset',
            text="Replace",
            icon="DISK_DRIVE",
            )
        op.preset_name=preset_name

        layout.separator()
        op=layout.operator(
            'gnpreset.remove_preset',
            text="Remove",
            icon="X",
            )
        op.preset_name=preset_name

def draw_modifier_menu(self, context):
    layout = self.layout
    row=layout.row(align=True)

    mods=context.object.modifiers
    if not mods.active\
    or not mods.active.type=="NODES"\
    or not mods.active.node_group:
        row.label(text="", icon="GEOMETRY_NODES")
    else:
        row.operator(
            'gnpreset.modify_nodetree_infos',
            text="",
            icon="GEOMETRY_NODES"
            )

        active=context.object.modifiers.active
        props=active.node_group.gnpreset

        # Description and URL
        row.separator()
        sub=row.row(align=True)
        if not props.description and not props.url:
            sub.enabled=False
        op=sub.operator(
            'gnpreset.display_description',
            text="",
            icon="INFO",
            )
        op.description=props.description
        op.url=props.url

        # New Preset
        row.separator()
        row.operator('gnpreset.save_preset', text="", icon="ADD")

        if props.presets:
            preset_name=props.active_preset
            preset=props.presets[preset_name]

            row.prop(
                props,
                "active_preset",
                text=""
                )
            # Description and URL
            sub=row.row(align=True)
            if not preset.description:
                sub.enabled=False
            op=sub.operator(
                'gnpreset.display_description',
                text="",
                icon="HELP"
                )
            op.description=preset.description
            op.url=""
            row.menu("GNPRESET_MT_manage_preset_menu", text="", icon="DOWNARROW_HLT")

            # Load
            row.separator()
            op=row.operator(
                'gnpreset.load_preset',
                text="",
                icon="CHECKMARK"
                )
            op.preset_name=preset_name

            row.menu("GNPRESET_MT_load_menu", text="", icon="DOWNARROW_HLT")

        return

    row.enabled=False
    sub=row.row(align=True)
    sub.alignment="RIGHT"
    sub.label(text="No Node Tree")


### REGISTER ---
def register():
    bpy.utils.register_class(GNPRESET_MT_load_menu)
    bpy.utils.register_class(GNPRESET_MT_manage_preset_menu)
    bpy.types.DATA_PT_modifiers.prepend(draw_modifier_menu)
def unregister():
    bpy.utils.unregister_class(GNPRESET_MT_load_menu)
    bpy.utils.unregister_class(GNPRESET_MT_manage_preset_menu)
    bpy.types.DATA_PT_modifiers.remove(draw_modifier_menu)
