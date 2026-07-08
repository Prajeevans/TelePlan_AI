import joblib
import pandas as pd


class AIPredictor:

    def __init__(
        self,
        model_path="./ml/saved_models/rsrp_linear_model.pkl",
        preprocessor_path="./ml/saved_models/preprocessor.pkl"
    ):

        self.model = joblib.load(model_path)
        self.preprocessor = joblib.load(preprocessor_path)

    def predict(self, sample):

        df = pd.DataFrame([sample])

        X = self.preprocessor.transform(df)

        prediction = self.model.predict(X)

        return float(prediction[0])