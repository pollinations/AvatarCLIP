from cog import BasePredictor, Path, Input
import os  
from glob import glob

#MODEL_PATHS = "--smpl_model_folder /smpl_data --AE_path_fname /avatarclip_data/model_VAE_16.pth --codebook_fname /avatarclip_data/codebook.pth"

# INIT_COMMANDS="""pip install git+https://github.com/voodoohop/neural_renderer.git
# mv /avatarclip_data/* /src/AvatarGen/ShapeGen/data/
# mkdir -p /src/smpl_models
# mv /smpl_data /src/smpl_models/smpl"""

class Predictor(BasePredictor):
    def setup(self):
        """Run pip install git+https://github.com/voodoohop/neural_renderer.git"""
        os.system('pip install git+https://github.com/voodoohop/neural_renderer.git')
        os.system('mv -v /avatarclip_data /src/AvatarGen/ShapeGen/data')
        os.system('mkdir -p /src/AvatarGen/ShapeGen/output/coarse_shape')
        os.system('mkdir -p /src/smpl_models')
        os.system('mv -v /smpl_data /src/smpl_models/smpl')

    def predict(self,
            text: str = Input(description="Coarse character prompt", default="overweight sumo wrestler")
    ) -> Path:
        """Run python main.py --target_txt '[text]' in folder ./AvatarGen/ShapeGen"""
        print("creating avatar for text", text)
        previouspath = os.getcwd()
        os.chdir("./AvatarGen/ShapeGen/")
        print("glob before", glob("./output/coarse_shape/*.obj"))
        os.system(f'python main.py --target_txt "a 3d rendering of {text} in unreal engine"')
        
        filepaths = glob("./output/coarse_shape/*.obj")
        print("glob after", glob("./output/coarse_shape/*.obj"))
        print("returning",filepath)
        return [Path(filepath) for filepath in filepaths]

