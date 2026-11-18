bl_info = {
    "name": "FlatOut 2 Material Fixer",
    "blender": (4, 4, 3),
    "category": "Utilities",
    "author": "Zack Wilde"
}

import bpy

def GetBSDFNode(material):
    return material.node_tree.nodes["Principled BSDF"]

def GetTextureNode(material):
    return GetBSDFNode(material).inputs["Base Color"].links[0].from_node

def FixPath(path):
    if path[-1] not in "/\\":
        path += "\\" if "\\" in path else "/"
    return path

def _DDSToPNG(object, folderPath):
    material = object.data.materials[0]
    bsdfNode = GetBSDFNode(material)
    textureNode = GetTextureNode(material)
    path = textureNode.image.filepath

    if "." in path:
        if path[path.rindex(".") + 1:] == "dds":
            
            filename = path[path.rindex("\\" if "\\" in path else "/") + 1:]

            if IsRoadMaterial(material):
                filename = material.name.lower()
            
            # Clearing out both the extension from the filename, and any .00[n]'s that might be on the material name
            if "." in filename:
                filename = filename[:filename.index(".")]

            textureNode.image = bpy.data.images.load(folderPath + filename + ".png", check_existing=True)
         
    
class DDSToPNG(bpy.types.Operator):
    """Finds all objects using DDS textures and fetches the PNG version from the specified texture folder"""
    bl_idname = "fo2materialfixer.ddstopng"
    bl_label = "DDS to PNG"
    
    folderPath: bpy.props.StringProperty(name="Texture Folder Path")

    def execute(self, context):
        self.folderPath = FixPath(self.folderPath)
        
        for object in bpy.data.objects:
            if not object.data or object.type != "MESH":
                continue
            
            _DDSToPNG(object, self.folderPath)

        return { 'FINISHED' }
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

def _AlphaFix(object):
    material = object.data.materials[0]
    if "alpha" in material.name:
        material.node_tree.links.new(GetBSDFNode(material).inputs["Alpha"], GetTextureNode(material).outputs["Alpha"])
         

class AlphaFix(bpy.types.Operator):
    """Finds all objects with 'alpha' in the name, and hooks up the alpha to the principled BSDF"""
    bl_idname = "fo2materialfixer.alphafix"
    bl_label = "Apply Alpha"

    def execute(self, context):
        for object in bpy.data.objects:
            if not object.data or object.type != "MESH":
                continue

            _AlphaFix(object)

        return { 'FINISHED' }
    
def IsRoadMaterial(material):
    matName = material.name.lower()
    return matName.startswith("sdm_") or matName.startswith("dm_")

def _LevelUVFix(object, fixOldBug):
    material = object.data.materials[0]
    matName = material.name
    if len(object.data.uv_layers) > 1:
        if IsRoadMaterial(material):
            object.data.uv_layers[1].active_render = True

        # Automates fixing the bug from the last version
        elif fixOldBug and object.data.uv_layers[1].active_render:
            object.data.uv_layers[0].active_render = True

class LevelUVFix(bpy.types.Operator):
    """Finds all track geometry and fixes the UV map"""
    bl_idname = "fo2materialfixer.leveluvfix"
    bl_label = "Fix Track UVs"
    
    fixOldBug: bpy.props.BoolProperty(name="Undo UV fix on non-track")

    def execute(self, context):
        for object in bpy.data.objects:
            if not object.data or object.type != "MESH":
                continue
        
            _LevelUVFix(object, self.fixOldBug)

        return { 'FINISHED' }
        
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
def _RemoveMapping(object):
    material = object.data.materials[0]
    textureNode = GetTextureNode(material)

    if textureNode.type != "TEX_IMAGE":
        return

    if textureNode.inputs["Vector"].is_linked:
        material.node_tree.links.remove(textureNode.inputs["Vector"].links[0])
    
class RemoveMapping(bpy.types.Operator):
    """Finds all materials with a Mapping node connected to the colour texture and disconnects it"""
    bl_idname = "fo2materialfixer.removemapping"
    bl_label = "Disconnect Mapping Nodes"
    
    def execute(self, context):
        for object in bpy.data.objects:
            if not object.data or object.type != "MESH":
                continue
        
            _RemoveMapping(object)
                        
        return { 'FINISHED' }
    
def _SetChannelPacked(object):
    textureNode = GetTextureNode(object.data.materials[0])
    if textureNode.type != "TEX_IMAGE":
        return

    textureNode.image.alpha_mode = "CHANNEL_PACKED"
    
class SetChannelPacked(bpy.types.Operator):
    """Sets all the alpha modes on each texture to be 'Channel Packed' rather than 'Straight'"""
    bl_idname = "fo2materialfixer.setchannelpacked"
    bl_label = "Set Channel Packed Alpha Mode"
    
    def execute(self, context):
        for object in bpy.data.objects:
            if not object.data or object.type != "MESH":
                continue
            
            _SetChannelPacked(object)
            
        return { 'FINISHED' }
    
class FixEverything(bpy.types.Operator):
    """Perform every fixing operator in one go"""
    bl_idname = "fo2materialfixer.alloftheabove"
    bl_label = "Fix Everything"
    
    folderPath: bpy.props.StringProperty(name="Texture Folder Path")
    fixOldBug: bpy.props.BoolProperty(name="Undo UV fix on non-track")
    
    def execute(self, context):
        self.folderPath = FixPath(self.folderPath)

        for object in bpy.data.objects:
            if not object.data or object.type != "MESH":
                continue
            
            _DDSToPNG(object, self.folderPath)
            _AlphaFix(object)
            _LevelUVFix(object, self.fixOldBug)
            _RemoveMapping(object)
            _SetChannelPacked(object)

        return { 'FINISHED' }
            
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
        

class CustomMenu(bpy.types.Menu):
    bl_label = "FlatOut Material Fixer"
    bl_idname = "TOPBAR_MT_fo2materialfixer"

    def draw(self, context):
        layout = self.layout
        layout.operator("fo2materialfixer.ddstopng")
        layout.operator("fo2materialfixer.alphafix")
        layout.operator("fo2materialfixer.leveluvfix")
        layout.operator("fo2materialfixer.removemapping")
        layout.operator("fo2materialfixer.setchannelpacked")
        layout.operator("fo2materialfixer.alloftheabove")
        
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
    bpy.utils.register_class(RemoveMapping)
    bpy.utils.register_class(SetChannelPacked)
    bpy.utils.register_class(FixEverything)
    
    bpy.types.TOPBAR_HT_upper_bar.append(draw_item)
    
def unregister():
    bpy.types.TOPBAR_HT_upper_bar.pop()
    bpy.utils.unregister_class(DDSToPNG)
    bpy.utils.unregister_class(AlphaFix)
    bpy.utils.unregister_class(LevelUVFix)
    bpy.utils.unregister_class(CustomMenu)
    bpy.utils.unregister_class(RemoveMapping)
    bpy.utils.unregister_class(SetChannelPacked)
    bpy.utils.unregister_class(FixEverything)
    
    
if __name__ == "__main__":
    register()
