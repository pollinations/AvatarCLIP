import os
import sys
from glob import glob
from time import sleep

import pymeshlab
from cog import BasePredictor, Input, Path

sys.path.append("/usr/local/lib/Python37_x64")

#MODEL_PATHS = "--smpl_model_folder /smpl_data --AE_path_fname /avatarclip_data/model_VAE_16.pth --codebook_fname /avatarclip_data/codebook.pth"



# mv -v /avatarclip_data /src/AvatarGen/ShapeGen/data
# mkdir -p /src/AvatarGen/ShapeGen/output/coarse_shape
# mkdir -p /src/smpl_models
# cp -rv /smpl_data /src/smpl_models/smpl

class Predictor(BasePredictor):
    def setup(self):
        """Run pip install git+https://github.com/voodoohop/neural_renderer.git"""
        os.system('pip install git+https://github.com/voodoohop/neural_renderer.git')
        os.system('mv -v /avatarclip_data /src/AvatarGen/ShapeGen/data')
        os.system('mkdir -p /src/AvatarGen/ShapeGen/output/coarse_shape')
        os.system('mkdir -p /src/smpl_models')
        os.system('cp -rv /smpl_data /src/smpl_models/smpl')
        os.system('mkdir -p /smpl_data/smpl')
        os.system('cp -rv /smpl_data/* /smpl_data/smpl')
        

    def predict(self,
            text: str = Input(description="prompt", default="overweight sumo wrestler"),
            fine: bool = Input(description="whether to generate a coarse avatar with no color (fast) or whether to add detail and texture (slow)", default=True),
            iterations: int = Input(description="number of iterations (for fine avatar)", default=10000)
    ) -> Path:
        """Run python main.py --target_txt '[text]' in folder ./AvatarGen/ShapeGen"""

        print("creating avatar for text", text)
        iterations = max(501, iterations) # otherwise not a single mesh will be written

        
        if not fine:
            previouspath = os.getcwd()
            os.chdir("/src/AvatarGen/ShapeGen/")
            print("glob before", glob("./output/coarse_shape/*.obj"))
            os.system(f'rm -rf ./output/coarse_shape')
            os.system(f'python main.py --target_txt "a 3d rendering of {text} in unreal engine"')
            
            filepaths = sorted(glob("./output/coarse_shape/*.obj"))
            print("glob after", glob("./output/coarse_shape/*.obj"))
            print("returning",filepaths)
            
            filepath_coarse_obj = filepaths[0]

            # save as glb file
            sleep(1)
            target_glb_path = os.path.join("/outputs",f"z_avatar.glb")
            print("running ", f"obj2gltf -i {filepath_coarse_obj} -o {target_glb_path}")
            os.system(f"obj2gltf -i {filepath_coarse_obj} -o {target_glb_path}")            

            return Path(filepath_coarse_obj)
        else:
            os.chdir("/src/AvatarGen/AppearanceGen/")
            os.system(f'python main.py --mode train_clip --conf confs/examples_small/pollinations.conf --prompt "{text}" --iterations {iterations}')
            
            # transform NERF to mesh
            os.system('python main.py --mode validate_mesh --conf confs/examples_small/example.conf')
       
            # convert mesh to obj

            print("glob before: /output/coarse_shape/*.obj", glob("/output/coarse_shape/*.obj"))
            lastmesh = sorted(glob("/outputs/meshes/*.ply"))[-1]

            os.system(f'cp {lastmesh} /outputs/mesh.ply')
            
            target_path = f"/outputs/z_avatar.obj"

            print(f"converting mesh '{lastmesh}' to obj")
            ms = pymeshlab.MeshSet()
            ms.load_new_mesh(lastmesh)
            ms.compute_color_transfer_vertex_to_face()
            ms.meshing_decimation_quadric_edge_collapse(targetfacenum=20000)
            ms.save_current_mesh(target_path) 
            

            # save as glb file
            sleep(1)
            target_glb_path = os.path.join("/outputs",f"z_avatar.glb")
            print("running ", f"obj2gltf -i {target_path} -o {target_glb_path}")
            os.system(f"obj2gltf -i {target_path} -o {target_glb_path}")


            os.chdir('/src/Avatar2FBX/')
            os.system('mkdir -p ./meshes')
            os.system(f'cp -v {lastmesh} ./meshes')
            os.system('python3.6 export_fbx.py')
            os.system('ls -l ./outputs/')
            os.system('cp -v ./outputs/*.fbx /outputs/y_avatar.fbx')

            os.system('ls -l /outputs')
            lastimage = sorted(glob("/outputs/*.png"))[-1]
            os.system("rm -rv /outputs/logs /outputs/normals /outputs/recording")
            
            print("returning last image",lastimage)
            return Path(lastimage)
