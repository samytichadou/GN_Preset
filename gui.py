import bpy

class GNPRESET_MT_load_menu(bpy.types.Menu):
    bl_label = "Load Preset"

    def draw(self, context):
        active=context.object.modifiers.active
        preset_name=active.node_group.gnpreset_active_preset

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

def draw_modifier_menu(self, context):
    layout = self.layout
    row=layout.row(align=True)
    row.label(text="", icon="GEOMETRY_NODES")

    if context.object.modifiers.active:
        active=context.object.modifiers.active
        if active.type=="NODES" and active.node_group:
            ng=active.node_group

            # Description and URL
            sub=row.row(align=True)
            sub.separator()
            if not ng.gnpreset_description:
                sub.enabled=False
            op=sub.operator(
                'gnpreset.display_description',
                text="",
                icon="INFO"
                )
            op.description=ng.gnpreset_description
            sub=row.row(align=True)
            if not ng.gnpreset_url:
                sub.enabled=False
            op=sub.operator(
                'wm.url_open',
                text="",
                icon="URL"
                )
            op.url=ng.gnpreset_url
            op=row.operator(
                'gnpreset.modify_nodetree_infos',
                text="",
                icon="GREASEPENCIL"
                )

            # New Preset
            row.separator()
            row.operator('gnpreset.save_preset', text="", icon="ADD")

            if active.node_group.gnpreset_presets:
                preset_name=active.node_group.gnpreset_active_preset
                preset=active.node_group.gnpreset_presets[preset_name]

                # Preset handling
                row.separator()
                op=row.operator(
                    'gnpreset.replace_preset',
                    text="",
                    icon="DISK_DRIVE"
                    )
                op.preset_name=preset_name
                op=row.operator(
                    'gnpreset.modify_preset',
                    text="",
                    icon="GREASEPENCIL"
                    )
                op.preset_name=preset_name
                row.prop(
                    active.node_group,
                    "gnpreset_active_preset",
                    text=""
                    )
                op=row.operator(
                    'gnpreset.remove_preset',
                    text="",
                    icon="X"
                    )
                op.preset_name=preset_name

                # Description and URL
                sub=row.row(align=True)
                sub.separator()
                if not preset.description:
                    sub.enabled=False
                op=sub.operator(
                    'gnpreset.display_description',
                    text="",
                    icon="HELP"
                    )
                op.description=preset.description

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
    bpy.types.DATA_PT_modifiers.prepend(draw_modifier_menu)
def unregister():
    bpy.utils.unregister_class(GNPRESET_MT_load_menu)
    bpy.types.DATA_PT_modifiers.remove(draw_modifier_menu)
