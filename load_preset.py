import bpy

def set_input(preset_input, ng_input):
    if preset_input.type in ("VECTOR","RGBA"):
        for i in range(0,len(ng_input)):
            ng_input[i]=getattr(preset_input, preset_input.type.lower())[i]
    else:
        ng_input=getattr(preset_input, preset_input.type.lower())

def set_nodegroup_inputs(preset, modifier):
    for input in preset.inputs:
        print(input.name)
        chk=0
        for i in modifier.node_group.inputs:
            if i.name==input.name and i.identifier==input.identifier:
                print(f"match : {i.name}")
                if input.type in ("VECTOR","RGBA"):
                    for n in range(0,len(modifier[i.identifier])):
                        modifier[i.identifier][n]=getattr(input, input.type.lower())[n]
                else:
                    modifier[i.identifier]=getattr(input, input.type.lower())
                chk=1
                break
        if chk==0:
            for i in modifier.node_group.inputs:
                if i.name==input.name:
                    print(f"semimatch : {i.name}")
                    if input.type in ("VECTOR","RGBA"):
                        for n in range(0,len(modifier[i.identifier])):
                            modifier[i.identifier][n]=getattr(input, input.type.lower())[n]
                    else:
                        modifier[i.identifier]=getattr(input, input.type.lower())
                    break

class GNPRESET_OT_load_preset(bpy.types.Operator):
    bl_idname = "gnpreset.load_preset"
    bl_label = "Load Preset"
    bl_description = ""
    bl_options = {"INTERNAL","REGISTER","UNDO"}

    preset_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        if context.object.modifiers.active:
            active=context.object.modifiers.active
            return active.type=="NODES" and active.node_group

    def execute(self, context):
        mod=context.object.modifiers.active
        preset=mod.node_group.gnpreset_presets[self.preset_name]

        set_nodegroup_inputs(preset, mod)

        self.report({'INFO'}, f"Preset {self.preset_name} loaded")

        # Redraw ui
        for area in context.screen.areas:
            area.tag_redraw()

        return {'FINISHED'}

### REGISTER ---
def register():
    bpy.utils.register_class(GNPRESET_OT_load_preset)
def unregister():
    bpy.utils.unregister_class(GNPRESET_OT_load_preset)
