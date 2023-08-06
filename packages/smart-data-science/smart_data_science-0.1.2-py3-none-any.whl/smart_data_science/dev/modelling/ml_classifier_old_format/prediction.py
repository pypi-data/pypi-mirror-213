"""
- Title:            Utils Machine Learning. Common ML functions for Tabular Data based on sklearn & lightgbm libraries
- Project/Topic:    Utils Tabular Data. Practical functions for Data Science
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2020 - 2022

- Status:           Planning

- Acknowledgements. Based on: tabular-ml-product-template by Angel Martinez-Tenor

Steps:
- 1 Load an already trained model & an explainer of the model,
- 2 Generate a prediction endpoint ready for receiving json requests with 2 keys:
    - 'data' (Mandatory): Input Dataframe as json messages (dataframe to dict). Include Dataframe Indexes. A single
        sample can be sent in 1-row dataframe .
    - 'explained_predictions' (Optional): True/False
- 3 Perform batch prediction and responds with a json message with the predictions column. Perform shap computation for
    individual contributions if requested
- 4 Return a JSON message with the following keys:
    - 'predictions': Output Dataframe with predictions(dataframe to dict). Include Dataframe Indexes
    - 'contributions': Output Dataframe with predictions. Include Dataframe Indexes. 'None' if no contributions were
        requested/computed
"""

# TO IMPROVE: Adapt to BB and Complete docstrings
# ignore all mypy and pylint errors
# pylint: disable-all
# mypy: ignore-errors

# import json

# import pandas as pd
# import uvicorn
# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse

# # import joblib  # from sklearn.externals import joblib deprecated
# from . import ml, ml_explainer

# PYCARET_PIPELINE = False  # Optional: Pycaret pipelines can be also used. Default: scikit-learn pipelines

# # if PYCARET_PIPELINE:  # pycaret model finally removed from the deployed app, Only the scikit-learn model is deployed
# #     import ml_pycaret as ml

# # print(f'Work Path: {os.getcwd()}')

# app = FastAPI()

# # load the trained pipeline
# print()
# pipeline = ml.load_pipeline()
# explainer = ml_explainer.load_explainer(pycaret_pipeline=PYCARET_PIPELINE)

# print("\n ---- Endpoint Ready ----")


# @app.get("/")
# def test_msg():
#     """Show a test message if accesses to the endpoint root"""
#     return "Classifier Prediction service deployed OK!"


# @app.post("/predict")
# async def predict(request: Request):
#     """Classifier Prediction service"""

#     # get the input data
#     request_json = await request.json()
#     request_dict = json.loads(request_json)

#     df_to_predict = pd.DataFrame(request_dict["data"])

#     # Make prediction (& contributions of the first row)
#     df_prediction = ml.predict(pipeline, df_to_predict)

#     # df_prediction = df_prediction.sort_values(by='Score_True', ascending=False)
#     df_prediction = df_prediction[["True Prob %"]]

#     dict_cont = None
#     if request_dict["explained_predictions"] is True:  # explained predictions requested
#         df_contributions = ml_explainer.get_contributions(
#             pipeline, explainer, df_to_predict, pycaret_pipeline=PYCARET_PIPELINE
#         )
#         print(df_contributions.index)
#         print(df_prediction.index)
#         df_contributions = df_contributions.reindex(df_prediction.index)
#         # sort contributions frame as predictions frame
#         dict_cont = df_contributions.to_dict()

#     # Return prediction & contributions
#     dict_pred = df_prediction.to_dict()
#     response_dict = {"prediction": dict_pred, "contributions": dict_cont}
#     response_json = json.dumps(response_dict)

#     if not response_json:
#         response_json = '{"ERROR":"No inference was performed"}'

#     # print(f'\nINPUT: \n{request_json}\n')
#     # print(f'\nOUTPUT: \n{response_json}\n')

#     return JSONResponse(content=response_json)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000, debug=False)
