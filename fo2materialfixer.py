bl_info = {
    "name": "FlatOut 2 Material Fixer",
    "blender": (4, 4, 3),
    "category": "Utilities",
    "author": "Zack Wilde"
}

import bpy
    
class DDSToPNG(bpy.types.Operator):
    """Finds all objects using DDS textures and fetches the PNG version from the specified texture folder"""
    bl_idname = "fo2materialfixer.ddstopng"
    bl_label = "DDS to PNG"
    
    folderPath: bpy.props.StringProperty(name="Texture Folder Path")

    def execute(self, context):
        for object in bpy.data.objects:
            if not object.data: continue
        
            image = object.data.materials[0].node_tree.nodes[3].image
            path = image.filepath
            if self.folderPath[-1] not in "/\\":
                self.folderPath += "\\" if "\\" in self.folderPath else "/"
            if "." in path:
                if path[path.rindex(".") + 1:] == "dds":
                    filename = path[path.rindex("\\" if "\\" in path else "//") + 1:path.rindex(".")]

                    matName = object.data.materials[0].name.lower()
                    if matName.startswith("sdm_") or matName.startswith("dm_"):
                        filename = matName
                        if "." in filename:
                            filename = filename[:filename.index(".")]

                    image.filepath = self.folderPath + filename + ".png"
                    image.reload()
                 
        return { 'FINISHED' }
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class AlphaFix(bpy.types.Operator):
    """Finds all objects with 'alpha' in the name, and hooks up the alpha to the principled BSDF"""
    bl_idname = "fo2materialfixer.alphafix"
    bl_label = "Apply Alpha"

    def execute(self, context):
        for object in bpy.data.objects:
            if not object.data: continue
                
            if "alpha" in object.data.materials[0].name:
                tree = object.data.materials[0].node_tree
                tree.links.new(tree.nodes[0].inputs[4], tree.nodes[3].outputs[1])
                 
        return { 'FINISHED' }


class LevelUVFix(bpy.types.Operator):
    """Finds all track geometry and fixes the UV map"""
    bl_idname = "fo2materialfixer.leveluvfix"
    bl_label = "Fix Track UVs"

    def execute(self, context):
        for object in bpy.data.objects:
            if not object.data: continue
        
            if len(object.data.uv_layers) > 1:
                object.data.uv_layers[1].active_render = True
                 
        return { 'FINISHED' }


    


class CustomMenu(bpy.types.Menu):
    bl_label = "FlatOut Material Fixer"
    bl_idname = "TOPBAR_MT_fo2materialfixer"

    def draw(self, context):
        layout = self.layout
        layout.operator("fo2materialfixer.ddstopng")
        layout.operator("fo2materialfixer.alphafix")
        layout.operator("fo2materialfixer.leveluvfix")
        
def SetScriptButton(self, context):
    layout = self.layout
    

def draw_item(self, context):
    layout = self.layout
    layout.menu(CustomMenu.bl_idname)
  
def register():
    bpy.utils.register_class(DDSToPNG)
    bpy.utils.register_class(AlphaFix)
    bpy.utils.register_class(LevelUVFix)
    bpy.utils.register_class(CustomMenu)
    
    bpy.types.TOPBAR_HT_upper_bar.append(draw_item)
    
def unregister():
    bpy.types.TOPBAR_HT_upper_bar.pop()
    bpy.utils.unregister_class(DDSToPNG)
    bpy.utils.unregister_class(AlphaFix)
    bpy.utils.unregister_class(LevelUVFix)
    bpy.utils.unregister_class(CustomMenu)
    
    
if __name__ == "__main__":
    register()