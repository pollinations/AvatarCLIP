from cog import BasePredictor, Path, Input
import os  
from glob import glob
class Predictor(BasePredictor):
    def setup(self):
        """Run pip install git+https://github.com/voodoohop/neural_renderer.git"""
        os.system('pip install git+https://github.com/voodoohop/neural_renderer.git')

    def predict(self,
            text: str = Input(description="Coarse character prompt", default="overweight sumo wrestler")
    ) -> Path:
        """Run python main.py --target_txt '[text]' in folder ./AvatarGen/ShapeGen"""
        previouspath = os.getcwd()
        os.chdir("./AvatarGen/ShapeGen/")
        os.system('python main.py --target_txt "' + text + '"')
        filepath = glob("./output/coarse_shape/*.obj")[0]
        print("returning",filepath)
        return Path(filepath)