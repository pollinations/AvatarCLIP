from cog import BasePredictor, Path, Input
import os  
from glob import glob

#MODEL_PATHS = "--smpl_model_folder /smpl_data --AE_path_fname /avatarclip_data/model_VAE_16.pth --codebook_fname /avatarclip_data/codebook.pth"

class Predictor(BasePredictor):
    def setup(self):
        """Run pip install git+https://github.com/voodoohop/neural_renderer.git"""
        os.system('pip install git+https://github.com/voodoohop/neural_renderer.git')
        os.system('mv /avatarclip_data /src/AvatarGen/ShapeGen/data')
        os.system('mkdir -p /src/smpl_models')
        os.system('mv /smpl_data /src/smpl_models/smpl')

    def predict(self,
            text: str = Input(description="Coarse character prompt", default="overweight sumo wrestler")
    ) -> Path:
        """Run python main.py --target_txt '[text]' in folder ./AvatarGen/ShapeGen"""
        previouspath = os.getcwd()
        os.chdir("./AvatarGen/ShapeGen/")
        os.system(f'python main.py --target_txt "{text}"')
        filepath = glob("./output/coarse_shape/*.obj")[0]
        print("returning",filepath)
        return Path(filepath)

